from flask import Flask
from flask_login import LoginManager
from models import db, User
from config import Config
from auth import auth_bp  # Import the authentication blueprint

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize the database with the Flask app
    db.init_app(app)
    
    # Initialize the Flask-Login manager with the Flask app
    login_manager.init_app(app)
    
    # Set the default login view for Flask-Login
    login_manager.login_view = 'auth.login'
    
    # Register the auth blueprint
    app.register_blueprint(auth_bp)

    # Define the user loader function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app

