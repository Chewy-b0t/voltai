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
                created_at  TEXT DEFAULT (datetime('now'))
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
            CREATE INDEX IF NOT EXISTS idx_err_time ON error_log(created_at DESC);
            CREATE INDEX IF NOT EXISTS idx_err_user ON error_log(user_id);
        """)

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

def sats_for_tokens(tokens: int, price: int = 50) -> int:
    return max(1, (tokens * price) // 1_000_000)

def tokens_for_sats(sats: int, price: int = 50) -> int:
    return (sats * 1_000_000) // price
