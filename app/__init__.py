# Application Factory
# Author: Senior Software Engineering Mentor

from flask import Flask
from app.config import config_map
from app.database import init_app as init_db

def create_app(config_name='default'):
    """
    Application factory for creating and configuring the Flask app.
    """
    app = Flask(__name__)
    
    # Load Configuration
    app.config.from_object(config_map[config_name])
    
    # Initialize Database cleanup
    init_db(app)
    
    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.transactions import transactions_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.analytics import analytics_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(transactions_bp, url_prefix='/transactions')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(analytics_bp, url_prefix='/analytics')
    
    # Root route redirect
    
    @app.route('/')
    def index():
        from flask import redirect, url_for, session
        if 'user_id' in session:
            return redirect(url_for('dashboard.index'))
        return redirect(url_for('auth.login'))

    return app
