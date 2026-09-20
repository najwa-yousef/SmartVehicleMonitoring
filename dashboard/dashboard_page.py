import tkinter as tk
from tkinter import ttk
import sqlite3
import os

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from dashboard.dashboard_data import get_dashboard_statistics

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = os.path.join(BASE_DIR, "vehicle_monitoring.db")


def create_card(parent, title, value):

    card = tk.Frame(
        parent,
        bg="white",
        bd=1,
        relief="solid",
        width=180,
        height=110
    )

    card.pack_propagate(False)

    title_label = tk.Label(
        card,
        text=title,
        font=("Arial", 12, "bold"),
        bg="white"
    )
    title_label.pack(pady=(15, 5))

    value_label = tk.Label(
        card,
        text=str(value),
        font=("Arial", 24, "bold"),
        fg="#2563eb",
        bg="white"
    )
    value_label.pack()

    return card


def get_speed_history():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT speed
        FROM vehicle_data
        ORDER BY id DESC
        LIMIT 20
    """)

    speeds = [row[0] for row in cursor.fetchall()]

    conn.close()

    speeds.reverse()

    return speeds


def get_recent_records():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT vehicle_id, driver_id, trip_id, speed
        FROM vehicle_data
        ORDER BY id DESC
        LIMIT 10
    """)

    records = cursor.fetchall()

    conn.close()

    return records


def create_dashboard_page(parent):

    page = tk.Frame(
        parent,
        bg="#f4f6f9"
    )

    # ==========================================
    # Dashboard Content
    # ==========================================

    def load_dashboard():

        # إزالة المحتوى القديم
        for widget in page.winfo_children():
            widget.destroy()

        # الحصول على البيانات الجديدة
        stats = get_dashboard_statistics()

        # ======================================
        # Header
        # ======================================

        header = tk.Frame(
            page,
            bg="#f4f6f9"
        )

        header.pack(
            fill="x",
            padx=40,
            pady=(20, 5)
        )

        title = tk.Label(
            header,
            text="Dashboard",
            font=("Arial", 24, "bold"),
            bg="#f4f6f9"
        )

        title.pack(
            side="left"
        )

        refresh_button = tk.Button(
            header,
            text="🔄 Refresh",
            font=("Arial", 11, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7,
            command=lambda: load_dashboard()
        )

        refresh_button.pack(
            side="right"
        )

        # ======================================
        # Cards
        # ======================================

        cards_frame = tk.Frame(
            page,
            bg="#f4f6f9"
        )

        cards_frame.pack(
            pady=20
        )

        create_card(
            cards_frame,
            "🚗 Vehicles",
            stats["total_vehicles"]
        ).grid(
            row=0,
            column=0,
            padx=15
        )

        create_card(
            cards_frame,
            "👤 Drivers",
            stats["total_drivers"]
        ).grid(
            row=0,
            column=1,
            padx=15
        )

        create_card(
            cards_frame,
            "🛣 Trips",
            stats["total_trips"]
        ).grid(
            row=0,
            column=2,
            padx=15
        )

        create_card(
            cards_frame,
            "🚨 Alerts",
            stats["total_alerts"]
        ).grid(
            row=0,
            column=3,
            padx=15
        )

        # ======================================
        # Average Speed
        # ======================================

        speed = tk.Label(
            page,
            text=f"Average Speed : {stats['average_speed']} km/h",
            font=("Arial", 16, "bold"),
            bg="#f4f6f9"
        )

        speed.pack(
            pady=10
        )

        # ======================================
        # Speed History Chart
        # ======================================

        chart_frame = tk.Frame(
            page,
            bg="white",
            bd=1,
            relief="solid"
        )

        chart_frame.pack(
            fill="x",
            expand=False,
            padx=40,
            pady=15
        )

        speeds = get_speed_history()

        figure = Figure(
            figsize=(10, 3),
            dpi=100
        )

        ax = figure.add_subplot(111)

        if speeds:

            x = list(range(1, len(speeds) + 1))

            ax.plot(
                x,
                speeds,
                marker="o"
            )

            ax.set_title(
                "Vehicle Speed History"
            )

            ax.set_xlabel(
                "Record"
            )

            ax.set_ylabel(
                "Speed (km/h)"
            )

            ax.grid(
                True,
                alpha=0.3
            )

        else:

            ax.text(
                0.5,
                0.5,
                "No speed data available",
                ha="center",
                va="center"
            )

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(
            figure,
            master=chart_frame
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="x",
            expand=False
        )

        # ======================================
        # Recent Vehicle Records
        # ======================================

        table_title = tk.Label(
            page,
            text="Recent Vehicle Records",
            font=("Arial", 18, "bold"),
            bg="#f4f6f9"
        )

        table_title.pack(
            pady=(10, 5)
        )

        table_frame = tk.Frame(
            page,
            bg="white"
        )

        table_frame.pack(
            fill="x",
            padx=40,
            pady=(0, 20)
        )

        columns = (
            "vehicle",
            "driver",
            "trip",
            "speed",
            "status"
        )

        table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=6
        )

        table.heading(
            "vehicle",
            text="Vehicle"
        )

        table.heading(
            "driver",
            text="Driver"
        )

        table.heading(
            "trip",
            text="Trip"
        )

        table.heading(
            "speed",
            text="Speed (km/h)"
        )

        table.heading(
            "status",
            text="Status"
        )

        table.column(
            "vehicle",
            width=150,
            anchor="center"
        )

        table.column(
            "driver",
            width=150,
            anchor="center"
        )

        table.column(
            "trip",
            width=180,
            anchor="center"
        )

        table.column(
            "speed",
            width=150,
            anchor="center"
        )

        table.column(
            "status",
            width=150,
            anchor="center"
        )

        records = get_recent_records()

        for vehicle_id, driver_id, trip_id, speed_value in records:

            if speed_value > 100:
                status = "⚠ Alert"
            else:
                status = "Normal"

            table.insert(
                "",
                "end",
                values=(
                    vehicle_id,
                    driver_id,
                    trip_id,
                    speed_value,
                    status
                )
            )

        table.pack(
            fill="x",
            expand=True
        )

    # تحميل Dashboard أول مرة
    load_dashboard()

    return page