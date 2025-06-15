import pymysql

conn = pymysql.connect(
    host='127.0.0.1',
    user='flask_user',
    password='Trust-Digital-Resilience',
    db='dummy_bank',
    cursorclass=pymysql.cursors.Cursor
)

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    otp_secret TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender VARCHAR(100),
    receiver VARCHAR(100),
    amount DECIMAL(10, 2),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()
