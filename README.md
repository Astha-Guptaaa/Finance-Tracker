# Personal Finance Tracker

A full-stack personal finance management application built with Python (Flask), MySQL, Bootstrap 5, and Chart.js.

## Features
- **User Authentication**: Secure registration and login with password hashing.
- **Transaction Management**: Add, edit, delete, and search income/expense/money transfer records.
- **Budgeting**: Monthly budget limits with spending warnings.
- **Analytics**: Charts showing monthly trends and category distribution.
- **Reports**: CSV export of all transaction data.

## Technology Stack
- **Backend**: Python 3.12, Flask
- **Database**: MySQL 8, mysql-connector-python
- **Frontend**: Bootstrap 5, Chart.js
- **Security**: Werkzeug (password hashing), Flask Sessions

## Getting Started

### Prerequisites
- Python 3.12+
- MySQL 8+

### Installation

1. **Clone the repository**:
   ```bash
   cd asthaProject
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**:
   - Create a MySQL database.
   - Run the schema script: `sql/schema.sql`.

4. **Environment Configuration**:
   - Edit the `.env` file with your database credentials and a secure `SECRET_KEY`.

5. **Run the Application**:
   ```bash
   python run.py
   ```
   Open your browser and navigate to `http://localhost:5000`.

## Usage
Refer to the [TESTING.md](TESTING.md) for a full guide on testing all features.

## Project Structure
```
asthaProject/
├── app/
│   ├── models/          # Data access layer
│   ├── routes/          # Flask Blueprints (controllers)
│   ├── static/          # CSS, JS, images
│   ├── templates/       # Jinja2 templates
│   ├── utils/           # Helper functions
│   ├── __init__.py      # Application factory
│   ├── config.py        # Configuration
│   └── database.py      # DB connection management
├── logs/                # Application logs
├── sql/                 # SQL schema
├── .env                 # Environment variables
├── requirements.txt     # Dependencies
└── run.py               # Entry point
```
