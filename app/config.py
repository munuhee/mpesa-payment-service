"""Module for configuration settings.
- loads environment variables using dotenv
- sets up various configuration parameters for the Flask app.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Secret key for Flask sessions
SECRET_KEY = os.environ.get('SECRET_KEY')

# Daraja API credentials
MPESA_CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
MPESA_CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
MPESA_SHORTCODE = os.environ.get('SHORTCODE')
MPESA_PASSKEY = os.environ.get('PASSKEY')

# SQLite database URI
if os.environ.get('FLASK_ENV') == 'testing':
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
else:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

# Disable Flask-SQLAlchemy modification tracking
SQLALCHEMY_TRACK_MODIFICATIONS = False
