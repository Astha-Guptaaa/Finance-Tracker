# User Model
# Author: Senior Software Engineering Mentor

from app.database import query_db
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    """
    User model to handle database operations related to users.
    """
    
    @staticmethod
    def create(username, email, password):
        """
        Creates a new user in the database with a hashed password.
        """
        password_hash = generate_password_hash(password)
        query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
        return query_db(query, (username, email, password_hash), commit=True)

    @staticmethod
    def get_by_id(user_id):
        """
        Retrieves a user by their ID.
        """
        query = "SELECT * FROM users WHERE id = %s"
        return query_db(query, (user_id,), one=True)

    @staticmethod
    def get_by_username(username):
        """
        Retrieves a user by their username.
        """
        query = "SELECT * FROM users WHERE username = %s"
        return query_db(query, (username,), one=True)

    @staticmethod
    def get_by_email(email):
        """
        Retrieves a user by their email.
        """
        query = "SELECT * FROM users WHERE email = %s"
        return query_db(query, (email,), one=True)

    @staticmethod
    def verify_password(stored_hash, password):
        """
        Verifies a password against the stored hash.
        """
        return check_password_hash(stored_hash, password)
