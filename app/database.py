# Database Connection Module
# Author: Senior Software Engineering Mentor

import mysql.connector
from mysql.connector import Error
from flask import current_app, g
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='logs/database.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s: %(message)s'
)

def get_db_connection():
    """
    Establishes a connection to the MySQL database.
    Stores the connection in Flask's 'g' object for reuse during a single request.
    """
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(
                host=current_app.config['DB_HOST'],
                user=current_app.config['DB_USER'],
                password=current_app.config['DB_PASSWORD'],
                database=current_app.config['DB_NAME'],
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci',
                autocommit=True  # Set to True for simpler transaction management in this project
            )
            # Ensure the connection is still alive
            if not g.db.is_connected():
                raise Error("Database connection failed")
                
        except Error as e:
            logging.error(f"Error connecting to MySQL: {e}")
            return None
            
    return g.db

def close_db_connection(e=None):
    """
    Closes the database connection at the end of the request.
    """
    db = g.pop('db', None)
    if db is not None and db.is_connected():
        db.close()

def query_db(query, args=(), one=False, commit=False):
    """
    Helper function to execute SQL queries.
    - query: SQL query string
    - args: tuple of arguments for placeholders
    - one: if True, returns only the first result
    - commit: if True, performs a commit (for INSERT/UPDATE/DELETE)
    """
    db = get_db_connection()
    if db is None:
        return None
        
    cursor = db.cursor(dictionary=True) # Returns results as dictionaries
    try:
        cursor.execute(query, args)
        
        if commit:
            db.commit()
            last_id = cursor.lastrowid
            cursor.close()
            return last_id
            
        rv = cursor.fetchall()
        cursor.close()
        return (rv[0] if rv else None) if one else rv
        
    except Error as e:
        logging.error(f"Database Query Error: {e} | Query: {query} | Args: {args}")
        if commit:
            db.rollback()
        cursor.close()
        return None

def init_app(app):
    """
    Registers database cleanup with the Flask app.
    """
    app.teardown_appcontext(close_db_connection)
