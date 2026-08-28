import sqlite3
import pytest
from fastapi.testclient import TestClient
from main import app, init_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    init_db()
    conn = sqlite3.connect("auth.db", timeout=30)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("DELETE FROM users;")
    conn.commit()
    conn.close()
    yield