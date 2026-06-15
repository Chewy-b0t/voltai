"""Database layer for VoltAI — user accounts, credits, usage."""

import sqlite3, hashlib, secrets
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).parent / "voltai.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with get_db() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                email       TEXT UNIQUE,
                username    TEXT UNIQUE NOT NULL,
                pass_hash   TEXT NOT NULL,
                display     TEXT DEFAULT '',
                referral_code TEXT UNIQUE,
                referred_by INTEGER,
                karma       INTEGER DEFAULT 0,
                created_at  TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (referred_by) REFERENCES users(id)
            );
            CREATE TABLE IF NOT EXISTS api_keys (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                key_hash    TEXT UNIQUE NOT NULL,
                key_prefix  TEXT NOT NULL,
                name        TEXT DEFAULT 'Default',
                credits     INTEGER DEFAULT 0,
                total_used  INTEGER DEFAULT 0,
                created_at  TEXT DEFAULT (datetime('now')),
                last_used   TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            CREATE TABLE IF NOT EXISTS invoices (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                payment_hash TEXT UNIQUE NOT NULL,
                key_id      INTEGER NOT NULL,
                user_id     INTEGER NOT NULL,
                amount_sats INTEGER NOT NULL,
                tokens      INTEGER NOT NULL,
                lninvoice   TEXT,
                verify_url  TEXT,
                status      TEXT DEFAULT 'pending',
                created_at  TEXT DEFAULT (datetime('now')),
                paid_at     TEXT,
                FOREIGN KEY (key_id) REFERENCES api_keys(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            CREATE TABLE IF NOT EXISTS usage_log (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                key_id      INTEGER NOT NULL,
                model       TEXT,
                tokens_in   INTEGER DEFAULT 0,
                tokens_out  INTEGER DEFAULT 0,
                cost_sats   INTEGER DEFAULT 0,
                created_at  TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (key_id) REFERENCES api_keys(id)
            );
            CREATE TABLE IF NOT EXISTS sessions (
                token       TEXT PRIMARY KEY,
                user_id     INTEGER NOT NULL,
                created_at  TEXT DEFAULT (datetime('now')),
                expires_at  TEXT DEFAULT (datetime('now', '+7 days')),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            CREATE TABLE IF NOT EXISTS error_log (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER,
                api_key_id  INTEGER,
                endpoint    TEXT,
                method      TEXT,
                status_code INTEGER,
                error_type  TEXT,
                error_msg   TEXT,
                request_body TEXT,
                ip_address  TEXT,
                created_at  TEXT DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS settings (
                key         TEXT PRIMARY KEY,
                value       TEXT NOT NULL,
                updated_at  TEXT DEFAULT (datetime('now'))
            );
            CREATE INDEX IF NOT EXISTS idx_err_time ON error_log(created_at DESC);
            CREATE INDEX IF NOT EXISTS idx_err_user ON error_log(user_id);
        """)
        # Migration: add new columns to existing tables
        cols = [r[1] for r in db.execute("PRAGMA table_info(users)").fetchall()]
        if "referral_code" not in cols:
            db.execute("ALTER TABLE users ADD COLUMN referral_code TEXT")
        if "referred_by" not in cols:
            db.execute("ALTER TABLE users ADD COLUMN referred_by INTEGER")
        if "karma" not in cols:
            db.execute("ALTER TABLE users ADD COLUMN karma INTEGER DEFAULT 0")
        # Generate referral codes for users who don't have one
        rows = db.execute("SELECT id FROM users WHERE referral_code IS NULL").fetchall()
        for r in rows:
            db.execute("UPDATE users SET referral_code=? WHERE id=?", (generate_referral_code(), r["id"]))

def hash_pass(pw: str) -> str:
    salt = secrets.token_hex(16)
    h = hashlib.sha256((salt + pw).encode()).hexdigest()
    return f"{salt}:{h}"

def check_pass(pw: str, stored: str) -> bool:
    salt, h = stored.split(":")
    return hashlib.sha256((salt + pw).encode()).hexdigest() == h

def hash_key(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()

def generate_key() -> str:
    return "sk-" + secrets.token_hex(16)

def generate_referral_code() -> str:
    return "VTAI-" + secrets.token_hex(4).upper()

def karma_tier(karma: int) -> str:
    if karma >= 100: return "diamond"
    if karma >= 50: return "gold"
    if karma >= 10: return "silver"
    if karma > 0: return "bronze"
    return "none"

def sats_for_tokens(tokens: int, price: int = 50) -> int:
    return max(1, (tokens * price) // 1_000_000)

def tokens_for_sats(sats: int, price: int = 50) -> int:
    return (sats * 1_000_000) // price
