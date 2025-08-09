
from flask import Flask
# import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Initialize extensions outside create_app, but without passing 'app' yet
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Configuration
    #app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site4.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ea34283308ca600a82345b884d250ab3') # Use environment variable for secret key
    app.config['SECRET_KEY'] = 'ea34283308ca600a82345b884d250ab3'

    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "auth.index"
    login_manager.login_message = "Login or Register"
    login_manager.login_message_category = "warning"

    # Import and Register blueprints inside create_app to avoid circular imports
    # if blueprints need to access 'app' or 'db'
    from .authetication.routes import auth_bp
    from .users.routes import users

    app.register_blueprint(auth_bp)
    app.register_blueprint(users)

    return app

# This line is for Gunicorn to find the 'app' object.
# It calls create_app() to get the Flask application instance.
app = create_app()

# Optional: If you need to initialize db with app context for shell or migrations
with app.app_context():
    db.create_all() # Only run this if you want to create tables on app start,
                      # usually handled by migrations or separate script.
