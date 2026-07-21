# Personal Finance Tracker - Testing Guide
# Author: Senior Software Engineering Mentor

This guide provides step-by-step instructions to verify the functionality of the Personal Finance Tracker.

## 1. Environment Setup Verification
- [ ] **Python Version**: Ensure you are using Python 3.12 (`python --version`).
- [ ] **Dependencies**: Install all required packages:
  ```bash
  pip install -r requirements.txt
  ```
- [ ] **Environment Variables**: Verify `.env` file exists and contains correct MySQL credentials.

## 2. Database Verification
- [ ] **Schema Import**: Run the SQL script in your MySQL terminal:
  ```sql
  SOURCE sql/schema.sql;
  ```
- [ ] **Connection Test**: Run the app (`python run.py`). If no "Database Connection Failed" errors appear in `logs/database.log`, the connection is successful.

## 3. Functional Test Cases

### A. Authentication Module
- [ ] **Register**: Create a new account. Verify that duplicate usernames/emails are blocked.
- [ ] **Login**: Access the dashboard with your new credentials.
- [ ] **Session**: Try to access `/dashboard/` directly in a private window; it should redirect you to `/auth/login`.

### B. Transaction Module
- [ ] **Add**: Create one of each type: Income, Expense, Received, Sent.
- [ ] **Validation**: Try to save a transaction without an amount; it should show a validation error.
- [ ] **Edit**: Change the amount of an existing transaction and verify the update.
- [ ] **Delete**: Remove a test transaction and verify it disappears from the list.

### C. Dashboard & Budgeting
- [ ] **Balance Calculation**: Verify `Balance = (Income + Received) - (Expense + Sent)`.
- [ ] **Budget Warning**: Set a budget of $100. Add an expense of $150. Verify the progress bar turns red and shows a warning.
- [ ] **Recent List**: Ensure the dashboard shows only the 5 most recent entries.

### D. Analytics & Reports
- [ ] **Charts**: Visit the Analytics page. Verify the Line Chart shows your monthly data.
- [ ] **CSV Export**: Click "Generate Report". Open the downloaded file to ensure all transaction details are present.

## 4. Error Handling Verification
- [ ] **404 Page**: Visit a non-existent URL (e.g., `/random-page`) to ensure the app handles it gracefully.
- [ ] **Logs**: Check `logs/database.log` for any captured SQL errors during your testing session.
