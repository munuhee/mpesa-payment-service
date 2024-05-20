"""Endpoints for initiating payments."""
from flask import request, jsonify
from app import app, db, services, models

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
    response = services.initiate_stk_push(phone_number, amount)

    # Check if STK push initiation was successful
    if 'ResponseCode' in response and response['ResponseCode'] == '0':
        checkout_request_id = response.get('CheckoutRequestID')
        new_transaction = models.MpesaTransaction(
            full_name=full_name,
            phone_number=phone_number,
            amount=amount,
            checkout_request_id=checkout_request_id,
            status='Pending'
        )
        db.session.add(new_transaction)
        db.session.commit()
        return jsonify(response), 200

    # Handle error response
    error_message = response.get('ResponseDescription', 'Unknown error occurred.')
    return jsonify({'error': error_message}), 500
