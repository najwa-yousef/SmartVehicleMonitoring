import sqlite3

conn = sqlite3.connect("vehicle_monitoring.db")

cursor = conn.cursor()

cursor.execute("SELECT * FROM alerts")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()