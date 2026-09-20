import tkinter as tk
from tkinter import ttk
import sqlite3
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DB_NAME = os.path.join(
    BASE_DIR,
    "vehicle_monitoring.db"
)


def get_alerts():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM alerts
        ORDER BY rowid DESC
    """)

    alerts = cursor.fetchall()

    conn.close()

    return alerts


def create_alerts_page(parent):

    page = tk.Frame(
        parent,
        bg="#f4f6f9"
    )

    title = tk.Label(
        page,
        text="🚨 Alerts",
        font=("Arial", 28, "bold"),
        bg="#f4f6f9"
    )

    title.pack(
        pady=(30, 20)
    )

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
        "timestamp",
        "speed",
        "alert"
    )

    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=15
    )

    table.heading(
        "id",
        text="ID"
    )

    table.heading(
        "timestamp",
        text="Timestamp"
    )

    table.heading(
        "speed",
        text="Speed"
    )

    table.heading(
        "alert",
        text="Alert"
    )

    table.column(
        "id",
        width=80,
        anchor="center"
    )

    table.column(
        "timestamp",
        width=250,
        anchor="center"
    )

    table.column(
        "speed",
        width=150,
        anchor="center"
    )

    table.column(
        "alert",
        width=350,
        anchor="center"
    )

    alerts = get_alerts()

    for alert in alerts:

        values = list(alert)

        table.insert(
            "",
            "end",
            values=values
        )

    table.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    return page