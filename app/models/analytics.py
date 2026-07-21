# Analytics Model
# Author: Senior Software Engineering Mentor

from app.database import query_db

class Analytics:
    """
    Analytics model to handle database operations for charts and reports.
    """
    
    @staticmethod
    def get_monthly_trends(user_id, year):
        """
        Retrieves monthly income and expense totals for a specific year.
        """
        query = """
            SELECT 
                MONTH(transaction_date) as month,
                SUM(CASE WHEN transaction_type = 'Income' THEN amount ELSE 0 END) as total_income,
                SUM(CASE WHEN transaction_type = 'Expense' THEN amount ELSE 0 END) as total_expense
            FROM transactions
            WHERE user_id = %s AND YEAR(transaction_date) = %s
            GROUP BY MONTH(transaction_date)
            ORDER BY month
        """
        return query_db(query, (user_id, year))

    @staticmethod
    def get_category_distribution(user_id, month, year):
        """
        Retrieves expense distribution by category for a specific month.
        """
        query = """
            SELECT category, SUM(amount) as total
            FROM transactions
            WHERE user_id = %s 
              AND transaction_type = 'Expense'
              AND MONTH(transaction_date) = %s
              AND YEAR(transaction_date) = %s
            GROUP BY category
            ORDER BY total DESC
        """
        return query_db(query, (user_id, month, year))

    @staticmethod
    def get_report_data(user_id, start_date=None, end_date=None):
        """
        Retrieves detailed transaction data for reports.
        """
        query = "SELECT transaction_date, transaction_type, category, amount, description FROM transactions WHERE user_id = %s"
        params = [user_id]
        
        if start_date:
            query += " AND transaction_date >= %s"
            params.append(start_date)
        if end_date:
            query += " AND transaction_date <= %s"
            params.append(end_date)
            
        query += " ORDER BY transaction_date DESC"
        return query_db(query, tuple(params))
