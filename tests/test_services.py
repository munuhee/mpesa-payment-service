"""Module for testing service functions."""

import unittest
from app.services import generate_access_token, initiate_stk_push

class TestServices(unittest.TestCase):
    """Test case for service functions."""

    def test_generate_access_token(self):
        """Test generate_access_token function."""
        # Call the function under test
        access_token = generate_access_token()

        # Assertions
        self.assertIsNotNone(access_token)
        self.assertIsInstance(access_token, str)

    def test_initiate_stk_push(self):
        """Test initiate_stk_push function."""
        # Call the function under test
        response = initiate_stk_push(254700000000, 1)

        # Assertions
        self.assertIsNotNone(response)
        self.assertIsInstance(response, dict)
        self.assertIn('ResponseCode', response)

if __name__ == '__main__':
    unittest.main()
