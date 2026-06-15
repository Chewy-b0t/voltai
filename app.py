#!/usr/bin/env python3
"""
VoltAI — GPU Inference Gateway
OpenAI-compatible API with Lightning payments.

Grandma-friendly: visit → sign up → add credits → use API.
"""

import os, json, secrets, asyncio, sqlite3
from pathlib import Path
from datetime import datetime

import httpx
from fastapi import FastAPI, Request, HTTPException, Response, Cookie
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, StreamingResponse
import uvicorn

from db import (init_db, get_db, hash_pass, check_pass, hash_key,
                generate_key, sats_for_tokens, tokens_for_sats)
from templates import LANDING_HTML, LOGIN_HTML, SIGNUP_HTML, APP_HTML

# ─── Config ──────────────────────────────────────────────────────────
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
GATEWAY_URL = os.environ.get("GATEWAY_URL", "http://127.0.0.1:11440")
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
        "ln_address": LN_ADDRESS,
        "price_per_m": PRICE,
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
        # Use Ollama's own OpenAI-compatible endpoint for proper format
        ollama_path = "v1/chat/completions"
    elif path.startswith("completions"):
        ollama_path = "v1/completions"
    elif path == "models":
        ollama_path = "v1/models"
    
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
    headers = {k:v for k,v in request.headers.items() if k.lower() not in ("host","authorization","content-length","content-type")}
    
    try:
        # Check if client wants streaming
        wants_stream = data.get("stream", True) if body else True
        
        if wants_stream:
            # Stream response directly
            req = client.build_request(request.method, target, content=body, headers=headers)
            resp = await client.send(req, stream=True)
            
            async def stream_gen():
                total_tokens = 0
                async for chunk in resp.aiter_bytes():
                    yield chunk
                await resp.aclose()
            
            return StreamingResponse(stream_gen(), media_type="text/event-stream",
                                   headers={"Cache-Control":"no-cache","X-Accel-Buffering":"no"})
        else:
            resp = await client.request(request.method, target, content=body, headers=headers)
    except httpx.ConnectError:
        log_error(user_id=key["user_id"], api_key_id=key["id"],
                  endpoint=f"/v1/{path}", method=request.method, status_code=502,
                  error_type="proxy", error_msg="Ollama not running",
                  ip=request.client.host if request.client else None)
        raise HTTPException(502, "Ollama not running")
    except Exception as e:
        log_error(user_id=key["user_id"], api_key_id=key["id"],
                  endpoint=f"/v1/{path}", method=request.method, status_code=500,
                  error_type="proxy", error_msg=str(e)[:200],
                  ip=request.client.host if request.client else None)
        raise HTTPException(500, f"Proxy error: {e}")
    
    # Non-streaming response
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
            # qwen3.5 fix: if content is empty but reasoning exists, use it
            choices = rd.get("choices", [])
            msg = choices[0].get("message", {}) if choices else {}
            if not msg.get("content") and msg.get("reasoning"):
                rd["choices"][0]["message"]["content"] = msg["reasoning"]
                return Response(content=json.dumps(rd).encode(),
                    status_code=200, media_type="application/json")
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

@app.get("/owlrun")
async def owlrun_dashboard():
    """Serve the Owlrun-style dashboard."""
    from fastapi.responses import HTMLResponse
    html_path = Path("/home/y/voltai/static/owlrun.html")
    if html_path.exists():
        return HTMLResponse(content=html_path.read_text())
    return HTMLResponse(content="<h1>Owlrun dashboard not found</h1>", status_code=404)

def get_setting(key, default=""):
    with get_db() as db:
        row = db.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        return row["value"] if row else default

def set_setting(key, value):
    with get_db() as db:
        db.execute("INSERT OR REPLACE INTO settings (key, value, updated_at) VALUES (?, ?, datetime('now'))", (key, str(value)))

def get_gpu_info():
    """Get GPU info via nvidia-smi."""
    import subprocess
    try:
        out = subprocess.check_output([
            "nvidia-smi", "--query-gpu=name,memory.total,memory.used,memory.free,temperature.gpu,power.draw,utilization.gpu",
            "--format=csv,noheader,nounits"
        ], timeout=5, text=True).strip().split(", ")
        return {
            "name": out[0],
            "vendor": "NVIDIA",
            "vram_total_mb": int(out[1]),
            "vram_used_mb": int(out[2]),
            "vram_free_mb": int(out[3]),
            "temp_c": int(out[4]),
            "power_w": float(out[5]),
            "util_pct": int(out[6]),
            "vram_exact": True
        }
    except:
        return {"name": "Unknown GPU", "vendor": "unknown", "vram_total_mb": 0, "vram_free_mb": 0, "temp_c": 0, "power_w": 0, "util_pct": 0, "vram_exact": False}

def get_disk_info():
    import shutil
    try:
        usage = shutil.disk_usage("/")
        return {
            "path": "/",
            "total_gb": round(usage.total / (1024**3), 1),
            "free_gb": round(usage.free / (1024**3), 1),
            "free_pct": round(usage.free / usage.total * 100, 1)
        }
    except:
        return {"path": "/", "total_gb": 0, "free_gb": 0, "free_pct": 0}

def get_earnings_data():
    """Get real earnings from gateway.db."""
    gateway_db = "/home/y/payout-gateway/gateway.db"
    try:
        conn = sqlite3.connect(gateway_db)
        conn.row_factory = sqlite3.Row
        # Total earned
        total = conn.execute("SELECT COALESCE(SUM(cost_sats),0) as sats FROM transactions").fetchone()["sats"]
        # Today
        today = conn.execute("SELECT COALESCE(SUM(cost_sats),0) as sats FROM transactions WHERE date(created_at)=date('now')").fetchone()["sats"]
        # Pending
        pending = conn.execute("SELECT COALESCE(SUM(cost_sats),0) as sats FROM transactions WHERE settled=0").fetchone()["sats"]
        # Withdrawn
        withdrawn = conn.execute("SELECT COALESCE(SUM(amount_sats),0) as sats FROM payouts WHERE status='settled'").fetchone()["sats"]
        # Today tokens and jobs from VoltAI's own usage_log
        conn.close()
        try:
            vconn = sqlite3.connect("/home/y/voltai/voltai.db")
            vconn.row_factory = sqlite3.Row
            tokens_today = vconn.execute("SELECT COALESCE(SUM(tokens_in+tokens_out),0) as t FROM usage_log WHERE date(created_at)=date('now')").fetchone()["t"]
            jobs_today = vconn.execute("SELECT COUNT(*) as c FROM usage_log WHERE date(created_at)=date('now')").fetchone()["c"]
            vconn.close()
        except:
            tokens_today = 0
            jobs_today = 0
        return {
            "total_sats": total,
            "today_sats": today,
            "pending_sats": pending,
            "withdrawn_sats": withdrawn,
            "tokens_today": tokens_today,
            "jobs_today": jobs_today,
            "payouts": []
        }
    except Exception:
        return {"total_sats": 0, "today_sats": 0, "pending_sats": 0, "withdrawn_sats": 0, "tokens_today": 0, "jobs_today": 0, "payouts": []}

@app.get("/api/status")
async def owlrun_status(request: Request):
    """Owlrun-compatible status endpoint with real data."""
    # Get Ollama models
    models = []
    try:
        resp = await client.get(f"{OLLAMA_URL}/api/tags")
        models = [m["name"] for m in resp.json().get("models", [])]
    except:
        pass

    gpu = get_gpu_info()
    disk = get_disk_info()
    earnings = get_earnings_data()
    threshold = int(get_setting("redeem_threshold", "100"))
    job_mode = get_setting("job_mode", "always")
    keep_warm = get_setting("keep_warm", "true") == "true"
    ctx_len = int(get_setting("context_length", "8192"))
    free_tier = int(get_setting("free_tier_pct", "0"))
    
    # Fetch live BTC price (cached for 60s)
    btc_data = json.loads(get_setting("btc_price_cache", '{"live":64000,"yesterday":64000,"avg24h":64000,"avg7d":64000}'))
    btc_updated = get_setting("btc_price_updated", "0")
    import time
    try:
        if time.time() - float(btc_updated) > 60:
            import urllib.request
            # Fetch current price
            req = urllib.request.Request('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_vol=true', headers={'User-Agent': 'VoltAI/1.0'})
            resp = urllib.request.urlopen(req, timeout=5)
            data = json.loads(resp.read())
            live = data['bitcoin']['usd']
            
            # Fetch 24h and 7d history for averages
            req2 = urllib.request.Request('https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=7', headers={'User-Agent': 'VoltAI/1.0'})
            resp2 = urllib.request.urlopen(req2, timeout=5)
            chart = json.loads(resp2.read())
            prices = [p[1] for p in chart.get('prices', [])]
            
            if len(prices) > 0:
                yesterday = prices[-24] if len(prices) >= 24 else prices[0]
                avg24h = sum(prices[-24:]) / min(24, len(prices))
                avg7d = sum(prices) / len(prices)
            else:
                yesterday = avg24h = avg7d = live
            
            btc_data = {"live": live, "yesterday": round(yesterday), "avg24h": round(avg24h), "avg7d": round(avg7d)}
            set_setting("btc_price_cache", json.dumps(btc_data))
            set_setting("btc_price_updated", str(time.time()))
    except Exception as e:
        pass
    btc_price = btc_data["live"]

    return {
        "node_id": "voltai-local",
        "provider_key": "voltai",
        "version": "1.0.0-voltai",
        "network": "production",
        "state": "earning",
        "job_mode": job_mode,
        "wallet": {
            "address": LN_ADDRESS,
            "configured": "Lightning payouts active"
        },
        "gpu": gpu,
        "model": get_setting("active_model", "qwen2.5:14b"),
        "models": models,
        "model_pricing": {"per_m_input_usd": 0, "per_m_output_usd": 0},
        "all_model_pricing": {},
        "earnings": {"today_usd": earnings["today_sats"] * btc_price / 100_000_000, "total_usd": earnings["total_sats"] * btc_price / 100_000_000},
        "gateway": {
            "connected": True,
            "status": "voltai",
            "jobs_today": earnings["jobs_today"],
            "tokens_today": earnings["tokens_today"],
            "earned_today_usd": earnings["today_sats"] * btc_price / 100_000_000,
            "earned_today_sats": earnings["today_sats"] * 1000,
            "earned_total_sats": earnings["total_sats"] * 1000,
            "queue_depth_global": 0
        },
        "disk": disk,
        "available_models": [{"tag": m, "vram_gb": 0, "installed": True, "active": m == get_setting("active_model", "qwen2.5:14b"), "fits": True} for m in models],
        "pulling": False,
        "context_length": ctx_len,
        "keep_warm": keep_warm,
        "free_tier_pct": free_tier,
        "karma_score": earnings.get("jobs_today", 0) + earnings.get("total_sats", 0) // 10,
        "karma_tier": "diamond" if (earnings.get("jobs_today", 0) + earnings.get("total_sats", 0) // 10) >= 100 else "gold" if (earnings.get("jobs_today", 0) + earnings.get("total_sats", 0) // 10) >= 50 else "silver" if (earnings.get("jobs_today", 0) + earnings.get("total_sats", 0) // 10) >= 10 else "bronze" if (earnings.get("jobs_today", 0) + earnings.get("total_sats", 0) // 10) > 0 else "none",
        "free_tier_jobs": earnings.get("jobs_today", 0) if free_tier > 0 else 0,
        "lightning_address": LN_ADDRESS,
        "redeem_threshold": threshold,
        "btc_price": {"live_usd": btc_data["live"], "yesterday_fix": btc_data["yesterday"], "daily_avg": btc_data["avg24h"], "weekly_avg": btc_data["avg7d"], "status": "live"},
        "broadcasts": [{"title": "VoltAI Gateway", "message": "Earnings auto-sent to your Lightning wallet. No action needed.", "severity": "info", "timestamp": "now"}],
        "sats_wallet": {
            "gateway_sats": earnings["pending_sats"] * 1000,
            "local_sats": 0,
            "total_sats": earnings["pending_sats"] * 1000,
            "usd_approx": earnings["pending_sats"] * btc_price / 100_000_000,
            "proof_count": 0,
            "last_claim": "",
            "last_token": "",
            "token_history": [],
            "withdraw_history": [{"amount_sats": p["amount_sats"], "payment_hash": "", "timestamp": p["created_at"]} for p in earnings["payouts"]]
        }
    }

@app.get("/api/history")
async def owlrun_history(period: str = "24h"):
    """Real usage history from usage_log."""
    # Get BTC price for USD conversion
    try:
        btc_data = json.loads(get_setting("btc_price_cache", '{"live":64000}'))
        btc_usd = btc_data.get("live", 64000)
    except:
        btc_usd = 64000
    
    with get_db() as db:
        rows = db.execute(
            """SELECT date(created_at) as date, SUM(tokens_in+tokens_out) as tokens, 
                      SUM(cost_sats) as sats, COUNT(*) as requests
               FROM usage_log WHERE created_at>=datetime('now','-7 days')
               GROUP BY date(created_at) ORDER BY date"""
        ).fetchall()
    
    buckets = []
    for r in rows:
        r = dict(r)
        sats = r["sats"]
        # Convert sats to USD: 1 BTC = 100,000,000 sats
        earned_usd = (sats / 100_000_000) * btc_usd
        buckets.append({
            "label": r["date"],
            "jobs": r["requests"],
            "earned": earned_usd,
            "tokens": r["tokens"],
            "sats": sats
        })
    return {"period": period, "buckets": buckets}

@app.post("/api/claim-ecash")
async def owlrun_claim():
    return {"error": "ecash claims handled by VoltAI gateway"}

@app.post("/api/set-lightning-address")
async def owlrun_set_ln(request: Request):
    data = await request.json()
    addr = data.get("address", LN_ADDRESS)
    set_setting("lightning_address", addr)
    return {"status": "ok", "address": addr}

@app.post("/api/set-redeem-threshold")
async def owlrun_set_threshold(request: Request):
    data = await request.json()
    threshold = data.get("threshold", 100)
    set_setting("redeem_threshold", threshold)
    # Also update gateway's min payout
    try:
        async with httpx.AsyncClient() as client:
            await client.post(f"{GATEWAY_URL}/api/set-min-payout", json={"min_payout_sats": threshold}, timeout=5.0)
    except Exception:
        pass
    return {"status": "ok", "threshold": threshold}

@app.post("/api/switch-model")
async def owlrun_switch_model(request: Request):
    data = await request.json()
    model = data.get("model", "")
    set_setting("active_model", model)
    return {"status": "ok", "model": model}

@app.post("/api/pull-model")
async def owlrun_pull_model(request: Request):
    from fastapi.responses import StreamingResponse
    data = await request.json()
    model = data.get("model", "")
    async def gen():
        try:
            import subprocess
            proc = subprocess.Popen(["ollama", "pull", model], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in proc.stdout:
                yield f'data: {{"status":"pulling {model}"}}\n\n'
            proc.wait()
            yield f'data: {{"status":"done"}}\n\n'
        except:
            yield f'data: {{"status":"error pulling model"}}\n\n'
    return StreamingResponse(gen(), media_type="text/event-stream")

@app.post("/api/remove-model")
async def owlrun_remove_model(request: Request):
    data = await request.json()
    model = data.get("model", "")
    import subprocess
    try:
        subprocess.run(["ollama", "rm", model], timeout=30)
        return {"status": "ok", "model": model}
    except:
        return {"error": "failed to remove model"}

@app.post("/api/set-job-mode")
async def owlrun_set_job_mode(request: Request):
    data = await request.json()
    mode = data.get("mode", "always")
    set_setting("job_mode", mode)
    return {"status": "ok", "mode": mode}

@app.post("/api/set-context-length")
async def owlrun_set_ctx(request: Request):
    data = await request.json()
    ctx = data.get("context_length", 8192)
    set_setting("context_length", ctx)
    return {"status": "ok", "context_length": ctx}

@app.post("/api/set-free-tier")
async def owlrun_set_free_tier(request: Request):
    data = await request.json()
    pct = data.get("pct", 0)
    set_setting("free_tier_pct", pct)
    return {"status": "ok", "free_tier_pct": pct}

@app.post("/api/set-keep-warm")
async def owlrun_set_keep_warm(request: Request):
    data = await request.json()
    on = data.get("on", True)
    set_setting("keep_warm", str(on).lower())
    return {"status": "ok", "keep_warm": on}

@app.get("/api/model-size")
async def owlrun_model_size(model: str = ""):
    # Estimate from model name
    size_map = {"3b": 2000, "7b": 4500, "8b": 5000, "9b": 6000, "14b": 9000, "27b": 16000, "70b": 40000}
    for key, mb in size_map.items():
        if key in model.lower():
            return {"model": model, "size_mb": mb, "source": "estimate"}
    return {"model": model, "size_mb": 4000, "source": "estimate"}

# ─── Start ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    print(f"{SITE_NAME} running on {HOST}:{PORT}")
    print(f"Ollama: {OLLAMA_URL}")
    print(f"Wallet: {LN_ADDRESS}")
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")
