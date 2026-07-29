import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_NAME = os.path.join(BASE_DIR, "vehicle_monitoring.db")

def create_database():
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vehicle_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id TEXT,
    driver_id TEXT,
    trip_id TEXT,
    timestamp TEXT,
    speed INTEGER,
    latitude REAL,
    longitude REAL
)
""")
    
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    speed INTEGER,
    message TEXT
)
""")

    conn.commit()
    conn.close()

def insert_vehicle_data(
    vehicle_id,
    driver_id,
    trip_id,
    timestamp,
    speed,
    latitude,
    longitude
):
    conn = sqlite3.connect(DB_NAME)
    

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO vehicle_data
    (vehicle_id, driver_id, trip_id, timestamp, speed, latitude, longitude)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
    vehicle_id,
    driver_id,
    trip_id,
    timestamp,
    speed,
    latitude,
    longitude
   ))
        
    conn.commit()
    conn.close()
    
def insert_alert(timestamp, speed, message):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO alerts
    (timestamp, speed, message)
    VALUES (?, ?, ?)
    """, (timestamp, speed, message))

    conn.commit()
    conn.close()

class DatabaseManager:

    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()

    def insert_vehicle_data(
       self,
       vehicle_id,
       driver_id,
       timestamp,
       speed,
       latitude,
       longitude
    ):
        
      self.cursor.execute("""
      INSERT INTO vehicle_data
      (vehicle_id, driver_id, timestamp, speed, latitude, longitude)
      VALUES (?, ?, ?, ?, ?, ?)
      """, (
          vehicle_id,
          driver_id,
          timestamp,
          speed,
          latitude,
          longitude
        ))    

    def close(self):
        self.conn.commit()
        self.conn.close()    