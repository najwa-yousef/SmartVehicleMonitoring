import tkinter as tk


def create_statistics_page(parent):

    page = tk.Frame(
        parent,
        bg="white"
    )

    title = tk.Label(
        page,
        text="📊 Statistics",
        font=("Arial", 24, "bold"),
        bg="white"
    )

    title.pack(
        pady=30
    )

    message = tk.Label(
        page,
        text="Statistics and charts will appear here",
        font=("Arial", 14),
        bg="white"
    )

    message.pack()

    return page