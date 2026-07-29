import random
from datetime import datetime

from data.drivers import DRIVERS
from data.vehicles import VEHICLES

from database.database_manager import (
    create_database,
    insert_vehicle_data,
    insert_alert
)

from alerts.speed_alert import check_speed


def generate_car_data(vehicle, trip_id):

    driver_id = vehicle["driver_id"]

    driver = next(
        driver for driver in DRIVERS
        if driver["driver_id"] == driver_id
    )

    if driver["driving_style"] == "safe":
        speed = random.randint(40, 90)

    elif driver["driving_style"] == "normal":
        speed = random.randint(60, 110)

    elif driver["driving_style"] == "aggressive":
        speed = random.randint(90, 140)

    else:   # expert
        speed = random.randint(50, 100)

    return {
        "vehicle_id": vehicle["vehicle_id"],
        "vehicle_model": vehicle["model"],
        "driver_id": driver_id,
        "trip_id": trip_id,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "speed": speed,
        "latitude": round(random.uniform(15.30, 15.40), 6),
        "longitude": round(random.uniform(44.15, 44.25), 6)
    }


if __name__ == "__main__":

    create_database()

    print("Simulation Started...")

    TOTAL_RECORDS = 10

    alert_count = 0

    records_per_vehicle = TOTAL_RECORDS // len(VEHICLES)

    for vehicle in VEHICLES:

        trip_id = f"TRIP{random.randint(1000, 9999)}"

        for _ in range(records_per_vehicle):

            car_data = generate_car_data(vehicle, trip_id)

            print(
                f"Vehicle: {car_data['vehicle_id']} "
                f"({car_data['vehicle_model']}) | "
                f"Driver: {car_data['driver_id']} | "
                f"Speed: {car_data['speed']} km/h"
            )

            insert_vehicle_data(
                car_data["vehicle_id"],
                car_data["driver_id"],
                car_data["trip_id"],
                car_data["timestamp"],
                car_data["speed"],
                car_data["latitude"],
                car_data["longitude"]
            )

            alert = check_speed(car_data["speed"])

            if alert:

                alert_count += 1

                insert_alert(
                    car_data["timestamp"],
                    car_data["speed"],
                    alert
                )

    print("Simulation Completed Successfully.")
    print(f"{TOTAL_RECORDS} records generated.")
    print(f"{alert_count} alerts generated.")
    print("Simulation Completed.")