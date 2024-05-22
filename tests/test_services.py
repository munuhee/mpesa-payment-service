import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from app import app, db
from app.services import (
    generate_access_token,
    initiate_stk_push,
    query_transaction_status
)

class TestMpesaServices(unittest.TestCase):

    def setUp(self):
        with app.app_context():
            # Set up an in-memory SQLite database for testing
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
            db.create_all()

    def tearDown(self):
        with app.app_context():
            # Clean up the database after each test
            db.session.remove()
            db.drop_all()

    @patch('app.services.requests.get')
    def test_generate_access_token(self, mock_get):
        expected_token = "c9SQxWWhmdVRlyh0zh8gZDTkubVF"
        mock_get.return_value.json.return_value = {"access_token": expected_token}
        token = generate_access_token()
        self.assertEqual(token, expected_token)

    @patch('app.services.requests.post')
    def test_initiate_stk_push(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "MerchantRequestID": "29115-34620561-1",
            "CheckoutRequestID": "ws_CO_191220191020363925",
            "ResponseCode": "0",
            "ResponseDescription": "Success. Request accepted for processing",
            "CustomerMessage": "Success. Request accepted for processing"
        }
        mock_post.return_value = mock_response

        with app.app_context():
            full_name = "John Doe"
            phone_number = 254700000000
            amount = 100
            response = initiate_stk_push(full_name, phone_number, amount)

            self.assertEqual(response['ResponseCode'], "0")
            self.assertEqual(response['ResponseDescription'], "Success. Request accepted for processing")

    @patch('app.services.requests.post')
    def test_query_transaction_status(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "ResponseCode": "0",
            "ResponseDescription": "The service request has been accepted successsfully",
            "MerchantRequestID": "22205-34066-1",
            "CheckoutRequestID": "ws_CO_13012021093521236557",
            "ResultCode": "0",
            "ResultDesc": "The service request is processed successfully."
        }
        mock_post.return_value = mock_response

        with app.app_context():
            checkout_request_id = "ws_CO_13012021093521236557"
            response = query_transaction_status(checkout_request_id)

            self.assertEqual(response['ResponseCode'], "0")
            self.assertEqual(response['ResponseDescription'], "The service request has been accepted successsfully")
            self.assertEqual(response['ResultCode'], "0")
            self.assertEqual(response['ResultDesc'], "The service request is processed successfully.")

if __name__ == '__main__':
    unittest.main()
