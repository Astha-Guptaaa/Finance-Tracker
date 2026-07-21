# Budget Model
# Author: Senior Software Engineering Mentor

from app.database import query_db

class Budget:
    """
    Budget model to handle database operations related to monthly budgets.
    """
    
    @staticmethod
    def get_user_budget(user_id, month, year):
        """
        Retrieves a user's budget for a specific month and year.
        """
        query = "SELECT * FROM budgets WHERE user_id = %s AND month = %s AND year = %s"
        return query_db(query, (user_id, month, year), one=True)

    @staticmethod
    def set_budget(user_id, amount, month, year):
        """
        Creates or updates a user's budget for a specific month and year.
        Uses ON DUPLICATE KEY UPDATE for efficient handling.
        """
        query = """
            INSERT INTO budgets (user_id, monthly_budget, month, year)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE monthly_budget = VALUES(monthly_budget)
        """
        return query_db(query, (user_id, amount, month, year), commit=True)

    @staticmethod
    def get_monthly_spending(user_id, month, year):
        """
        Calculates total expenses for a user in a specific month and year.
        """
        query = """
            SELECT SUM(amount) as total_spent
            FROM transactions
            WHERE user_id = %s 
            AND transaction_type = 'Expense'
            AND MONTH(transaction_date) = %s
            AND YEAR(transaction_date) = %s
        """
        result = query_db(query, (user_id, month, year), one=True)
        return result['total_spent'] if result and result['total_spent'] else 0.00
