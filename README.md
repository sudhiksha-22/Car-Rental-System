# Car Rental System

A Python + Tkinter desktop application for managing car rentals with Oracle Database integration. This system supports both customer and agent interfaces for renting and managing vehicles.

## Project Overview

The Car Rental System is a desktop application that allows customers to browse, rent, and return cars, while agents can manage the car inventory. The system uses Oracle Database for data persistence and provides a clean, user-friendly Tkinter interface.

## Features

### Customer Features
- User Registration & Login
- Browse Available Cars
- Rent Cars with custom end dates
- View Currently Rented Cars
- Return Cars
- Overdue Car Detection (blocks new rentals if overdue)

### Agent Features
- Agent Registration & Login
- Add New Cars to Inventory
- Update Car Details (Model, Tariff, Year, Terms, Availability)
- Delete Cars from Inventory
- View Complete Car Inventory

## Tech Stack

- **Python 3.7+** - Programming language
- **Tkinter** - GUI framework
- **Oracle Database** - Database management system
- **oracledb** - Python Oracle database driver

## How to Run

### Prerequisites
1. Python 3.7+ installed
2. Oracle Database (Oracle XE or higher) installed and running
3. Oracle Instant Client downloaded and extracted

### Setup Steps

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure database connection:**
   - Copy `config.example.py` to `config.py`
   - Edit `config.py` with your Oracle Database credentials:
     ```python
     DB_HOST = "your_host"
     DB_SERVICE = "XE"
     DB_USER = "your_username"
     DB_PASSWORD = "your_password"
     ORACLE_CLIENT_LIB_DIR = r"C:/path/to/instantclient_21_12"
     ```

3. **Set up database tables:**
   - Connect to your Oracle Database
   - Run the SQL scripts to create required tables (Customers, Agent, Cars, RentalTransactions)
   - Create the sequence: `rental_transaction_seq`

4. **Run the application:**
   ```bash
   python main.py
   ```

5. **Login or Register:**
   - Use existing credentials, or
   - Click "Register" to create a new account (Customer or Agent)

---

**Note**: Make sure your Oracle Database is running and the connection details in `config.py` are correct before running the application.
