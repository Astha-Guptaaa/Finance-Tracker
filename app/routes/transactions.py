# Transaction Routes
# Author: Senior Software Engineering Mentor

from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app.models.transaction import Transaction
from app.routes.auth import login_required
from datetime import datetime

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/')
@login_required
def index():
    """
    View all transactions with optional search and filters.
    """
    user_id = session['user_id']
    
    # Get filters from request
    filters = {
        'type': request.args.get('type'),
        'start_date': request.args.get('start_date'),
        'end_date': request.args.get('end_date'),
        'search': request.args.get('search')
    }
    
    # Handle quick filters (Today, This Week, This Month)
    quick_filter = request.args.get('filter')
    if quick_filter == 'today':
        filters['start_date'] = datetime.now().strftime('%Y-%m-%d')
        filters['end_date'] = filters['start_date']
    elif quick_filter == 'this_week':
        # Logic for start of week (Monday)
        pass # Implementation details usually depend on business requirements
    elif quick_filter == 'this_month':
        filters['start_date'] = datetime.now().strftime('%Y-%m-01')
        
    transactions = Transaction.get_all_by_user(user_id, filters)
    return render_template('transactions/list.html', transactions=transactions, filters=filters)

@transactions_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """
    Handles adding a new transaction.
    """
    if request.method == 'POST':
        user_id = session['user_id']
        t_type = request.form.get('transaction_type')
        category = request.form.get('category')
        amount = request.form.get('amount')
        description = request.form.get('description')
        date = request.form.get('transaction_date')

        if not all([t_type, category, amount, date]):
            flash('Please fill in all required fields.', 'danger')
        else:
            try:
                Transaction.create(user_id, t_type, category, amount, description, date)
                flash('Transaction added successfully!', 'success')
                return redirect(url_for('transactions.index'))
            except Exception as e:
                flash('Error adding transaction.', 'danger')

    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('transactions/add.html', today=today)

@transactions_bp.route('/edit/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def edit(transaction_id):
    """
    Handles editing an existing transaction.
    """
    user_id = session['user_id']
    transaction = Transaction.get_by_id(transaction_id, user_id)

    if not transaction:
        flash('Transaction not found.', 'danger')
        return redirect(url_for('transactions.index'))

    if request.method == 'POST':
        t_type = request.form.get('transaction_type')
        category = request.form.get('category')
        amount = request.form.get('amount')
        description = request.form.get('description')
        date = request.form.get('transaction_date')

        if not all([t_type, category, amount, date]):
            flash('Please fill in all required fields.', 'danger')
        else:
            Transaction.update(transaction_id, user_id, t_type, category, amount, description, date)
            flash('Transaction updated successfully!', 'success')
            return redirect(url_for('transactions.index'))

    return render_template('transactions/edit.html', transaction=transaction)

@transactions_bp.route('/delete/<int:transaction_id>', methods=['POST'])
@login_required
def delete(transaction_id):
    """
    Handles deleting a transaction.
    """
    user_id = session['user_id']
    Transaction.delete(transaction_id, user_id)
    flash('Transaction deleted successfully!', 'success')
    return redirect(url_for('transactions.index'))
