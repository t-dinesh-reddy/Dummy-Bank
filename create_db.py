import sqlite3
conn = sqlite3.connect('database.db')
conn.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    otp_secret TEXT NOT NULL
)
''')
conn.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT,
    receiver TEXT,
    amount REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
conn.close()
