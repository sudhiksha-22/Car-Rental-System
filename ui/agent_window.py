"""
Agent Window for Car Rental System
Handles agent interface for managing cars
"""

import tkinter as tk
from tkinter import messagebox, ttk, StringVar, Entry, Frame, Label, Button, Toplevel
from tkinter import END, TOP, X
from database.db_operations import DatabaseOperations


class AgentWindow:
    """
    Agent home window for managing car inventory
    """
    
    def __init__(self, root, agent_id):
        """
        Initialize agent window
        
        Args:
            root: Tkinter root window
            agent_id: Agent ID
        """
        self.root = root
        self.agent_id = agent_id
        self.root.title("Agent Car Rental Management System")
        self.root.geometry("800x600")
        
        self.db = DatabaseOperations()
        self.db.connect()
        
        self._create_widgets()
        self._display_all_cars()
    
    def _create_widgets(self):
        """Create and place UI widgets"""
        # Form variables
        self.name = StringVar()
        self.age = StringVar()
        self.doj = StringVar()
        self.gender = StringVar()
        self.email = StringVar()
        self.contact = StringVar()
        
        # Entries Frame
        entries_frame = Frame(self.root, bg="#535c68")
        entries_frame.pack(side=TOP, fill=X)
        
        title = Label(
            entries_frame, 
            text="CAR DETAILS", 
            font=("Calibri", 18, "bold"), 
            bg="#535c68", 
            fg="white"
        )
        title.grid(row=0, columnspan=4, padx=10, pady=20, sticky="w")
        
        # Car Number
        lblName = Label(entries_frame, text="Car number", font=("Calibri", 16), bg="#535c68", fg="white")
        lblName.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        txtName = Entry(entries_frame, textvariable=self.name, font=("Calibri", 16), width=30)
        txtName.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Car Model
        lblAge = Label(entries_frame, text="Carmodel", font=("Calibri", 16), bg="#535c68", fg="white")
        lblAge.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        txtAge = Entry(entries_frame, textvariable=self.age, font=("Calibri", 16), width=30)
        txtAge.grid(row=1, column=3, padx=10, pady=10, sticky="w")
        
        # Tariff
        lbldoj = Label(entries_frame, text="Tariff", font=("Calibri", 16), bg="#535c68", fg="white")
        lbldoj.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        txtDoj = Entry(entries_frame, textvariable=self.doj, font=("Calibri", 16), width=30)
        txtDoj.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        # Year
        lblEmail = Label(entries_frame, text="Year", font=("Calibri", 16), bg="#535c68", fg="white")
        lblEmail.grid(row=2, column=2, padx=10, pady=10, sticky="w")
        txtEmail = Entry(entries_frame, textvariable=self.email, font=("Calibri", 16), width=30)
        txtEmail.grid(row=2, column=3, padx=10, pady=10, sticky="w")
        
        # Availability
        lblGender = Label(entries_frame, text="Availability", font=("Calibri", 16), bg="#535c68", fg="white")
        lblGender.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        comboGender = ttk.Combobox(
            entries_frame, 
            font=("Calibri", 16), 
            width=28, 
            textvariable=self.gender, 
            state="readonly"
        )
        comboGender['values'] = ("Available", "Rented", "Returned")
        comboGender.grid(row=3, column=1, padx=10, sticky="w")
        
        # Terms
        lblContact = Label(entries_frame, text="Terms", font=("Calibri", 16), bg="#535c68", fg="white")
        lblContact.grid(row=3, column=2, padx=10, pady=10, sticky="w")
        txtContact = Entry(entries_frame, textvariable=self.contact, font=("Calibri", 16), width=30)
        txtContact.grid(row=3, column=3, padx=10, sticky="w")
        
        # Buttons Frame
        btn_frame = Frame(entries_frame, bg="#535c68")
        btn_frame.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="w")
        
        btnAdd = Button(
            btn_frame, 
            command=self.add_car, 
            text="Add Details", 
            width=15, 
            font=("Calibri", 16, "bold"), 
            fg="white",
            bg="#16a085", 
            bd=0
        )
        btnAdd.grid(row=0, column=0)
        
        btnEdit = Button(
            btn_frame, 
            command=self.update_car, 
            text="Update Details", 
            width=15, 
            font=("Calibri", 16, "bold"),
            fg="white", 
            bg="#2980b9",
            bd=0
        )
        btnEdit.grid(row=0, column=1, padx=10)
        
        btnDelete = Button(
            btn_frame, 
            command=self.delete_car, 
            text="Delete Details", 
            width=15, 
            font=("Calibri", 16, "bold"),
            fg="white", 
            bg="#c0392b",
            bd=0
        )
        btnDelete.grid(row=0, column=2, padx=10)
        
        btnClear = Button(
            btn_frame, 
            command=self.clear_all, 
            text="Clear Details", 
            width=15, 
            font=("Calibri", 16, "bold"), 
            fg="white",
            bg="#f39c12",
            bd=0
        )
        btnClear.grid(row=0, column=3, padx=10)
        
        # Table Frame
        self.tree_frame = Frame(self.root, bg="#ecf0f1")
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        
        style = ttk.Style()
        style.configure("mystyle.Treeview", font=('Calibri', 18), rowheight=50)
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 18))
        
        self.tv = ttk.Treeview(
            self.tree_frame, 
            columns=(1, 2, 3, 4, 5, 6, 7), 
            style="mystyle.Treeview"
        )
        self.tv.heading("1", text="CAR NUMBER")
        self.tv.column("1", width=100)
        self.tv.heading("2", text="Model")
        self.tv.column("2", width=150)
        self.tv.heading("3", text="Tariff")
        self.tv.column("3", width=100)
        self.tv.heading("4", text="Year")
        self.tv.column("4", width=100)
        self.tv.heading("5", text="Availability")
        self.tv.column("5", width=150)
        self.tv['show'] = 'headings'
        self.tv.pack(fill=tk.BOTH, expand=True)
    
    def _display_all_cars(self):
        """Display all cars in the table"""
        self.tv.delete(*self.tv.get_children())
        cars = self.db.get_all_cars()
        
        for row in cars:
            self.tv.insert("", END, values=row)
    
    def add_car(self):
        """Add a new car to the system"""
        if (
            self.name.get() == "" or
            self.age.get() == "" or
            self.doj.get() == "" or
            self.email.get() == "" or
            self.gender.get() == "" or
            self.contact.get() == ""
        ):
            messagebox.showerror("Error in Input", "Please Fill All the Details")
            return
        
        try:
            car_number = int(self.name.get())
            car_model = self.age.get()
            tariff = int(self.doj.get())
            year = int(self.email.get())
            terms = self.contact.get()
            
            success = self.db.add_car(car_number, self.agent_id, car_model, tariff, year, terms)
            
            if success:
                messagebox.showinfo("Success", "Record Inserted")
                self.clear_all()
                self._display_all_cars()
            else:
                messagebox.showerror("Error", "Failed to add car. Please try again.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for Car Number, Tariff, and Year.")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding car: {str(e)}")
    
    def update_car(self):
        """Open update car dialog"""
        update_window = Toplevel(self.root)
        update_window.title("Update Car")
        update_window.configure(bg='#333333')
        
        carnumber_label = Label(
            update_window, 
            text="Car number", 
            bg='#333333', 
            fg="#FFFFFF", 
            font=("Arial", 16)
        )
        carnumber_label.grid(row=1, column=0, padx=10, pady=10)
        
        carnumber_entry = Entry(update_window, font=("Arial", 16))
        carnumber_entry.grid(row=1, column=1, pady=20, padx=10)
        
        field_label = Label(
            update_window, 
            text="Field (CarModel/Tariff/Year/Terms/Availability)", 
            bg='#333333', 
            fg="#FFFFFF", 
            font=("Arial", 16)
        )
        field_label.grid(row=2, column=0, padx=10, pady=10)
        
        field_entry = Entry(update_window, font=("Arial", 16))
        field_entry.grid(row=2, column=1, pady=20, padx=10)
        
        val_label = Label(
            update_window, 
            text="Value", 
            bg='#333333', 
            fg="#FFFFFF", 
            font=("Arial", 16)
        )
        val_label.grid(row=3, column=0, padx=10, pady=10)
        
        val_entry = Entry(update_window, font=("Arial", 16))
        val_entry.grid(row=3, column=1, pady=20, padx=10)
        
        def perform_update():
            cn = carnumber_entry.get()
            field = field_entry.get()
            value = val_entry.get()
            
            if cn and field and value:
                success = self.db.update_car(int(cn), field, value)
                if success:
                    messagebox.showinfo(title="Success", message="Successfully updated")
                    update_window.destroy()
                    self.clear_all()
                    self._display_all_cars()
                else:
                    messagebox.showerror(title="Error", message="Failed to update. Please check your inputs.")
            else:
                messagebox.showerror(title="Error", message="Please fill all fields.")
        
        update_button = Button(
            update_window, 
            text="UPDATE", 
            bg="#FF3399", 
            fg="#FFFFFF", 
            font=("Arial", 16),
            command=perform_update
        )
        update_button.grid(row=4, column=0, columnspan=2, pady=10)
    
    def delete_car(self):
        """Open delete car dialog"""
        delete_window = Toplevel(self.root)
        delete_window.title("Delete Car")
        delete_window.configure(bg='#333333')
        
        carnumber_label = Label(
            delete_window, 
            text="Car number", 
            bg='#333333', 
            fg="#FFFFFF", 
            font=("Arial", 16)
        )
        carnumber_label.grid(row=1, column=0, padx=10, pady=10)
        
        carnumber_entry = Entry(delete_window, font=("Arial", 16))
        carnumber_entry.grid(row=1, column=1, pady=20, padx=10)
        
        def perform_delete():
            cn = carnumber_entry.get()
            if cn:
                try:
                    success = self.db.delete_car(int(cn))
                    if success:
                        messagebox.showinfo(title="Success", message="Successfully deleted")
                        delete_window.destroy()
                        self._display_all_cars()
                    else:
                        messagebox.showerror(title="Error", message="Failed to delete car.")
                except ValueError:
                    messagebox.showerror(title="Error", message="Please enter a valid car number.")
                except Exception as e:
                    messagebox.showerror(title="Error", message=f"Error during delete: {str(e)}")
            else:
                messagebox.showerror(title="Error", message="Please enter a car number.")
        
        delete_button = Button(
            delete_window, 
            text="DELETE", 
            bg="#FF3399", 
            fg="#FFFFFF", 
            font=("Arial", 16),
            command=perform_delete
        )
        delete_button.grid(row=2, column=0, columnspan=2, pady=10)
    
    def clear_all(self):
        """Clear all form fields"""
        self.name.set("")
        self.age.set("")
        self.doj.set("")
        self.gender.set("")
        self.email.set("")
        self.contact.set("")
    
    def cleanup(self):
        """Clean up resources"""
        if self.db:
            self.db.disconnect()

