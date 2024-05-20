"""
Module: Transactions
"""
from datetime import datetime
from app import db

class MpesaTransaction(db.Model):
    """
    Represents a transaction made through the M-Pesa service.

    Attributes:
        id (int): Unique identifier for the transaction.
        full_name (str): Full name of the user initiating the transaction.
        phone_number (str): Phone number associated with the user initiating the transaction.
            Format: "<country_code><phone_number>" (e.g., "254700000000")
        amount (int): Amount of money involved in the transaction.
    """
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=True)
    phone_number = db.Column(db.String(13), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    checkout_request_id = db.Column(db.String(100), nullable=False, unique=True)
    mpesa_receipt_number = db.Column(db.String(100))
    transaction_date = db.Column(db.String(100))
    status = db.Column(db.String(20), default='Pending')
    result_desc = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        """
        String representation of the MpesaTransaction object.
        """
        return f"MpesaTransaction(id={self.id}, full_name='{self.full_name}', "\
                f"phone_number='{self.phone_number}', amount={self.amount})"
