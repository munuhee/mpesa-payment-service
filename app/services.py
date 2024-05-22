"""
Module providing functions for interacting with the M-Pesa API.
"""

import base64
from datetime import datetime
import requests
from app import app, db, models

def generate_access_token():
    """Generate access token for M-Pesa API authentication."""
    consumer_key = app.config['MPESA_CONSUMER_KEY']
    consumer_secret = app.config['MPESA_CONSUMER_SECRET']

    # Concatenate consumer key and consumer secret
    auth_string = f"{consumer_key}:{consumer_secret}"
    # Encode the auth string in base64
    encoded_auth_string = base64.b64encode(auth_string.encode()).decode('utf-8')
    headers = {'Authorization': f'Basic {encoded_auth_string}'}

    response = requests.get(
        'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials',
        headers=headers,
        timeout=10
    )
    access_token = response.json()['access_token']
    return access_token

def generate_password():
    """Generate password for M-Pesa transactions."""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    # Concatenate Shortcode, Passkey, and Timestamp
    concat_string = f"{app.config['MPESA_SHORTCODE']}{app.config['MPESA_PASSKEY']}{timestamp}"
    # Encode the concatenated string to base64
    return base64.b64encode(concat_string.encode()).decode()

# Initiate STK push for M-Pesa payment
def initiate_stk_push(full_name, phone_number, amount):
    """Initiate STK push for M-Pesa payment."""
    access_token = generate_access_token()
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'}
    password = generate_password()

    payload = {
        "BusinessShortCode": int(app.config['MPESA_SHORTCODE']),
        "Password": password,
        "Timestamp": datetime.now().strftime('%Y%m%d%H%M%S'),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": int(app.config['MPESA_SHORTCODE']),
        "PhoneNumber": phone_number,
        "CallBackURL": app.config['MPESA_CONFIRMATION_URL'],
        "AccountReference": "CompanyXLTD",
        "TransactionDesc": "Payment of X"
    }

    response = requests.post(
        'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
        headers=headers,
        json=payload,
        timeout=10
    )

    response_data = response.json()

    # Save transaction details to database if the request was accepted for processing
    if 'ResponseCode' in response_data and response_data['ResponseCode'] == '0':
        checkout_request_id = response_data.get('CheckoutRequestID')
        transaction = models.MpesaTransaction(
            full_name=full_name,
            phone_number=phone_number,
            amount=amount,
            checkout_request_id=checkout_request_id,
            status='Pending'
        )
        db.session.add(transaction)
        db.session.commit()

    return response_data

def query_transaction_status(checkout_request_id):
    """Query transaction status."""
    access_token = generate_access_token()
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'}
    password = generate_password()
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    business_short_code = int(app.config['MPESA_SHORTCODE'])

    query_data = {
        "BusinessShortCode": business_short_code,
        "Password": password,
        "Timestamp": timestamp,
        "CheckoutRequestID": checkout_request_id
    }

    response = requests.post(
        'https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query',
        json=query_data,
        headers=headers,
        timeout=10
    )

    # Save transaction details to database if the request was accepted for processing
    if 'ResultCode' in response and response['ResultCode'] == '0':
        transaction = models.MpesaTransaction.query.filter_by(
            checkout_request_id=checkout_request_id
        ).first()
        if transaction:
            transaction.status = 'Completed'
            db.session.commit()
        return response.json()

    response_data = response.json()
    return response_data
