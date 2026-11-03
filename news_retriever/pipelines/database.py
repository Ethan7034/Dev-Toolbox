import sqlite3
from datetime import datetime
import os

os.makedirs("data", exist_ok=True)
DB_PATH = "data/search_history.db"

def init_db():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            keyword TEXT NOT NULL,
            result_count INTEGER,
            search_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_search(username: str, keyword: str, result_count: int):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO search_logs (username, keyword, result_count, search_time)
        VALUES (?, ?, ?, ?)
    ''', (username, keyword, result_count, current_time))
    
    conn.commit()
    conn.close()

def get_user_history(username: str, limit: int = 5):
    """查询某个用户的最近搜索历史"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT keyword, result_count, search_time 
        FROM search_logs 
        WHERE username = ? 
        ORDER BY id DESC LIMIT ?
    ''', (username, limit))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

init_db()