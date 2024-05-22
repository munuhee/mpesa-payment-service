"""
Unit tests for Payment service routes.

This module tests the endpoints and functionality of the Payment service,
specifically focusing on the M-Pesa STK push initiation and transaction status query endpoints.
"""
import unittest
from unittest.mock import patch
from app import app, db

class FlaskTestCase(unittest.TestCase):
    """Test case for Payment service routes."""

    def setUp(self):
        """Set up a test client and initialize an in-memory database."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        # Create an application context and push it
        self.app_context = app.app_context()
        self.app_context.push()

        # Initialize the test client
        self.app = app.test_client()
        db.create_all()  # Create all database tables

    def tearDown(self):
        """Tear down the database and close the session."""
        # Remove the database session and drop all tables
        db.session.remove()
        db.drop_all()
        self.app_context.pop()  # Pop the application context

    @patch('app.services.initiate_stk_push')
    def test_initiate_mpesa_stk_push_success(self, mock_initiate_stk_push):
        """Test initiating M-Pesa STK push successfully."""
        # Mock the initiate_stk_push service response
        mock_initiate_stk_push.return_value = {
            'ResponseCode': '0',
            'ResponseDescription': 'Success',
            'MerchantRequestID': '12345',
            'CheckoutRequestID': '67890'
        }

        # Send a POST request to initiate the M-Pesa STK push
        response = self.app.post('/initiate_mpesa_stk_push', json={
            'full_name': 'John Doe',
            'phone_number': '254700000000',
            'amount': 1
        })

        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertIn('ResponseCode', response.get_json())
        self.assertEqual(response.get_json()['ResponseCode'], '0')

    def test_initiate_mpesa_stk_push_missing_fields(self):
        """Test initiating M-Pesa STK push with missing fields."""
        # Send a POST request with missing fields
        response = self.app.post('/initiate_mpesa_stk_push', json={
            'full_name': 'John Doe',
            'phone_number': '254700000000'
        })

        # Verify the response
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())
        self.assertEqual(
            response.get_json()['error'],
            'Full name, phone number, and amount are required.'
        )

    def test_initiate_mpesa_stk_push_invalid_phone_number(self):
        """Test initiating M-Pesa STK push with an invalid phone number."""
        # Send a POST request with an invalid phone number
        response = self.app.post('/initiate_mpesa_stk_push', json={
            'full_name': 'John Doe',
            'phone_number': 'invalid_phone',
            'amount': 1
        })

        # Verify the response
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())
        self.assertEqual(response.get_json()['error'], 'Invalid phone number.')

    def test_initiate_mpesa_stk_push_invalid_amount(self):
        """Test initiating M-Pesa STK push with an invalid amount."""
        # Send a POST request with an invalid amount
        response = self.app.post('/initiate_mpesa_stk_push', json={
            'full_name': 'John Doe',
            'phone_number': '254700000000',
            'amount': 'invalid_amount'
        })

        # Verify the response
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())
        self.assertEqual(response.get_json()['error'], 'Invalid amount.')

    @patch('app.services.query_transaction_status')
    def test_query_transaction_status_success(self, mock_query_transaction_status):
        """Test querying transaction status successfully."""
        # Mock the query_transaction_status service response
        mock_query_transaction_status.return_value = {
            'ResponseCode': '0',
            'ResponseDescription':'The service request has been accepted successsfully',
            'MerchantRequestID':'7071-4170-a0e4-8345632bad44629026',
            'CheckoutRequestID':'ws_CO_13012021093521236557',
            'ResultCode': '0',
            'ResultDesc':'The service request is processed successfully.'
        }

        # Send a POST request to query the transaction status
        response = self.app.post('/query_transaction_status', json={
            'checkout_request_id': 'ws_CO_13012021093521236557'
        })

        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertIn('ResponseCode', response.get_json())
        self.assertEqual(response.get_json()['ResponseCode'], '0')

    def test_query_transaction_status_missing_checkout_request_id(self):
        """Test querying transaction status with missing checkout request ID."""
        # Send a POST request with missing checkout request ID
        response = self.app.post('/query_transaction_status', json={})

        # Verify the response
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())
        self.assertEqual(response.get_json()['error'], 'Checkout request ID is required.')

    @patch('app.services.query_transaction_status')
    def test_query_transaction_status_failure(self, mock_query_transaction_status):
        """Test querying transaction status with a failure response."""
        # Mock the query_transaction_status service response with an error
        mock_query_transaction_status.return_value = {
            "CheckoutRequestID": "ws_CO_22052024141856201700000000",
            "MerchantRequestID": "1c5b-4ba8-815c-ac45c57a3db0683578",
            "ResponseCode": "0",
            "ResponseDescription": "The service request has been accepted successsfully",
            "ResultCode": "1001",
            "ResultDesc": "Unable to lock subscriber."
        }

        # Send a POST request to query the transaction status
        response = self.app.post('/query_transaction_status', json={
            'checkout_request_id': 'ws_CO_22052024141856201700000000'
        })

        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['ResultCode'], '1001')

if __name__ == '__main__':
    unittest.main()
