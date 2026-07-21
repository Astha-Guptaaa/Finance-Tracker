# Dashboard Routes
# Author: Senior Software Engineering Mentor

from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from app.models.transaction import Transaction
from app.models.budget import Budget
from app.routes.auth import login_required
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    """
    Main dashboard view summarizing financial status and budget.
    """
    user_id = session['user_id']
    now = datetime.now()
    current_month = now.month
    current_year = now.year

    # 1. Fetch Totals for all transaction types
    totals_raw = Transaction.get_totals(user_id)
    totals = {
        'Income': 0.00,
        'Expense': 0.00,
        'Received': 0.00,
        'Sent': 0.00
    }
    for row in totals_raw:
        totals[row['transaction_type']] = float(row['total'])

    # 2. Calculate Balance
    # Balance = (Income + Received) - (Expense + Sent)
    current_balance = (totals['Income'] + totals['Received']) - (totals['Expense'] + totals['Sent'])

    # 3. Budget Management
    budget_info = Budget.get_user_budget(user_id, current_month, current_year)
    monthly_budget = float(budget_info['monthly_budget']) if budget_info else 0.00
    
    # 4. Monthly Spending & Budget Warning
    total_spent_this_month = float(Budget.get_monthly_spending(user_id, current_month, current_year))
    
    budget_status = {
        'limit': monthly_budget,
        'spent': total_spent_this_month,
        'remaining': max(0, monthly_budget - total_spent_this_month),
        'percentage': (total_spent_this_month / monthly_budget * 100) if monthly_budget > 0 else 0,
        'warning': total_spent_this_month > monthly_budget if monthly_budget > 0 else False
    }

    # 5. Recent Transactions (Top 5)
    recent_transactions = Transaction.get_all_by_user(user_id)
    recent_transactions = recent_transactions[:5] if recent_transactions else []

    return render_template(
        'dashboard/index.html',
        totals=totals,
        balance=current_balance,
        budget_status=budget_status,
        recent_transactions=recent_transactions,
        current_month_name=now.strftime('%B %Y')
    )

@dashboard_bp.route('/update-budget', methods=['POST'])
@login_required
def update_budget():
    """
    Handles updating the monthly budget limit.
    """
    user_id = session['user_id']
    amount = request.form.get('budget_amount')
    now = datetime.now()
    
    if amount:
        try:
            Budget.set_budget(user_id, float(amount), now.month, now.year)
            flash('Monthly budget updated successfully!', 'success')
        except ValueError:
            flash('Invalid budget amount.', 'danger')
    
    return redirect(url_for('dashboard.index'))
