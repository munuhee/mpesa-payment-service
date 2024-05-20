"""
Initialize Flask app with SQLAlchemy and Flask-Migrate.

Creates a Flask app instance, configures it using 'config.py',
sets up SQLAlchemy for database operations, and configures Flask-Migrate.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Create a Flask app instance
app = Flask(__name__)

# Load configuration settings from 'config.py'
app.config.from_pyfile('config.py')

# Initialize SQLAlchemy with the app for database operations
db = SQLAlchemy(app)

# Set up Flask-Migrate for handling database migrations
migrate = Migrate(app, db)

# Import application modules
from app import routes, models, services
