# Database Initialization Script (Robust Version)
# Author: Senior Software Engineering Mentor

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

def initialize_database():
    # Load environment variables manually to be sure
    load_dotenv()
    
    db_host = os.getenv('DB_HOST', 'localhost')
    db_user = os.getenv('DB_USER', 'root')
    db_pass = os.getenv('DB_PASSWORD', '')
    db_name = os.getenv('DB_NAME', 'asthafinance')

    print(f"--- Database Initialization Start ---")
    print(f"Connecting to: {db_host}")
    print(f"User: {db_user}")
    print(f"Database: {db_name}")

    try:
        # Connect to MySQL (without database first)
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pass
        )
        cursor = conn.cursor()

        # Create Database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.execute(f"USE {db_name}")
        print(f"Database '{db_name}' is ready.")

        # Table: users
        print("Creating 'users' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                email VARCHAR(100) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB;
        """)

        # Table: transactions
        print("Creating 'transactions' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                transaction_type ENUM('Income', 'Expense', 'Received', 'Sent') NOT NULL,
                category VARCHAR(50) NOT NULL,
                amount DECIMAL(15, 2) NOT NULL,
                description TEXT,
                transaction_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            ) ENGINE=InnoDB;
        """)

        # Table: budgets
        print("Creating 'budgets' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                monthly_budget DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
                month INT NOT NULL,
                year INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY unique_budget (user_id, month, year),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            ) ENGINE=InnoDB;
        """)

        conn.commit()
        print(f"\nALL TABLES CREATED SUCCESSFULLY!")
        print(f"--- Database Initialization End ---\n")

    except Error as e:
        print(f"\n❌ ERROR: {e}")
        print(f"Please check your MySQL credentials in the .env file.")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    initialize_database()
