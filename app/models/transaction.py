# Transaction Model
# Author: Senior Software Engineering Mentor

from app.database import query_db

class Transaction:
    """
    Transaction model to handle database operations related to financial records.
    """
    
    @staticmethod
    def create(user_id, transaction_type, category, amount, description, transaction_date):
        """
        Creates a new transaction record.
        """
        query = """
            INSERT INTO transactions 
            (user_id, transaction_type, category, amount, description, transaction_date) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return query_db(query, (user_id, transaction_type, category, amount, description, transaction_date), commit=True)

    @staticmethod
    def get_by_id(transaction_id, user_id):
        """
        Retrieves a specific transaction for a specific user.
        """
        query = "SELECT * FROM transactions WHERE id = %s AND user_id = %s"
        return query_db(query, (transaction_id, user_id), one=True)

    @staticmethod
    def get_all_by_user(user_id, filters=None):
        """
        Retrieves all transactions for a user with optional filtering.
        """
        query = "SELECT * FROM transactions WHERE user_id = %s"
        params = [user_id]
        
        if filters:
            if filters.get('type'):
                query += " AND transaction_type = %s"
                params.append(filters['type'])
            if filters.get('start_date'):
                query += " AND transaction_date >= %s"
                params.append(filters['start_date'])
            if filters.get('end_date'):
                query += " AND transaction_date <= %s"
                params.append(filters['end_date'])
            if filters.get('search'):
                query += " AND (category LIKE %s OR description LIKE %s)"
                search_term = f"%{filters['search']}%"
                params.extend([search_term, search_term])
                
        query += " ORDER BY transaction_date DESC, created_at DESC"
        return query_db(query, tuple(params))

    @staticmethod
    def update(transaction_id, user_id, transaction_type, category, amount, description, transaction_date):
        """
        Updates an existing transaction record.
        """
        query = """
            UPDATE transactions 
            SET transaction_type = %s, category = %s, amount = %s, 
                description = %s, transaction_date = %s 
            WHERE id = %s AND user_id = %s
        """
        return query_db(query, (transaction_type, category, amount, description, transaction_date, transaction_id, user_id), commit=True)

    @staticmethod
    def delete(transaction_id, user_id):
        """
        Deletes a transaction record.
        """
        query = "DELETE FROM transactions WHERE id = %s AND user_id = %s"
        return query_db(query, (transaction_id, user_id), commit=True)

    @staticmethod
    def get_totals(user_id):
        """
        Calculates totals for each transaction type for a user.
        """
        query = """
            SELECT transaction_type, SUM(amount) as total 
            FROM transactions 
            WHERE user_id = %s 
            GROUP BY transaction_type
        """
        return query_db(query, (user_id,))
