# pyrefly: ignore [missing-import]
from flask import Flask
import os
import logging
from dotenv import load_dotenv
from database.db import init_db
from controllers.main_controller import main_blueprint
from controllers.api_controller import api_blueprint

# Load environment variables from .env (local development)
load_dotenv()

def create_app():
    # Configure logging: DEBUG locally, INFO in production
    is_production = os.environ.get('FLASK_ENV') == 'production'
    log_level = logging.INFO if is_production else logging.DEBUG
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s %(levelname)s %(name)s: %(message)s'
    )
    # Initialize the Flask application
    # Set static_folder to 'frontend' and static_url_path to '/frontend' to match requirements
    app = Flask(__name__, 
                static_folder='frontend', 
                static_url_path='/frontend', 
                template_folder='templates')
    
    # Secret key: read from SECRET_KEY env var (set by Render), or generate one locally
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(24)
    
    # Initialize database tables
    with app.app_context():
        init_db()
        
    # Register blueprints (controllers)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint)
    
    return app

if __name__ == '__main__':
    app = create_app()
    # Run the application on default port 5000 in debug mode for local development
    app.run(host='127.0.0.1', port=5000, debug=True)
