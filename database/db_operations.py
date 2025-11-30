"""
Database operations module for Car Rental System
Contains all SQL queries and database operations
"""

import oracledb
from datetime import datetime
from .db_connection import get_connection, close_connection


class DatabaseOperations:
    """
    Handles all database operations for the Car Rental System
    """
    
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establish database connection"""
        self.connection = get_connection()
        self.cursor = self.connection.cursor()
    
    def disconnect(self):
        """Close database connection"""
        close_connection(self.connection, self.cursor)
        self.connection = None
        self.cursor = None
    
    def commit(self):
        """Commit current transaction"""
        if self.connection:
            self.connection.commit()
    
    # ============ Customer Operations ============
    
    def login_customer(self, username, password):
        """
        Authenticate customer login
        
        Args:
            username: Customer username
            password: Customer password
            
        Returns:
            tuple: User record if found, None otherwise
        """
        query = """
            SELECT * FROM Users 
            WHERE USERNAME = :username AND PASSWORD = :password
        """
        self.cursor.execute(query, {'username': username, 'password': password})
        return self.cursor.fetchone()
    
    def register_customer(self, customer_id, username, password):
        """
        Register a new customer
        
        Args:
            customer_id: Unique customer ID (will be used for both USER_ID and CUST_ID)
            username: Customer username
            password: Customer password
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Insert into Users table
            query_users = """
                INSERT INTO Users (USER_ID, USERNAME, PASSWORD) 
                VALUES (:user_id, :username, :password)
            """
            self.cursor.execute(query_users, {
                'user_id': customer_id,
                'username': username,
                'password': password
            })
            
            # Insert into Customer table
            query_customer = """
                INSERT INTO Customer (CUST_ID, CUST_NAME) 
                VALUES (:cust_id, :cust_name)
            """
            self.cursor.execute(query_customer, {
                'cust_id': customer_id,
                'cust_name': username
            })
            
            self.commit()
            return True
        except oracledb.DatabaseError as e:
            print(f"Database Error: {e}")
            return False
    
    def get_customer_id(self, username):
        """
        Get customer ID (CUST_ID) by username for use in RentalTransactions
        Since CUSTOMERID in RentalTransactions references Customer.CUST_ID
        
        If customer doesn't exist in Customer table, try to create it from Users table
        
        Args:
            username: Customer username
            
        Returns:
            int: Customer ID (CUST_ID) or None
        """
        # Get CUST_ID from Customer table using CUST_NAME (which matches USERNAME)
        query = "SELECT CUST_ID FROM Customer WHERE CUST_NAME = :username"
        self.cursor.execute(query, {'username': username})
        result = self.cursor.fetchone()
        
        if result:
            return result[0]
        
        # If not found in Customer table, check if user exists in Users table
        # and create corresponding Customer record
        query_user = "SELECT USER_ID FROM Users WHERE USERNAME = :username"
        self.cursor.execute(query_user, {'username': username})
        user_result = self.cursor.fetchone()
        
        if user_result:
            user_id = user_result[0]
            # Create Customer record with same ID
            try:
                # Check if it already exists (in case of race condition)
                check_existing = "SELECT CUST_ID FROM Customer WHERE CUST_ID = :cust_id"
                self.cursor.execute(check_existing, {'cust_id': user_id})
                if self.cursor.fetchone():
                    return user_id
                
                insert_customer = """
                    INSERT INTO Customer (CUST_ID, CUST_NAME) 
                    VALUES (:cust_id, :cust_name)
                """
                self.cursor.execute(insert_customer, {
                    'cust_id': user_id,
                    'cust_name': username
                })
                self.commit()
                # Verify it was created
                self.cursor.execute(check_existing, {'cust_id': user_id})
                if self.cursor.fetchone():
                    return user_id
                else:
                    print(f"Warning: Customer record creation may have failed for USER_ID {user_id}")
                    return None
            except oracledb.DatabaseError as e:
                print(f"Error creating Customer record: {e}")
                # Try to get existing record in case of duplicate key error
                check_existing = "SELECT CUST_ID FROM Customer WHERE CUST_ID = :cust_id"
                self.cursor.execute(check_existing, {'cust_id': user_id})
                existing = self.cursor.fetchone()
                if existing:
                    return existing[0]
                return None
        
        return None
    
    def get_customer_rented_cars(self, username):
        """
        Get all rented cars for a customer
        
        Args:
            username: Customer username
            
        Returns:
            list: List of rented car records
        """
        query = """
            SELECT CARID, CARMODEL, YEAR, RENTALENDDATE
            FROM (
                SELECT C.CARID, C.CARMODEL, C.YEAR, RT.RENTALENDDATE,
                       ROW_NUMBER() OVER (PARTITION BY C.CARID ORDER BY RT.RENTALENDDATE DESC) AS rnk
                FROM Cars C
                INNER JOIN RentalTransactions RT ON C.CARID = RT.CARID
                WHERE C.AVAILABILITYSTATUS = 'Rented'
                AND RT.CUSTOMERID = (SELECT CUST_ID FROM Customer WHERE CUST_NAME = :username)
            )
            WHERE rnk = 1
        """
        self.cursor.execute(query, {'username': username})
        return self.cursor.fetchall()
    
    def get_overdue_cars(self, username):
        """
        Get overdue cars for a customer
        
        Args:
            username: Customer username
            
        Returns:
            list: List of overdue car records
        """
        query = """
            SELECT C.CARID, C.CARMODEL, RT.RENTALENDDATE
            FROM Cars C
            INNER JOIN RentalTransactions RT ON C.CARID = RT.CARID
            WHERE C.AVAILABILITYSTATUS = 'Rented'
            AND RT.CUSTOMERID = (SELECT CUST_ID FROM Customer WHERE CUST_NAME = :username)
            AND RT.RENTALSTATUS = 'Pending'
            AND RT.RENTALENDDATE < SYSTIMESTAMP
        """
        self.cursor.execute(query, {'username': username})
        return self.cursor.fetchall()
    
    # ============ Agent Operations ============
    
    def login_agent(self, username, password):
        """
        Authenticate agent login
        
        Args:
            username: Agent username
            password: Agent password
            
        Returns:
            tuple: Agent record if found, None otherwise
        """
        query = """
            SELECT * FROM Agent 
            WHERE AGENTNAME = :username AND A_PASSWORD = :password
        """
        self.cursor.execute(query, {'username': username, 'password': password})
        return self.cursor.fetchone()
    
    def register_agent(self, agent_id, agentname, password):
        """
        Register a new agent
        
        Args:
            agent_id: Unique agent ID
            agentname: Agent username
            password: Agent password (must be 8 characters based on schema)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # A_PASSWORD is CHAR(8) and CONTACT is CHAR(10), so we need to provide values
            # Truncate password to 8 chars if longer, pad if shorter
            password_8 = (password[:8] if len(password) >= 8 else password.ljust(8))[:8]
            contact = ''  # Empty contact, can be updated later
            
            query = """
                INSERT INTO Agent (AGENTID, AGENTNAME, A_PASSWORD, CARHANDLING, CONTACT) 
                VALUES (:agent_id, :agentname, :password, 0, :contact)
            """
            self.cursor.execute(query, {
                'agent_id': agent_id,
                'agentname': agentname,
                'password': password_8,
                'contact': contact
            })
            self.commit()
            return True
        except oracledb.DatabaseError as e:
            print(f"Database Error: {e}")
            return False
    
    # ============ Car Operations ============
    
    def get_available_cars(self):
        """
        Get all available cars for rent
        
        Returns:
            list: List of available car records
        """
        query = "SELECT * FROM Cars WHERE AVAILABILITYSTATUS = 'Available'"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_all_cars(self):
        """
        Get all cars (for agent view)
        
        Returns:
            list: List of all car records
        """
        query = "SELECT CARID, CARMODEL, TARIFF, YEAR, AVAILABILITYSTATUS FROM Cars"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def add_car(self, car_id, agent_id, car_model, tariff, year, terms):
        """
        Add a new car to the system
        
        Args:
            car_id: Unique car ID
            agent_id: Agent ID who manages this car
            car_model: Car model name
            tariff: Rental tariff
            year: Car year
            terms: Rental terms
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            query = """
                INSERT INTO Cars (CARID, AGENTID, CARMODEL, TARIFF, ODAMOUNT, YEAR, TERMS, AVAILABILITYSTATUS)
                VALUES (:car_id, :agent_id, :car_model, :tariff, :odamount, :year, :terms, 'Available')
            """
            self.cursor.execute(query, {
                'car_id': car_id,
                'agent_id': agent_id,
                'car_model': car_model,
                'tariff': tariff,
                'odamount': tariff // 4,
                'year': year,
                'terms': terms
            })
            self.commit()
            return True
        except oracledb.DatabaseError as e:
            print(f"Database Error: {e}")
            return False
    
    def update_car(self, car_id, field, value):
        """
        Update a car field
        
        Args:
            car_id: Car ID to update
            field: Field name to update
            value: New value
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Map field names to column names
            field_mapping = {
                'CarModel': 'CARMODEL',
                'Tariff': 'TARIFF',
                'Year': 'YEAR',
                'Terms': 'TERMS',
                'Availability': 'AVAILABILITYSTATUS'
            }
            
            if field not in field_mapping:
                return False
            
            column = field_mapping[field]
            
            # Handle different data types
            if field == 'Tariff':
                query = f"UPDATE Cars SET {column} = :value WHERE CARID = :car_id"
                self.cursor.execute(query, {'value': int(value), 'car_id': int(car_id)})
            elif field == 'Year':
                query = f"UPDATE Cars SET {column} = :value WHERE CARID = :car_id"
                self.cursor.execute(query, {'value': int(value), 'car_id': int(car_id)})
            else:
                query = f"UPDATE Cars SET {column} = :value WHERE CARID = :car_id"
                self.cursor.execute(query, {'value': value, 'car_id': int(car_id)})
            
            self.commit()
            return True
        except Exception as e:
            print(f"Error updating car: {e}")
            return False
    
    def delete_car(self, car_id):
        """
        Delete a car from the system
        
        Args:
            car_id: Car ID to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            query = "DELETE FROM Cars WHERE CARID = :car_id"
            self.cursor.execute(query, {'car_id': int(car_id)})
            self.commit()
            return True
        except Exception as e:
            print(f"Error deleting car: {e}")
            return False
    
    # ============ Rental Operations ============
    
    def create_rental(self, customer_id, car_id, rental_start_date, rental_end_date, total_cost):
        """
        Create a new rental transaction
        
        Args:
            customer_id: Customer ID (must be CUST_ID from Customer table)
            car_id: Car ID
            rental_start_date: Rental start date
            rental_end_date: Rental end date
            total_cost: Total rental cost
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # First, verify that the customer exists in Customer table
            check_customer = "SELECT CUST_ID FROM Customer WHERE CUST_ID = :customer_id"
            self.cursor.execute(check_customer, {'customer_id': customer_id})
            customer_exists = self.cursor.fetchone()
            
            if not customer_exists:
                print(f"Error: Customer with CUST_ID {customer_id} does not exist in Customer table")
                # Try to create it from Users table
                check_user = "SELECT USER_ID, USERNAME FROM Users WHERE USER_ID = :user_id"
                self.cursor.execute(check_user, {'user_id': customer_id})
                user_record = self.cursor.fetchone()
                
                if user_record:
                    user_id, username = user_record
                    try:
                        insert_customer = """
                            INSERT INTO Customer (CUST_ID, CUST_NAME) 
                            VALUES (:cust_id, :cust_name)
                        """
                        self.cursor.execute(insert_customer, {
                            'cust_id': user_id,
                            'cust_name': username
                        })
                        self.commit()
                        print(f"Created Customer record for USER_ID {user_id}")
                    except oracledb.DatabaseError as e:
                        print(f"Failed to create Customer record: {e}")
                        return False
                else:
                    # Debug: Check what customers exist
                    debug_query = "SELECT CUST_ID, CUST_NAME FROM Customer"
                    self.cursor.execute(debug_query)
                    existing_customers = self.cursor.fetchall()
                    print(f"Existing customers in Customer table: {existing_customers}")
                    # Also check Users table
                    debug_users = "SELECT USER_ID, USERNAME FROM Users"
                    self.cursor.execute(debug_users)
                    existing_users = self.cursor.fetchall()
                    print(f"Existing users in Users table: {existing_users}")
                    return False
            
            # Verify that the car exists
            check_car = "SELECT CARID FROM Cars WHERE CARID = :car_id"
            self.cursor.execute(check_car, {'car_id': car_id})
            if not self.cursor.fetchone():
                print(f"Error: Car with CARID {car_id} does not exist")
                return False
            
            query = """
                INSERT INTO RentalTransactions 
                (TRANSACTIONID, CUSTOMERID, CARID, RENTALSTARTDATE, RENTALENDDATE, TOTALCOST, RENTALSTATUS) 
                VALUES ((SELECT NVL(MAX(TRANSACTIONID), 0) + 1 FROM RentalTransactions), :customer_id, :car_id, 
                TO_DATE(:rental_start_date, 'YYYY-MM-DD HH24:MI:SS'), 
                TO_DATE(:rental_end_date, 'YYYY-MM-DD'), :total_cost, 'Pending')
            """
            self.cursor.execute(query, {
                'customer_id': customer_id,
                'car_id': car_id,
                'rental_start_date': rental_start_date,
                'rental_end_date': rental_end_date,
                'total_cost': total_cost
            })
            self.commit()
            return True
        except oracledb.DatabaseError as e:
            print(f"Database Error: {e}")
            print(f"Attempted to insert CUSTOMERID: {customer_id}, CARID: {car_id}")
            return False
    
    def return_car(self, car_id):
        """
        Return a rented car
        
        Args:
            car_id: Car ID to return
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            return_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Update rental transaction
            return_query = """
                UPDATE RentalTransactions RT
                SET RT.RENTALENDDATE = TO_DATE(:return_date, 'YYYY-MM-DD HH24:MI:SS'),
                    RT.RENTALSTATUS = 'Returned'
                WHERE RT.CARID = :car_id
                AND RT.RENTALSTATUS = 'Pending'
            """
            self.cursor.execute(return_query, {
                'return_date': return_date,
                'car_id': car_id
            })
            
            # Update car availability
            update_query = "UPDATE Cars SET AVAILABILITYSTATUS = 'Available' WHERE CARID = :car_id"
            self.cursor.execute(update_query, {'car_id': car_id})
            
            self.commit()
            return True
        except oracledb.DatabaseError as e:
            print(f"Database Error: {e}")
            return False
    
    def update_car_availability(self, car_id, status):
        """
        Update car availability status
        
        Args:
            car_id: Car ID
            status: New availability status ('Available' or 'Rented')
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            query = "UPDATE Cars SET AVAILABILITYSTATUS = :status WHERE CARID = :car_id"
            self.cursor.execute(query, {'status': status, 'car_id': car_id})
            self.commit()
            return True
        except Exception as e:
            print(f"Error updating availability: {e}")
            return False

