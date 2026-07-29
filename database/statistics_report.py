import sqlite3

conn = sqlite3.connect("vehicle_monitoring.db")

cursor = conn.cursor()

# عدد سجلات القيادة
cursor.execute("SELECT COUNT(*) FROM vehicle_data")
total_records = cursor.fetchone()[0]

# عدد المخالفات
cursor.execute("SELECT COUNT(*) FROM alerts")
total_alerts = cursor.fetchone()[0]

# أعلى سرعة
cursor.execute("SELECT MAX(speed) FROM vehicle_data")
max_speed = cursor.fetchone()[0]

# متوسط السرعة
cursor.execute("SELECT AVG(speed) FROM vehicle_data")
avg_speed = cursor.fetchone()[0]

print("===== Vehicle Statistics Report =====")
print(f"Total Records : {total_records}")
print(f"Total Alerts  : {total_alerts}")
print(f"Maximum Speed : {max_speed} km/h")
print(f"Average Speed : {avg_speed:.2f} km/h")

violation_percentage = (total_alerts / total_records) * 100

safety_score = max(0, 100 - violation_percentage)

print(f"Driver Safety Score : {safety_score:.2f}/100")

conn.close()