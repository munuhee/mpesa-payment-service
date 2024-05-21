"""Endpoints for initiating payments."""
from flask import request, jsonify
from app import app, services

@app.route('/initiate_mpesa_stk_push', methods=['POST'])
def initiate_mpesa_stk_push():
    """Initiate STK push for M-Pesa payment.

    Args:
        full_name (str): Full name of the customer.
        phone_number (str): Phone number of the customer.
        amount (float): Amount to be paid.

    Returns:
        dict: Response from the STK push request.
    """
    full_name = request.json.get('full_name')
    phone_number = request.json.get('phone_number')
    amount = request.json.get('amount')

    # Check if required fields are provided
    if not all([full_name, phone_number, amount]):
        return jsonify({'error': 'Full name, phone number, and amount are required.'}), 400

    # Convert phone number to int
    try:
        phone_number = int(phone_number)
    except ValueError:
        return jsonify({'error': 'Invalid phone number.'}), 400

    # Convert amount to integer
    try:
        amount = int(amount)
    except ValueError:
        return jsonify({'error': 'Invalid amount.'}), 400

    # Initiate STK push
    response = services.initiate_stk_push(full_name, phone_number, amount)

    # Check if STK push initiation was successful
    if 'ResponseCode' in response and response['ResponseCode'] == '0':
        return jsonify(response), 200

    # Handle error response
    error_message = response.get('ResponseDescription', 'Unknown error occurred.')
    return jsonify({'error': error_message}), 500

@app.route('/query_transaction_status', methods=['POST'])
def query_transaction_status():
    """
    Query transaction status for M-Pesa payment.

    Args:
        checkout_request_id (str): ID of the checkout request.

    Returns:
        dict: Response from the transaction status query.
    """
    # Get checkout request ID from request
    checkout_request_id = request.json.get('checkout_request_id')

    # Check if checkout request ID is provided
    if not checkout_request_id:
        return jsonify({'error': 'Checkout request ID is required.'}), 400

    # Query transaction status
    response = services.query_transaction_status(checkout_request_id)

    # Check if the response contains transaction status information
    if 'ResponseCode' in response:
        return jsonify(response), 200

    # Handle error response
    error_message = response.get('errorMessage', 'Unknown error occurred.')
    return jsonify({'error': error_message}), 500
