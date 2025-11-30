"""
Customer Window for Car Rental System
Handles customer interface for viewing and managing rentals
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from database.db_operations import DatabaseOperations


class CustomerWindow:
    """
    Customer home window for viewing rented cars and renting new ones
    """
    
    def __init__(self, root, username):
        """
        Initialize customer window
        
        Args:
            root: Tkinter root window
            username: Customer username
        """
        self.root = root
        self.username = username
        self.root.title(f"Welcome, {username}")
        
        self.db = DatabaseOperations()
        self.db.connect()
        
        self._display_home()
    
    def _display_home(self):
        """Display customer home page with rented cars"""
        # Check for overdue cars first
        overdue_cars = self.db.get_overdue_cars(self.username)
        
        if overdue_cars:
            self._display_overdue_cars(overdue_cars)
        else:
            self._display_normal_view()
    
    def _display_overdue_cars(self, overdue_cars):
        """Display overdue cars with warning"""
        overdue_info_label = tk.Label(
            self.root,
            text="⚠ Overdue Cars:",
            font=('Calibri', 16, 'bold'),
            fg='red',
            pady=10
        )
        overdue_info_label.grid(row=0, column=0, columnspan=3)
        
        for i, car in enumerate(overdue_cars):
            formatted_date = car[2].strftime('%Y-%m-%d') if car[2] else "N/A"
            
            overdue_car_label = tk.Label(
                self.root,
                text=f"CarID: {car[0]}, Model: {car[1]}, Due Date: {formatted_date}",
                font=('Calibri', 14),
                pady=5
            )
            overdue_car_label.grid(row=i + 1, column=0, columnspan=3)
            
            btn_return_car = tk.Button(
                self.root,
                text="Return Car (Overdue)",
                command=lambda car_id=car[0]: self.return_car(car_id),
                font=('Calibri', 16, 'bold'),
                width=20,
                fg='white',
                bg='#e74c3c'
            )
            btn_return_car.grid(row=i + 1, column=3, pady=5)
        
        # Disable renting if there are overdue cars
        btn_rent_car = tk.Button(
            self.root,
            text="Rent a Car (Disabled - Return overdue cars first)",
            state=tk.DISABLED,
            font=('Calibri', 16, 'bold'),
            width=30,
            fg='white',
            bg='#95a5a6'
        )
        btn_rent_car.grid(row=len(overdue_cars) + 1, column=0, columnspan=4, pady=10)
    
    def _display_normal_view(self):
        """Display normal view with rented cars"""
        rented_cars = self.db.get_customer_rented_cars(self.username)
        
        if rented_cars:
            for i, car in enumerate(rented_cars):
                formatted_end_date = car[3].strftime('%Y-%m-%d') if car[3] else "N/A"
                
                car_info_label = tk.Label(
                    self.root,
                    text=f"CarID: {car[0]}, Model: {car[1]}, Year: {car[2]}, End Date: {formatted_end_date}",
                    font=('Calibri', 14),
                    pady=5
                )
                car_info_label.grid(row=i, column=0, pady=5)
                
                btn_return_car = tk.Button(
                    self.root,
                    text="Return Car",
                    command=lambda car_id=car[0]: self.return_car(car_id),
                    font=('Calibri', 16, 'bold'),
                    width=15,
                    fg='white',
                    bg='#3498db'
                )
                btn_return_car.grid(row=i, column=2, pady=5)
            
            btn_rent_car = tk.Button(
                self.root,
                text="Rent a Car",
                command=self.rent_car,
                font=('Calibri', 16, 'bold'),
                width=15,
                fg='white',
                bg='#3498db'
            )
            btn_rent_car.grid(row=len(rented_cars), column=0, pady=5)
        else:
            label_no_cars = tk.Label(
                self.root,
                text="No cars are currently rented.",
                font=('Calibri', 14),
                pady=5
            )
            label_no_cars.grid(row=0, column=0, pady=5)
            
            btn_rent_car = tk.Button(
                self.root,
                text="Rent a Car",
                command=self.rent_car,
                font=('Calibri', 16, 'bold'),
                width=15,
                fg='white',
                bg='#3498db'
            )
            btn_rent_car.grid(row=1, column=0, pady=5)
    
    def return_car(self, car_id):
        """Handle car return"""
        success = self.db.return_car(car_id)
        
        if success:
            messagebox.showinfo("Car Returned", "Car returned successfully!")
            # Refresh the view
            for widget in self.root.winfo_children():
                widget.destroy()
            self._display_home()
        else:
            messagebox.showerror("Error", "Failed to return car. Please try again.")
    
    def rent_car(self):
        """Display available cars for rent"""
        available_cars = self.db.get_available_cars()
        
        if not available_cars:
            messagebox.showinfo("No Available Cars", "Sorry, there are no available cars at the moment.")
            return
        
        # Create new window for available cars
        available_window = tk.Toplevel(self.root)
        available_window.title("Available Cars for Rent")
        available_window.configure(bg='#ecf0f1')
        
        for i, car in enumerate(available_cars):
            car_info_label = tk.Label(
                available_window,
                text=f"CarID: {car[0]}, Model: {car[2]}, Year: {car[5]}, Tariff: {car[3]}",
                font=('Calibri', 14),
                pady=5,
                bg='#ecf0f1'
            )
            car_info_label.grid(row=i, column=0, pady=5, padx=10)
            
            rent_button = tk.Button(
                available_window,
                text="Rent",
                command=lambda car_id=car[0], price=car[3]: self.initiate_rental(car_id, price, available_window),
                font=('Calibri', 16, 'bold'),
                width=15,
                fg='white',
                bg='#3498db'
            )
            rent_button.grid(row=i, column=1, pady=5)
    
    def initiate_rental(self, car_id, price, parent_window):
        """Open rental form for a specific car"""
        rental_window = tk.Toplevel(self.root)
        rental_window.title("Rent a Car")
        
        end_date_label = tk.Label(rental_window, text="Enter End Date (DD-MM-YYYY):", font=('Calibri', 16))
        end_date_label.grid(row=0, column=0, pady=10)
        
        end_date_entry = tk.Entry(rental_window, font=('Calibri', 16), width=30)
        end_date_entry.grid(row=0, column=1, pady=10)
        
        rent_button = tk.Button(
            rental_window,
            text="Rent",
            command=lambda: self.finalize_rental(car_id, price, end_date_entry.get(), rental_window, parent_window),
            font=('Calibri', 16, 'bold'),
            width=15,
            fg='white',
            bg='#3498db'
        )
        rent_button.grid(row=1, column=0, columnspan=2, pady=10)
    
    def is_valid_date(self, date_string):
        """Validate date format (DD-MM-YYYY)"""
        try:
            datetime.strptime(date_string, '%d-%m-%Y')
            return True
        except ValueError:
            return False
    
    def finalize_rental(self, car_id, price, end_date, rental_window, parent_window):
        """Complete the rental transaction"""
        if not end_date:
            messagebox.showerror("Error", "Please enter the end date.")
            return
        
        if not self.is_valid_date(end_date):
            messagebox.showerror("Error", "Invalid date format. Please enter a valid date (DD-MM-YYYY).")
            return
        
        # Get customer ID
        customer_id = self.db.get_customer_id(self.username)
        if not customer_id:
            messagebox.showerror("Error", "Could not find customer ID.")
            return
        
        # Format dates
        today_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        end_date_formatted = datetime.strptime(end_date, '%d-%m-%Y').strftime('%Y-%m-%d')
        
        # Create rental
        success = self.db.create_rental(customer_id, car_id, today_date, end_date_formatted, price)
        
        if success:
            # Update car availability
            self.db.update_car_availability(car_id, 'Rented')
            
            messagebox.showinfo("Rental Success", "Car rented successfully!")
            rental_window.destroy()
            parent_window.destroy()
            
            # Refresh the view
            for widget in self.root.winfo_children():
                widget.destroy()
            self._display_home()
        else:
            messagebox.showerror("Error", "Failed to create rental. Please try again.")
    
    def cleanup(self):
        """Clean up resources"""
        if self.db:
            self.db.disconnect()

