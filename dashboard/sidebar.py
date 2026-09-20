import tkinter as tk


def create_sidebar(parent, show_page):

    sidebar = tk.Frame(
        parent,
        bg="#1f2937",
        width=250
    )

    sidebar.pack(
        side="left",
        fill="y"
    )

    sidebar.pack_propagate(False)

    # -------------------------
    # Logo
    # -------------------------

    logo = tk.Label(
        sidebar,
        text="🚗\nVehicle Monitor",
        bg="#1f2937",
        fg="white",
        font=("Arial", 18, "bold"),
        justify="center"
    )

    logo.pack(pady=30)

    # -------------------------
    # Buttons
    # -------------------------

    buttons = [
        ("🏠 Dashboard", "dashboard"),
        ("🚗 Vehicles", "vehicles"),
        ("👤 Drivers", "drivers"),
        ("🚨 Alerts", "alerts"),
        ("📊 Statistics", "statistics"),
        ("🚪 Exit", "exit")
    ]

    for text, page_name in buttons:

        if page_name == "exit":
            command = parent.destroy
        else:
            command = lambda p=page_name: show_page(p)

        button = tk.Button(
            sidebar,
            text=text,
            font=("Arial", 12),
            bg="#374151",
            fg="white",
            relief="flat",
            activebackground="#2563eb",
            activeforeground="white",
            width=20,
            height=2,
            cursor="hand2",
            command=command
        )

        button.pack(pady=5)

    return sidebar