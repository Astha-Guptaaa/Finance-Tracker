# Analytics Routes
# Author: Senior Software Engineering Mentor

from flask import Blueprint, render_template, session, request, Response
from app.models.analytics import Analytics
from app.routes.auth import login_required
from datetime import datetime
import csv
import io

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/')
@login_required
def index():
    """
    Analytics dashboard with chart data.
    """
    user_id = session['user_id']
    now = datetime.now()
    
    # Get Trends for Chart.js
    trends = Analytics.get_monthly_trends(user_id, now.year)
    
    # Prepare labels (Months) and datasets
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    income_data = [0] * 12
    expense_data = [0] * 12
    
    for row in trends:
        month_idx = row['month'] - 1
        income_data[month_idx] = float(row['total_income'])
        expense_data[month_idx] = float(row['total_expense'])

    # Get Category Distribution for Pie Chart
    distribution = Analytics.get_category_distribution(user_id, now.month, now.year)
    cat_labels = [row['category'] for row in distribution]
    cat_values = [float(row['total']) for row in distribution]

    return render_template(
        'analytics/index.html',
        months=months,
        income_data=income_data,
        expense_data=expense_data,
        cat_labels=cat_labels,
        cat_values=cat_values
    )

@analytics_bp.route('/export/csv')
@login_required
def export_csv():
    """
    Exports transactions to CSV format.
    """
    user_id = session['user_id']
    data = Analytics.get_report_data(user_id)
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['Date', 'Type', 'Category', 'Amount', 'Description'])
    
    # Rows
    for row in data:
        writer.writerow([
            row['transaction_date'],
            row['transaction_type'],
            row['category'],
            row['amount'],
            row['description']
        ])
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=financial_report.csv"}
    )
