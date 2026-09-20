import tkinter as tk
from tkinter import ttk
import sqlite3
import os

from data.vehicles import VEHICLES


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DB_NAME = os.path.join(
    BASE_DIR,
    "vehicle_monitoring.db"
)


def get_vehicles():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            vehicle_id,
            driver_id,
            COUNT(*) AS records
        FROM vehicle_data
        GROUP BY vehicle_id, driver_id
        ORDER BY vehicle_id
    """)

    vehicles = cursor.fetchall()

    conn.close()

    return vehicles


def get_vehicle_model(vehicle_id):

    for vehicle in VEHICLES:

        if vehicle["vehicle_id"] == vehicle_id:
            return vehicle["model"]

    return "Unknown"


def create_vehicles_page(parent):

    page = tk.Frame(
        parent,
        bg="#f4f6f9"
    )

    # ======================================
    # Title
    # ======================================

    title = tk.Label(
        page,
        text="🚗 Vehicles",
        font=("Arial", 28, "bold"),
        bg="#f4f6f9"
    )

    title.pack(
        pady=(30, 20)
    )

    # ======================================
    # Table Container
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

    # ======================================
    # Table
    # ======================================

    columns = (
        "vehicle",
        "model",
        "driver",
        "records"
    )

    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=15
    )

    table.heading(
        "vehicle",
        text="Vehicle ID"
    )

    table.heading(
        "model",
        text="Model"
    )

    table.heading(
        "driver",
        text="Driver ID"
    )

    table.heading(
        "records",
        text="Records"
    )

    table.column(
        "vehicle",
        width=180,
        anchor="center"
    )

    table.column(
        "model",
        width=300,
        anchor="center"
    )

    table.column(
        "driver",
        width=180,
        anchor="center"
    )

    table.column(
        "records",
        width=150,
        anchor="center"
    )

    # ======================================
    # Load Data
    # ======================================

    vehicles = get_vehicles()

    for vehicle_id, driver_id, records in vehicles:

        model = get_vehicle_model(vehicle_id)

        table.insert(
            "",
            "end",
            values=(
                vehicle_id,
                model,
                driver_id,
                records
            )
        )

    table.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    return page