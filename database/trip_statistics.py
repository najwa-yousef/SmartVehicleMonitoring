import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = os.path.join(BASE_DIR, "vehicle_monitoring.db")

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("""
               
SELECT
    trip_id,
    vehicle_id,
    driver_id,
    COUNT(*) AS total_records,
    AVG(speed) AS average_speed,
    MAX(speed) AS maximum_speed
FROM vehicle_data
GROUP BY trip_id, vehicle_id, driver_id
""")

rows = cursor.fetchall()

print("===== Trip Statistics =====")

for row in rows:
    print(f"Trip ID       : {row[0]}")
    print(f"Vehicle ID    : {row[1]}")
    print(f"Driver ID     : {row[2]}")
    print(f"Records       : {row[3]}")
    print(f"Average Speed : {row[4]:.2f} km/h")
    print(f"Maximum Speed : {row[5]} km/h")
    print("-" * 35)

conn.close()