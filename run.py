# Entry point for the application
# Author: Senior Software Engineering Mentor

from app import create_app
import os

# Create the application instance using the environment set in .env
config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    # Run the application
    # Host '0.0.0.0' makes the server accessible externally
    app.run(host='0.0.0.0', port=5000)
