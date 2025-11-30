"""
Registration Window for Car Rental System
Handles new user registration (Customer and Agent)
"""

import tkinter as tk
from tkinter import messagebox, StringVar
import random
from database.db_operations import DatabaseOperations


class RegistrationWindow:
    """
    Registration window for new customer and agent signup
    """
    
    def __init__(self, parent_window, on_registration_success):
        """
        Initialize registration window
        
        Args:
            parent_window: Parent Tkinter window
            on_registration_success: Callback function after successful registration
        """
        self.parent = parent_window
        self.on_registration_success = on_registration_success
        
        self.window = tk.Toplevel(parent_window)
        self.window.title("Registration")
        self.window.geometry("400x300")
        
        self.db = DatabaseOperations()
        self.db.connect()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create and place UI widgets"""
        # Username
        self.label_username = tk.Label(self.window, text="Username:")
        self.label_username.grid(row=0, column=0, pady=5)
        
        self.entry_username = tk.Entry(self.window, width=20)
        self.entry_username.grid(row=0, column=1, pady=5)
        
        # Password
        self.label_password = tk.Label(self.window, text="Password:")
        self.label_password.grid(row=1, column=0, pady=5)
        
        self.entry_password = tk.Entry(self.window, show="*", width=20)
        self.entry_password.grid(row=1, column=1, pady=5)
        
        # Category selection
        self.label_category = tk.Label(self.window, text="Category:")
        self.label_category.grid(row=2, column=0, pady=5)
        
        self.category_var = StringVar(self.window)
        self.category_var.set("customer")
        self.category_menu = tk.OptionMenu(self.window, self.category_var, "customer", "agent")
        self.category_menu.grid(row=2, column=1, pady=5)
        
        # Register button
        self.register_button = tk.Button(
            self.window, 
            text="Register", 
            command=self.on_register,
            bg="#4CAF50"
        )
        self.register_button.grid(row=3, column=0, columnspan=2, pady=10)
    
    def on_register(self):
        """Handle registration button click"""
        username = self.entry_username.get()
        password = self.entry_password.get()
        category = self.category_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required.")
            return
        
        if category == 'customer':
            customer_id = random.randint(100000, 999999)
            success = self.db.register_customer(customer_id, username, password)
            
            if success:
                messagebox.showinfo("Registration", "Customer registered successfully!")
                self.db.disconnect()
                self.window.destroy()
                if self.on_registration_success:
                    self.on_registration_success()
            else:
                messagebox.showerror("Error", "Registration failed. Please try again.")
        
        elif category == 'agent':
            agent_id = random.randint(100000, 999999)
            success = self.db.register_agent(agent_id, username, password)
            
            if success:
                messagebox.showinfo("Registration", "Agent registered successfully!")
                self.db.disconnect()
                self.window.destroy()
                if self.on_registration_success:
                    self.on_registration_success()
            else:
                messagebox.showerror("Error", "Registration failed. Please try again.")

