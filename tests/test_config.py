"""Module for testing configuration."""

import unittest
import os
from dotenv import load_dotenv
from app import app

# Load environment variables from .env file
load_dotenv()

class TestConfig(unittest.TestCase):
    """Test configuration class."""

    def test_secret_key(self):
        """Test if SECRET_KEY is not None."""
        self.assertIsNotNone(app.config['SECRET_KEY'])

    def test_mpesa_credentials(self):
        """Test if MPESA credentials are not None."""
        self.assertIsNotNone(app.config['MPESA_CONSUMER_KEY'])
        self.assertIsNotNone(app.config['MPESA_CONSUMER_SECRET'])
        self.assertIsNotNone(app.config['MPESA_SHORTCODE'])
        self.assertIsNotNone(app.config['MPESA_PASSKEY'])
        self.assertIsNotNone(app.config['MPESA_CONFIRMATION_URL'])

    def test_database_uri(self):
        """Test if DATABASE_URI is not None."""
        if os.environ.get('FLASK_ENV') == 'testing':
            self.assertEqual(app.config['SQLALCHEMY_DATABASE_URI'], 'sqlite:///:memory:')
        else:
            self.assertIsNotNone(app.config['SQLALCHEMY_DATABASE_URI'])

    def test_sqlalchemy_track_modifications(self):
        """Test if SQLAlchemy track modifications is False."""
        self.assertFalse(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])

    def test_load_dotenv(self):
        """Test if .env file is loaded correctly."""
        self.assertIsNotNone(os.getenv('SECRET_KEY'))
        self.assertIsNotNone(os.getenv('CONSUMER_KEY'))
        self.assertIsNotNone(os.getenv('CONSUMER_SECRET'))
        self.assertIsNotNone(os.getenv('SHORTCODE'))
        self.assertIsNotNone(os.getenv('CONFIRMATION_URL'))
        self.assertIsNotNone(os.getenv('PASSKEY'))
        self.assertIsNotNone(os.getenv('SQLALCHEMY_DATABASE_URI'))
        self.assertIsNotNone(os.getenv('FLASK_ENV'))

if __name__ == '__main__':
    unittest.main()
