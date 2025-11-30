"""
Configuration file example for Car Rental System
Copy this file to config.py and update with your actual database credentials
"""

# Oracle Database Configuration
DB_HOST = "your_host"  # e.g., "localhost" or "DESKTOP-XXXXX"
DB_PORT = 1521
DB_SERVICE = "XE"  # Your service name (e.g., XE for Oracle Express Edition)
DB_USER = "your_username"  # Your database username
DB_PASSWORD = "your_password"  # Your database password

# Oracle Instant Client Path
# Update this to point to your Oracle Instant Client installation
# Example: r"C:/oracle/instantclient_21_12"
ORACLE_CLIENT_LIB_DIR = r"C:/path/to/instantclient_21_12"

# Application Settings
APP_TITLE = "Car Rental System"
APP_GEOMETRY = "400x300"

