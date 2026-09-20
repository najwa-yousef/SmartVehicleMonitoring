import tkinter as tk
from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from dashboard.dashboard_data import (
    get_dashboard_statistics,
    get_speed_history,
    get_recent_vehicle_data
)


# ==========================================================
# Main Window
# ==========================================================

window = tk.Tk()

window.title("Smart Vehicle Monitoring Dashboard")

window.geometry("1000x760")

window.configure(bg="#f4f6f9")

window.resizable(False, False)


# ==========================================================
# Dashboard Title
# ==========================================================

title = tk.Label(
    window,
    text="Smart Vehicle Monitoring Dashboard",
    font=("Arial", 20, "bold"),
    bg="#f4f6f9",
    fg="#1f2937"
)

title.pack(pady=15)


# ==========================================================
# Cards Frame
# ==========================================================

cards_frame = tk.Frame(
    window,
    bg="#f4f6f9"
)

cards_frame.pack(pady=10)


value_labels = {}


def create_card(title, key, row, column):

    frame = tk.Frame(
        cards_frame,
        bg="white",
        width=200,
        height=100,
        relief="raised",
        bd=2
    )

    frame.grid(
        row=row,
        column=column,
        padx=15,
        pady=15
    )

    frame.grid_propagate(False)

    title_label = tk.Label(
        frame,
        text=title,
        font=("Arial", 12, "bold"),
        bg="white"
    )

    title_label.pack(pady=(12, 5))

    value_label = tk.Label(
        frame,
        text="0",
        font=("Arial", 24, "bold"),
        fg="#2563eb",
        bg="white"
    )

    value_label.pack()

    value_labels[key] = value_label


create_card(
    "🚗 Vehicles",
    "total_vehicles",
    0,
    0
)

create_card(
    "👤 Drivers",
    "total_drivers",
    0,
    1
)

create_card(
    "🛣 Trips",
    "total_trips",
    1,
    0
)

create_card(
    "⚠ Alerts",
    "total_alerts",
    1,
    1
)


# ==========================================================
# Average Speed
# ==========================================================

average_speed_label = tk.Label(
    window,
    text="Average Speed : 0 km/h",
    font=("Arial", 14, "bold"),
    bg="#f4f6f9"
)

average_speed_label.pack(pady=10)


# ==========================================================
# Chart
# ==========================================================

chart_frame = tk.Frame(
    window,
    bg="#f4f6f9"
)

chart_frame.pack(
    fill="x",
    padx=20,
    pady=10
)

figure = Figure(
    figsize=(8.5, 3),
    dpi=100
)

axis = figure.add_subplot(111)

canvas = FigureCanvasTkAgg(
    figure,
    master=chart_frame
)

canvas.get_tk_widget().pack(
    fill="both",
    expand=True
)


# ==========================================================
# Recent Vehicle Data Table
# ==========================================================

table_frame = tk.Frame(
    window,
    bg="#f4f6f9"
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)

columns = (
    "Vehicle",
    "Driver",
    "Trip",
    "Speed",
    "Status"
)

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=10
)

table.heading("Vehicle", text="Vehicle")
table.heading("Driver", text="Driver")
table.heading("Trip", text="Trip")
table.heading("Speed", text="Speed")
table.heading("Status", text="Status")

table.column("Vehicle", width=120, anchor="center")
table.column("Driver", width=120, anchor="center")
table.column("Trip", width=180, anchor="center")
table.column("Speed", width=120, anchor="center")
table.column("Status", width=150, anchor="center")

table.pack(
    fill="both",
    expand=True
)


# ==========================================================
# Refresh Dashboard
# ==========================================================

def refresh_dashboard():

    stats = get_dashboard_statistics()

    value_labels["total_vehicles"].config(
        text=stats["total_vehicles"]
    )

    value_labels["total_drivers"].config(
        text=stats["total_drivers"]
    )

    value_labels["total_trips"].config(
        text=stats["total_trips"]
    )

    value_labels["total_alerts"].config(
        text=stats["total_alerts"]
    )

    average_speed_label.config(
        text=f"Average Speed : {stats['average_speed']} km/h"
    )


    # -----------------------------
    # Chart
    # -----------------------------

    speeds = get_speed_history()

    axis.clear()

    if speeds:

        axis.plot(
            range(1, len(speeds)+1),
            speeds,
            marker="o",
            linewidth=2
        )

    axis.set_title("Vehicle Speed History")

    axis.set_xlabel("Reading")

    axis.set_ylabel("Speed (km/h)")

    axis.grid(True)

    canvas.draw()


    # -----------------------------
    # Table
    # -----------------------------

    for item in table.get_children():

        table.delete(item)

    rows = get_recent_vehicle_data()

    for vehicle, driver, trip, speed in rows:

        if speed > 120:

            status = "Overspeed"

        else:

            status = "Normal"

        table.insert(
            "",
            tk.END,
            values=(
                vehicle,
                driver,
                trip,
                f"{speed} km/h",
                status
            )
        )

# ==========================================================
# Buttons
# ==========================================================

buttons_frame = tk.Frame(
    window,
    bg="#f4f6f9"
)

buttons_frame.pack(
    pady=15
)

refresh_button = tk.Button(
    buttons_frame,
    text="Refresh",
    width=15,
    bg="#2563eb",
    fg="white",
    font=("Arial", 11, "bold"),
    command=refresh_dashboard
)

refresh_button.grid(
    row=0,
    column=0,
    padx=10
)

exit_button = tk.Button(
    buttons_frame,
    text="Exit",
    width=15,
    bg="#dc2626",
    fg="white",
    font=("Arial", 11, "bold"),
    command=window.destroy
)

exit_button.grid(
    row=0,
    column=1,
    padx=10
)


# ==========================================================
# Initial Load
# ==========================================================

refresh_dashboard()


# ==========================================================
# Run Application
# ==========================================================

window.mainloop()        