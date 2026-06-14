#!/usr/bin/env python3
"""
VoltAI — GPU Inference Gateway
OpenAI-compatible API with Lightning payments.

Grandma-friendly: visit → sign up → add credits → use API.
"""

import os, json, secrets, asyncio
from datetime import datetime

import httpx
from fastapi import FastAPI, Request, HTTPException, Response, Cookie
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
import uvicorn

from db import (init_db, get_db, hash_pass, check_pass, hash_key,
                generate_key, sats_for_tokens, tokens_for_sats)
from templates import LANDING_HTML, LOGIN_HTML, SIGNUP_HTML, APP_HTML

# ─── Config ──────────────────────────────────────────────────────────
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
PORT = int(os.environ.get("PORT", "11435"))
HOST = os.environ.get("HOST", "0.0.0.0")
BASE_URL = os.environ.get("BASE_URL", f"http://127.0.0.1:{PORT}")
LN_ADDRESS = os.environ.get("LN_ADDRESS", "postalzombie921@minibits.cash")
MINIBITS_LNURL = f"https://minibits.cash/.well-known/lnurlp/{LN_ADDRESS.split('@')[0]}"
PRICE = int(os.environ.get("PRICE_SATS_PER_M", "50"))
FREE_TOKENS = int(os.environ.get("FREE_TOKENS", "10000"))
SITE_NAME = "VoltAI"

app = FastAPI(title=SITE_NAME, version="1.0.0")
client = httpx.AsyncClient(timeout=120.0)

# ─── Error Logger ────────────────────────────────────────────────────
def log_error(user_id=None, api_key_id=None, endpoint=None, method=None,
              status_code=None, error_type=None, error_msg=None, request_body=None, ip=None):
    try:
        with get_db() as db:
            db.execute(
                """INSERT INTO error_log (user_id, api_key_id, endpoint, method, status_code,
                   error_type, error_msg, request_body, ip_address)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (user_id, api_key_id, endpoint, method, status_code,
                 error_type, error_msg, str(request_body)[:500] if request_body else None, ip)
            )
    except Exception:
        pass

# ─── Auth Helpers ────────────────────────────────────────────────────
def get_user(request: Request) -> dict | None:
    token = request.cookies.get("session")
    if not token:
        return None
    with get_db() as db:
        row = db.execute(
            "SELECT u.* FROM users u JOIN sessions s ON u.id=s.user_id WHERE s.token=? AND s.expires_at>datetime('now')",
            (token,)
        ).fetchone()
    return dict(row) if row else None

def require_user(request: Request) -> dict:
    user = get_user(request)
    if not user:
        raise HTTPException(401, "Not logged in")
    return user

# ─── Auth Routes ─────────────────────────────────────────────────────
@app.get("/signup")
async def signup_page():
    return HTMLResponse(SIGNUP_HTML)

@app.post("/api/auth/signup")
async def signup(request: Request):
    data = await request.json()
    username = data.get("username", "").strip()
    password = data.get("password", "")
    email = data.get("email", "").strip() or None
    
    if not username or len(username) < 3:
        raise HTTPException(400, "Username must be at least 3 characters")
    if not password or len(password) < 6:
        raise HTTPException(400, "Password must be at least 6 characters")
    
    with get_db() as db:
        existing = db.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
        if existing:
            raise HTTPException(400, "Username already taken")
        
        db.execute(
            "INSERT INTO users (email, username, pass_hash) VALUES (?, ?, ?)",
            (email, username, hash_pass(password))
        )
        user_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        
        # Create default API key with free credits
        raw_key = generate_key()
        db.execute(
            "INSERT INTO api_keys (user_id, key_hash, key_prefix, name, credits) VALUES (?, ?, ?, 'Default', ?)",
            (user_id, hash_key(raw_key), raw_key[:12] + "...", FREE_TOKENS)
        )
        
        # Create session
        session_token = secrets.token_hex(32)
        db.execute(
            "INSERT INTO sessions (token, user_id) VALUES (?, ?)",
            (session_token, user_id)
        )
    
    resp = RedirectResponse("/", status_code=303)
    resp.set_cookie("session", session_token, httponly=True, samesite="lax", max_age=60*60*24*7)
    return resp

@app.post("/api/auth/login")
async def login(request: Request):
    data = await request.json()
    username = data.get("username", "").strip()
    password = data.get("password", "")
    
    with get_db() as db:
        user = db.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        if not user or not check_pass(password, user["pass_hash"]):
            raise HTTPException(401, "Invalid username or password")
        
        session_token = secrets.token_hex(32)
        db.execute("INSERT INTO sessions (token, user_id) VALUES (?, ?)",
                   (session_token, user["id"]))
    
    resp = JSONResponse({"status": "ok", "redirect": "/app"})
    resp.set_cookie("session", session_token, httponly=True, samesite="lax", max_age=60*60*24*7)
    return resp

@app.get("/api/auth/logout")
async def logout(request: Request):
    token = request.cookies.get("session")
    if token:
        with get_db() as db:
            db.execute("DELETE FROM sessions WHERE token=?", (token,))
    resp = RedirectResponse("/", status_code=303)
    resp.delete_cookie("session")
    return resp

@app.get("/login")
async def login_page():
    return HTMLResponse(LOGIN_HTML)

# ─── Bot Registration (no session needed) ────────────────────────────
@app.post("/api/auth/register")
async def register_bot(request: Request):
    """Bot-friendly signup: returns API key directly. No CAPTCHA, no email."""
    data = await request.json()
    username = data.get("username", "").strip()
    password = data.get("password", "")
    
    if not username or len(username) < 3:
        raise HTTPException(400, "Username must be at least 3 characters")
    if not password or len(password) < 6:
        raise HTTPException(400, "Password must be at least 6 characters")
    
    with get_db() as db:
        existing = db.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
        if existing:
            raise HTTPException(400, "Username already taken")
        
        db.execute(
            "INSERT INTO users (username, pass_hash) VALUES (?, ?)",
            (username, hash_pass(password))
        )
        user_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        
        raw_key = generate_key()
        db.execute(
            "INSERT INTO api_keys (user_id, key_hash, key_prefix, name, credits) VALUES (?, ?, ?, 'Default', ?)",
            (user_id, hash_key(raw_key), raw_key[:12] + "...", FREE_TOKENS)
        )
    
    return {"api_key": raw_key, "username": username, "free_tokens": FREE_TOKENS}

# ─── Error Console ───────────────────────────────────────────────────
@app.get("/api/errors")
async def get_errors(request: Request, limit: int = 50):
    user = get_user(request)
    if not user:
        raise HTTPException(401)
    
    with get_db() as db:
        errors = db.execute(
            """SELECT id, endpoint, method, status_code, error_type, error_msg,
                      ip_address, created_at
               FROM error_log WHERE user_id=? OR user_id IS NULL
               ORDER BY created_at DESC LIMIT ?""",
            (user["id"], limit)
        ).fetchall()
    
    return {"errors": [dict(e) for e in errors]}

@app.get("/api/errors/all")
async def get_all_errors(request: Request, limit: int = 100):
    """Admin view: all errors from all users."""
    user = get_user(request)
    if not user:
        raise HTTPException(401)
    
    with get_db() as db:
        errors = db.execute(
            """SELECT e.id, e.user_id, u.username, e.endpoint, e.method,
                      e.status_code, e.error_type, e.error_msg, e.ip_address, e.created_at
               FROM error_log e LEFT JOIN users u ON e.user_id=u.id
               ORDER BY e.created_at DESC LIMIT ?""",
            (limit,)
        ).fetchall()
    
    return {"errors": [dict(e) for e in errors]}

@app.delete("/api/errors")
async def clear_errors(request: Request):
    user = get_user(request)
    if not user:
        raise HTTPException(401)
    with get_db() as db:
        db.execute("DELETE FROM error_log WHERE user_id=?", (user["id"],))
    return {"status": "ok"}

# ─── Dashboard (logged in) ──────────────────────────────────────────
@app.get("/app")
async def app_page(request: Request):
    user = get_user(request)
    if not user:
        return RedirectResponse("/login", status_code=303)
    return HTMLResponse(APP_HTML)

@app.get("/api/me")
async def api_me(request: Request):
    user = get_user(request)
    if not user:
        raise HTTPException(401)
    
    with get_db() as db:
        keys = db.execute(
            "SELECT id, key_prefix, name, credits, total_used, created_at, last_used FROM api_keys WHERE user_id=?",
            (user["id"],)
        ).fetchall()
        
        total_credits = sum(k["credits"] for k in keys)
        total_used = sum(k["total_used"] for k in keys)
        
        usage_7d = db.execute(
            """SELECT date(created_at) as date, SUM(tokens_in+tokens_out) as tokens, 
                      SUM(cost_sats) as sats, COUNT(*) as requests
               FROM usage_log WHERE user_id=? AND created_at>=datetime('now','-7 days')
               GROUP BY date(created_at) ORDER BY date""",
            (user["id"],)
        ).fetchall()
        
        today = db.execute(
            "SELECT COALESCE(SUM(tokens_in+tokens_out),0) FROM usage_log WHERE user_id=? AND date(created_at)=date('now')",
            (user["id"],)
        ).fetchone()[0]
    
    return {
        "user": {"username": user["username"], "email": user["email"]},
        "keys": [dict(k) for k in keys],
        "stats": {"total_credits": total_credits, "total_used": total_used, "today_tokens": today},
        "usage_7d": [dict(u) for u in usage_7d],
    }

# ─── Key Management ─────────────────────────────────────────────────
@app.post("/api/keys")
async def create_key(request: Request):
    user = require_user(request)
    data = await request.json()
    name = data.get("name", "Default")
    raw_key = generate_key()
    
    with get_db() as db:
        db.execute(
            "INSERT INTO api_keys (user_id, key_hash, key_prefix, name, credits) VALUES (?, ?, ?, ?, ?)",
            (user["id"], hash_key(raw_key), raw_key[:12] + "...", name, FREE_TOKENS)
        )
    
    return {"key": raw_key, "name": name, "free_tokens": FREE_TOKENS}

@app.delete("/api/keys/{key_id}")
async def delete_key(key_id: int, request: Request):
    user = require_user(request)
    with get_db() as db:
        db.execute("DELETE FROM api_keys WHERE id=? AND user_id=?", (key_id, user["id"]))
    return {"status": "ok"}

# ─── Buy Credits ────────────────────────────────────────────────────
@app.post("/api/buy")
async def buy_credits(request: Request):
    user = require_user(request)
    data = await request.json()
    key_id = data.get("key_id")
    sats = data.get("amount_sats", 100)
    
    if not key_id:
        log_error(user_id=user["id"], endpoint="/api/buy", method="POST", status_code=400,
                  error_type="validation", error_msg="key_id required",
                  ip=request.client.host if request.client else None)
        raise HTTPException(400, "key_id required")
    
    tokens = tokens_for_sats(sats)
    
    # Get invoice from Minibits
    try:
        resp = await client.get(f"{MINIBITS_LNURL}?amount={sats*1000}")
        ln_data = resp.json()
        if ln_data.get("status") == "ERROR":
            log_error(user_id=user["id"], endpoint="/api/buy", method="POST", status_code=502,
                      error_type="minibits", error_msg=ln_data.get("reason", "Unknown Minibits error"),
                      ip=request.client.host if request.client else None)
            raise HTTPException(502, f"Minibits error: {ln_data.get('reason')}")
    except httpx.RequestError as e:
        log_error(user_id=user["id"], endpoint="/api/buy", method="POST", status_code=502,
                  error_type="minibits", error_msg=str(e)[:200],
                  ip=request.client.host if request.client else None)
        raise HTTPException(502, f"Failed to reach Minibits: {e}")
    
    payment_hash = secrets.token_hex(32)
    
    with get_db() as db:
        db.execute(
            """INSERT INTO invoices (payment_hash, key_id, user_id, amount_sats, tokens, lninvoice, verify_url)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (payment_hash, key_id, user["id"], sats, tokens, ln_data.get("pr"), ln_data.get("verify"))
        )
    
    return {
        "payment_hash": payment_hash,
        "amount_sats": sats,
        "tokens": tokens,
        "invoice": ln_data.get("pr"),
        "verify_url": ln_data.get("verify"),
    }

@app.get("/api/invoice/{ph}/status")
async def invoice_status(ph: str, request: Request):
    user = require_user(request)
    with get_db() as db:
        inv = db.execute("SELECT * FROM invoices WHERE payment_hash=? AND user_id=?", (ph, user["id"])).fetchone()
        if not inv:
            raise HTTPException(404)
        inv = dict(inv)
        
        if inv["status"] == "paid":
            return {"status": "paid", "tokens": inv["tokens"]}
        
        if inv["verify_url"]:
            try:
                r = await client.get(inv["verify_url"])
                if r.json().get("status") == "OK":
                    db.execute("UPDATE api_keys SET credits=credits+? WHERE id=?", (inv["tokens"], inv["key_id"]))
                    db.execute("UPDATE invoices SET status='paid', paid_at=datetime('now') WHERE payment_hash=?", (ph,))
                    return {"status": "paid", "tokens": inv["tokens"]}
            except Exception:
                pass
        
        return {"status": "pending", "amount_sats": inv["amount_sats"]}

# ─── Ollama Proxy ────────────────────────────────────────────────────
@app.api_route("/v1/{path:path}", methods=["GET","POST","PUT","DELETE"])
async def ollama_proxy(path: str, request: Request):
    auth = request.headers.get("authorization")
    if not auth:
        log_error(endpoint=f"/v1/{path}", method=request.method, status_code=401,
                  error_type="auth", error_msg="Missing Authorization header",
                  ip=request.client.host if request.client else None)
        raise HTTPException(401, "Missing Authorization header")
    
    token = auth.replace("Bearer ", "").strip()
    if not token.startswith("sk-"):
        log_error(endpoint=f"/v1/{path}", method=request.method, status_code=401,
                  error_type="auth", error_msg="Invalid key format",
                  ip=request.client.host if request.client else None)
        raise HTTPException(401, "Invalid key format")
    
    with get_db() as db:
        key = db.execute("SELECT * FROM api_keys WHERE key_hash=?", (hash_key(token),)).fetchone()
        if not key:
            log_error(endpoint=f"/v1/{path}", method=request.method, status_code=401,
                      error_type="auth", error_msg="Invalid API key",
                      ip=request.client.host if request.client else None)
            raise HTTPException(401, "Invalid API key")
        key = dict(key)
    
    body = await request.body()
    
    # Map OpenAI paths to Ollama paths
    ollama_path = path
    if path.startswith("chat/completions"):
        ollama_path = "api/chat"
    elif path.startswith("completions"):
        ollama_path = "api/generate"
    elif path == "models":
        ollama_path = "api/tags"
    
    # Estimate tokens
    is_chat = False
    est_tokens = 0
    if body:
        try:
            data = json.loads(body)
            if "messages" in data or "prompt" in data:
                is_chat = True
                txt = json.dumps(data.get("messages", [{"role":"user","content":data.get("prompt","")}]))
                est_tokens = len(txt)//4 + (data.get("options",{}).get("num_predict",512) or 512)
                cost = sats_for_tokens(est_tokens)
                if key["credits"] < cost:
                    log_error(user_id=key["user_id"], api_key_id=key["id"],
                              endpoint=f"/v1/{path}", method=request.method, status_code=402,
                              error_type="billing", error_msg=f"Insufficient credits: need {cost}, have {key['credits']}",
                              ip=request.client.host if request.client else None)
                    raise HTTPException(402, f"Insufficient credits. Need {cost} sats, have {key['credits']}")
        except json.JSONDecodeError:
            pass
    
    # Forward to Ollama
    target = f"{OLLAMA_URL}/{ollama_path}"
    headers = {k:v for k,v in request.headers.items() if k.lower() not in ("host","authorization")}
    
    try:
        resp = await client.request(request.method, target, content=body, headers=headers)
    except httpx.ConnectError:
        log_error(user_id=key["user_id"], api_key_id=key["id"],
                  endpoint=f"/v1/{path}", method=request.method, status_code=502,
                  error_type="proxy", error_msg="Ollama not running",
                  ip=request.client.host if request.client else None)
        raise HTTPException(502, "Ollama not running")
    except Exception as e:
        log_error(user_id=key["user_id"], api_key_id=key["id"],
                  endpoint=f"/v1/{path}", method=request.method, status_code=502,
                  error_type="proxy", error_msg=str(e)[:200],
                  ip=request.client.host if request.client else None)
        raise HTTPException(502, f"Proxy error: {e}")
    
    # Streaming
    if "text/event-stream" in resp.headers.get("content-type",""):
        return Response(content=resp.content, status_code=resp.status_code,
                       media_type="text/event-stream",
                       headers={"Cache-Control":"no-cache","X-Accel-Buffering":"no"})
    
    # Log non-200 Ollama responses
    if resp.status_code != 200:
        try:
            err_body = resp.json()
            log_error(user_id=key["user_id"], api_key_id=key["id"],
                      endpoint=f"/v1/{path}", method=request.method, status_code=resp.status_code,
                      error_type="ollama", error_msg=str(err_body.get("error", resp.text))[:200],
                      ip=request.client.host if request.client else None)
        except Exception:
            pass
    
    # Count actual tokens
    if is_chat and resp.status_code == 200:
        try:
            rd = resp.json()
            actual = rd.get("prompt_eval_count",0) + rd.get("eval_count",0)
            if actual == 0: actual = est_tokens
            actual_cost = sats_for_tokens(actual)
            est_cost = sats_for_tokens(est_tokens)
            if actual_cost != est_cost:
                with get_db() as db:
                    db.execute("UPDATE api_keys SET credits=credits+? WHERE id=?", (est_cost-actual_cost, key["id"]))
            with get_db() as db:
                db.execute(
                    "INSERT INTO usage_log (user_id,key_id,model,tokens_in,tokens_out,cost_sats) VALUES (?,?,?,?,?,?)",
                    (key["user_id"], key["id"], rd.get("model","?"),
                     rd.get("prompt_eval_count",0), rd.get("eval_count",0), actual_cost)
                )
        except Exception:
            pass
    
    return Response(content=resp.content, status_code=resp.status_code,
                   media_type=resp.headers.get("content-type","application/json"))

# ─── Public Ollama endpoints ─────────────────────────────────────────
@app.get("/v1/models")
async def list_models():
    try:
        r = await client.get(f"{OLLAMA_URL}/api/tags")
        models = r.json().get("models", [])
        return {"data": [{"id": m["name"], "object": "model"} for m in models]}
    except:
        return {"data": []}

# ─── Landing ─────────────────────────────────────────────────────────
@app.get("/")
async def landing(request: Request):
    user = get_user(request)
    if user:
        return RedirectResponse("/app", status_code=303)
    return HTMLResponse(LANDING_HTML)

# ─── Start ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    print(f"{SITE_NAME} running on {HOST}:{PORT}")
    print(f"Ollama: {OLLAMA_URL}")
    print(f"Wallet: {LN_ADDRESS}")
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")
