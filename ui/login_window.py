"""
Login Window for Car Rental System
Handles user authentication (Customer and Agent)
"""

import tkinter as tk
from tkinter import messagebox, StringVar
from database.db_operations import DatabaseOperations


class LoginWindow:
    """
    Login window for customer and agent authentication
    """
    
    # UI Style constants
    COMMON_STYLE = {
        'font': ('Calibri', 16),
        'padx': 10,
        'pady': 10,
    }
    
    BUTTON_STYLE = {
        'font': ('Calibri', 16, 'bold'),
        'width': 15,
        'fg': 'white',
    }
    
    ENTRY_STYLE = {
        'font': ('Calibri', 16),
        'width': 30,
    }
    
    def __init__(self, root, on_customer_login, on_agent_login, on_register_click):
        """
        Initialize login window
        
        Args:
            root: Tkinter root window
            on_customer_login: Callback function for customer login
            on_agent_login: Callback function for agent login
            on_register_click: Callback function for registration button
        """
        self.root = root
        self.root.title("Car Rental System - Login")
        self.root.geometry("400x300")
        
        self.on_customer_login = on_customer_login
        self.on_agent_login = on_agent_login
        self.on_register_click = on_register_click
        
        self.db = DatabaseOperations()
        self.db.connect()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create and place UI widgets"""
        # Username
        self.label_username = tk.Label(self.root, text="Username:", **self.COMMON_STYLE)
        self.label_username.grid(row=0, column=0, pady=5)
        
        self.entry_username = tk.Entry(self.root, **self.ENTRY_STYLE)
        self.entry_username.grid(row=0, column=1, pady=5)
        
        # Password
        self.label_password = tk.Label(self.root, text="Password:", **self.COMMON_STYLE)
        self.label_password.grid(row=1, column=0, pady=5)
        
        self.entry_password = tk.Entry(self.root, show="*", **self.ENTRY_STYLE)
        self.entry_password.grid(row=1, column=1, pady=5)
        
        # User type selection
        self.user_type_label = tk.Label(self.root, text="Login As:", **self.COMMON_STYLE)
        self.user_type_label.grid(row=2, column=0, pady=5)
        
        self.user_type_var = StringVar(self.root)
        self.user_type_var.set("customer")
        self.user_type_menu = tk.OptionMenu(self.root, self.user_type_var, "customer", "agent")
        self.user_type_menu.config(**self.ENTRY_STYLE)
        self.user_type_menu.grid(row=2, column=1, pady=5)
        
        # Login button
        self.login_button = tk.Button(
            self.root, 
            text="Login", 
            command=self.on_login, 
            bg="#4CAF50",
            **self.BUTTON_STYLE
        )
        self.login_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Register button
        self.register_button = tk.Button(
            self.root, 
            text="Register", 
            command=self.on_register_click, 
            bg="#3498db",
            **self.BUTTON_STYLE
        )
        self.register_button.grid(row=4, column=0, columnspan=2, pady=10)
    
    def on_login(self):
        """Handle login button click"""
        username = self.entry_username.get()
        password = self.entry_password.get()
        user_type = self.user_type_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return
        
        if user_type == 'customer':
            self._login_customer(username, password)
        elif user_type == 'agent':
            self._login_agent(username, password)
    
    def _login_customer(self, username, password):
        """Authenticate and login customer"""
        customer = self.db.login_customer(username, password)
        
        if customer:
            self.db.disconnect()
            self.root.destroy()
            self.on_customer_login(username)
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def _login_agent(self, username, password):
        """Authenticate and login agent"""
        agent = self.db.login_agent(username, password)
        
        if agent:
            agent_id = agent[0]
            self.db.disconnect()
            self.root.destroy()
            self.on_agent_login(agent_id)
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def cleanup(self):
        """Clean up resources"""
        if self.db:
            self.db.disconnect()

