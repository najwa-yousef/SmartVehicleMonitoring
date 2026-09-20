import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = os.path.join(BASE_DIR, "vehicle_monitoring.db")


def get_dashboard_statistics():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # عدد المركبات
    cursor.execute("""
        SELECT COUNT(DISTINCT vehicle_id)
        FROM vehicle_data
    """)
    total_vehicles = cursor.fetchone()[0]

    # عدد السائقين
    cursor.execute("""
        SELECT COUNT(DISTINCT driver_id)
        FROM vehicle_data
    """)
    total_drivers = cursor.fetchone()[0]

    # عدد الرحلات
    cursor.execute("""
        SELECT COUNT(DISTINCT trip_id)
        FROM vehicle_data
    """)
    total_trips = cursor.fetchone()[0]

    # عدد التنبيهات
    cursor.execute("""
        SELECT COUNT(*)
        FROM alerts
    """)
    total_alerts = cursor.fetchone()[0]

    # متوسط السرعة
    cursor.execute("""
        SELECT AVG(speed)
        FROM vehicle_data
    """)
    average_speed = cursor.fetchone()[0]

    if average_speed is None:
        average_speed = 0

    conn.close()

    return {
        "total_vehicles": total_vehicles,
        "total_drivers": total_drivers,
        "total_trips": total_trips,
        "total_alerts": total_alerts,
        "average_speed": round(average_speed, 2)
    }

def get_speed_history(limit=30):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT speed
        FROM vehicle_data
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    speeds = [row[0] for row in rows]

    speeds.reverse()

    return speeds

def get_recent_vehicle_data(limit=10):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            vehicle_id,
            driver_id,
            trip_id,
            speed
        FROM vehicle_data
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return rows