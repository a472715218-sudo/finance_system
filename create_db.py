import sqlite3

conn = sqlite3.connect("finance.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS income(
id INTEGER PRIMARY KEY AUTOINCREMENT,
amount REAL,
date TEXT,
note TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS expense(
id INTEGER PRIMARY KEY AUTOINCREMENT,
amount REAL,
date TEXT,
note TEXT
)
""")

conn.commit()
conn.close()

print("数据库创建完成")