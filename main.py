"""
Main entry point for Car Rental System
A Python + Tkinter application for managing car rentals with Oracle Database
"""

import tkinter as tk
from ui.login_window import LoginWindow
from ui.registration_window import RegistrationWindow
from ui.customer_window import CustomerWindow
from ui.agent_window import AgentWindow
import config


class CarRentalApp:
    """
    Main application class that coordinates all windows
    """
    
    def __init__(self):
        """Initialize the application"""
        self.root = tk.Tk()
        self.root.title(config.APP_TITLE)
        self.root.geometry(config.APP_GEOMETRY)
        
        # Start with login window
        self.show_login()
    
    def show_login(self):
        """Display login window"""
        login_window = LoginWindow(
            self.root,
            on_customer_login=self.on_customer_login,
            on_agent_login=self.on_agent_login,
            on_register_click=self.show_registration
        )
    
    def show_registration(self):
        """Display registration window"""
        registration_window = RegistrationWindow(
            self.root,
            on_registration_success=self.show_login
        )
    
    def on_customer_login(self, username):
        """Handle successful customer login"""
        # Create new root window for customer
        customer_root = tk.Tk()
        customer_app = CustomerWindow(customer_root, username)
        customer_root.mainloop()
    
    def on_agent_login(self, agent_id):
        """Handle successful agent login"""
        # Create new root window for agent
        agent_root = tk.Tk()
        agent_app = AgentWindow(agent_root, agent_id)
        agent_root.mainloop()
    
    def run(self):
        """Start the application main loop"""
        self.root.mainloop()


def main():
    """Main entry point"""
    app = CarRentalApp()
    app.run()


if __name__ == "__main__":
    main()

