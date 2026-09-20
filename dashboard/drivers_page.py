import tkinter as tk
from tkinter import ttk
import sqlite3
import os

from data.drivers import DRIVERS


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DB_NAME = os.path.join(
    BASE_DIR,
    "vehicle_monitoring.db"
)


def get_driver_records():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            driver_id,
            COUNT(*) AS records,
            AVG(speed) AS average_speed
        FROM vehicle_data
        GROUP BY driver_id
        ORDER BY driver_id
    """)

    records = cursor.fetchall()

    conn.close()

    return records


def get_driver_name(driver_id):

    for driver in DRIVERS:

        if driver["driver_id"] == driver_id:
            return driver["name"]

    return "Unknown"


def get_driving_style(driver_id):

    for driver in DRIVERS:

        if driver["driver_id"] == driver_id:
            return driver["driving_style"]

    return "Unknown"


def create_drivers_page(parent):

    page = tk.Frame(
        parent,
        bg="#f4f6f9"
    )

    # ======================================
    # Title
    # ======================================

    title = tk.Label(
        page,
        text="👤 Drivers",
        font=("Arial", 28, "bold"),
        bg="#f4f6f9"
    )

    title.pack(
        pady=(30, 20)
    )

    # ======================================
    # Table
    # ======================================

    table_frame = tk.Frame(
        page,
        bg="white"
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=40,
        pady=(0, 30)
    )

    columns = (
        "id",
        "name",
        "style",
        "records",
        "average"
    )

    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=15
    )

    table.heading(
        "id",
        text="Driver ID"
    )

    table.heading(
        "name",
        text="Name"
    )

    table.heading(
        "style",
        text="Driving Style"
    )

    table.heading(
        "records",
        text="Records"
    )

    table.heading(
        "average",
        text="Average Speed"
    )

    table.column(
        "id",
        width=150,
        anchor="center"
    )

    table.column(
        "name",
        width=200,
        anchor="center"
    )

    table.column(
        "style",
        width=200,
        anchor="center"
    )

    table.column(
        "records",
        width=150,
        anchor="center"
    )

    table.column(
        "average",
        width=180,
        anchor="center"
    )

    # ======================================
    # Load Data
    # ======================================

    records = get_driver_records()

    for driver_id, total_records, average_speed in records:

        name = get_driver_name(driver_id)

        style = get_driving_style(driver_id)

        average_speed = round(
            average_speed,
            2
        )

        table.insert(
            "",
            "end",
            values=(
                driver_id,
                name,
                style,
                total_records,
                f"{average_speed} km/h"
            )
        )

    table.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    return page