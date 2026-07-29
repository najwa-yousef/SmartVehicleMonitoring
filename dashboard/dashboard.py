import tkinter as tk
import sqlite3

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from dashboard.dashboard_data import get_dashboard_statistics

# -----------------------------
# Get Dashboard Statistics
# -----------------------------
stats = get_dashboard_statistics()


# -----------------------------
# Main Window
# -----------------------------
window = tk.Tk()
window.title("Smart Vehicle Monitoring Dashboard")
window.geometry("700x500")
window.resizable(False, False)
window.configure(bg="#f4f6f9")


# -----------------------------
# Title
# -----------------------------
title = tk.Label(
    window,
    text="Smart Vehicle Monitoring Dashboard",
    font=("Arial", 20, "bold"),
    bg="#f4f6f9",
    fg="#1f2937"
)
title.pack(pady=20)


# -----------------------------
# Cards Frame
# -----------------------------
cards_frame = tk.Frame(
    window,
    bg="#f4f6f9"
)
cards_frame.pack(pady=10)


# -----------------------------
# Card Function
# -----------------------------
def create_card(parent, title_text, value):

    frame = tk.Frame(
        parent,
        bg="white",
        width=220,
        height=100,
        relief="raised",
        bd=2
    )

    frame.grid_propagate(False)

    title = tk.Label(
        frame,
        text=title_text,
        font=("Arial", 12, "bold"),
        bg="white"
    )

    title.pack(pady=(12, 5))

    number = tk.Label(
        frame,
        text=str(value),
        font=("Arial", 22, "bold"),
        bg="white",
        fg="#2563eb"
    )

    number.pack()

    return frame


# -----------------------------
# Create Cards
# -----------------------------
vehicle_card = create_card(
    cards_frame,
    "🚗 Vehicles",
    stats["total_vehicles"]
)

driver_card = create_card(
    cards_frame,
    "👤 Drivers",
    stats["total_drivers"]
)

trip_card = create_card(
    cards_frame,
    "🛣 Trips",
    stats["total_trips"]
)

alert_card = create_card(
    cards_frame,
    "⚠ Alerts",
    stats["total_alerts"]
)


vehicle_card.grid(row=0, column=0, padx=15, pady=15)
driver_card.grid(row=0, column=1, padx=15, pady=15)

trip_card.grid(row=1, column=0, padx=15, pady=15)
alert_card.grid(row=1, column=1, padx=15, pady=15)


# -----------------------------
# Average Speed
# -----------------------------
speed_label = tk.Label(
    window,
    text=f"Average Speed : {stats['average_speed']} km/h",
    font=("Arial", 14, "bold"),
    bg="#f4f6f9",
    fg="#111827"
)

speed_label.pack(pady=15)


# -----------------------------
# Buttons
# -----------------------------
button_frame = tk.Frame(
    window,
    bg="#f4f6f9"
)

button_frame.pack(pady=20)


def refresh_dashboard():

    new_stats = get_dashboard_statistics()

    vehicle_card.winfo_children()[1].config(
        text=str(new_stats["total_vehicles"])
    )

    driver_card.winfo_children()[1].config(
        text=str(new_stats["total_drivers"])
    )

    trip_card.winfo_children()[1].config(
        text=str(new_stats["total_trips"])
    )

    alert_card.winfo_children()[1].config(
        text=str(new_stats["total_alerts"])
    )

    speed_label.config(
        text=f"Average Speed : {new_stats['average_speed']} km/h"
    )


refresh_button = tk.Button(
    button_frame,
    text="Refresh",
    width=15,
    bg="#2563eb",
    fg="white",
    command=refresh_dashboard
)

refresh_button.grid(row=0, column=0, padx=10)


exit_button = tk.Button(
    button_frame,
    text="Exit",
    width=15,
    bg="#dc2626",
    fg="white",
    command=window.destroy
)

exit_button.grid(row=0, column=1, padx=10)


window.mainloop()