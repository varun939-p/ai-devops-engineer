import sqlite3

conn = sqlite3.connect("logs.db")
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print("Tables:", tables)

rows = conn.execute("SELECT * FROM logs").fetchall()
print("Log Entries:", rows)
