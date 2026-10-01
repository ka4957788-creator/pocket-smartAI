import sqlite3
from pathlib import Path
from contextlib import contextmanager
from .config import get_settings
s=get_settings(); Path(s.database_path).parent.mkdir(parents=True,exist_ok=True)
SCHEMA='''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,email TEXT UNIQUE NOT NULL,password_hash TEXT NOT NULL,created_at TEXT DEFAULT CURRENT_TIMESTAMP);CREATE TABLE IF NOT EXISTS recommendations(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,planner_type TEXT NOT NULL,input_json TEXT NOT NULL,result_json TEXT NOT NULL,created_at TEXT DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE);'''
@contextmanager
def get_db():
    c=sqlite3.connect(s.database_path); c.row_factory=sqlite3.Row; c.execute('PRAGMA foreign_keys=ON')
    try: yield c; c.commit()
    finally: c.close()
def init_db():
    with get_db() as c:c.executescript(SCHEMA)
