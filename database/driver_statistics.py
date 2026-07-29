import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = os.path.join(BASE_DIR, "vehicle_monitoring.db")

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("""
SELECT
    driver_id,
    COUNT(*) AS total_records,
    AVG(speed) AS average_speed,
    MAX(speed) AS max_speed,
    SUM(CASE
        WHEN speed > 100 THEN 1
        ELSE 0
    END) AS overspeed_records
FROM vehicle_data
GROUP BY driver_id
""")

rows = cursor.fetchall()

print("===== Driver Statistics =====")

for row in rows:
    print(f"Driver : {row[0]}")
    print(f"Records : {row[1]}")
    print(f"Average Speed : {row[2]:.2f} km/h")
    print(f"Maximum Speed : {row[3]} km/h")
    safety_score = max(0, 100 - (row[4] * 5))
    print(f"Overspeed Records : {row[4]}")
    print(f"Safety Score : {safety_score}/100")
    print("-" * 30)

conn.close()