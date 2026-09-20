import tkinter as tk

from dashboard.sidebar import create_sidebar
from dashboard.dashboard_page import create_dashboard_page
from dashboard.vehicles_page import create_vehicles_page
from dashboard.drivers_page import create_drivers_page
from dashboard.alerts_page import create_alerts_page
from dashboard.statistics_page import create_statistics_page


# =====================================================
# Main Window
# =====================================================

window = tk.Tk()

window.title("Smart Vehicle Monitoring System")

window.geometry("1400x850")

window.configure(bg="#f4f6f9")

window.resizable(False, False)


# =====================================================
# Content Area
# =====================================================

content = tk.Frame(
    window,
    bg="white"
)

content.pack(
    side="right",
    fill="both",
    expand=True
)


current_page = None


# =====================================================
# Show Page
# =====================================================

def show_page(page_name):

    global current_page

    if current_page is not None:

        current_page.destroy()

    if page_name == "dashboard":

     current_page = create_dashboard_page(content)

    elif page_name == "vehicles":

     print("VEHICLES BUTTON CLICKED")

     current_page = create_vehicles_page(content)

    elif page_name == "drivers":

     current_page = create_drivers_page(content)

    elif page_name == "alerts":

     current_page = create_alerts_page(content)

    elif page_name == "statistics":

     current_page = create_statistics_page(content)

    else:

     current_page = tk.Frame(
        content,
        bg="white"
    )

    current_page.pack(
        fill="both",
        expand=True
    )


# =====================================================
# Sidebar
# =====================================================

sidebar = create_sidebar(
    window,
    show_page
)


# =====================================================
# First Page
# =====================================================

show_page("dashboard")


window.mainloop()