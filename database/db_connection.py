"""
Database connection module for Car Rental System
Handles Oracle Database connection setup and management
"""

import oracledb
import config


def init_oracle_client():
    """
    Initialize Oracle Client with the library directory from config
    """
    try:
        oracledb.init_oracle_client(lib_dir=config.ORACLE_CLIENT_LIB_DIR)
    except Exception as e:
        print(f"Warning: Oracle client initialization failed: {e}")
        print("If Oracle client is already initialized, this warning can be ignored.")


def get_connection():
    """
    Create and return a connection to the Oracle database
    
    Returns:
        connection: Oracle database connection object
        
    Raises:
        oracledb.DatabaseError: If connection fails
    """
    # Initialize Oracle client if not already done
    try:
        init_oracle_client()
    except:
        pass  # Client may already be initialized
    
    # Create DSN (Data Source Name)
    dsn = f"{config.DB_HOST}/{config.DB_SERVICE}"
    
    # Create and return connection
    connection = oracledb.connect(
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        dsn=dsn
    )
    
    return connection


def close_connection(connection, cursor=None):
    """
    Close database connection and cursor
    
    Args:
        connection: Oracle database connection object
        cursor: Optional cursor object to close
    """
    try:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    except Exception as e:
        print(f"Error closing connection: {e}")

