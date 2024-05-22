"""Module for testing MpesaTransaction class."""

import unittest
from app.models import MpesaTransaction


class TestMpesaTransaction(unittest.TestCase):
    """Test case for the MpesaTransaction class."""

    def setUp(self):
        """Set up a MpesaTransaction instance."""
        self.transaction = MpesaTransaction(
            full_name="John Doe",
            phone_number="254700000000",
            amount=1
        )

    def test_attributes(self):
        """Test if attributes are set correctly."""
        self.assertEqual(self.transaction.full_name, "John Doe")
        self.assertEqual(self.transaction.phone_number, "254700000000")
        self.assertEqual(self.transaction.amount, 1)

    def test_repr(self):
        """Test the __repr__ method."""
        expected_repr = (
            "MpesaTransaction(id=None, full_name='John Doe', "
            "phone_number='254700000000', amount=1)"
        )
        self.assertEqual(repr(self.transaction), expected_repr)

if __name__ == '__main__':
    unittest.main()
