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

@app.route('/mpesa_callback', methods=['POST'])
def mpesa_callback():
    """Handle M-Pesa STK push callback and return saved data as JSON."""
    data = request.json
    print(data)

    if data and 'Body' in data and 'stkCallback' in data['Body']:
        callback_data = data['Body']['stkCallback']
        merchant_request_id = callback_data.get('MerchantRequestID')
        checkout_request_id = callback_data.get('CheckoutRequestID')
        result_code = callback_data.get('ResultCode')
        result_desc = callback_data.get('ResultDesc')

        # Find the transaction in the database
        transaction = models.MpesaTransaction.query.filter_by(checkout_request_id=checkout_request_id).first()

        if transaction:
            transaction.result_desc = result_desc

            if result_code == 0 and 'CallbackMetadata' in callback_data:
                metadata = callback_data['CallbackMetadata']['Item']
                mpesa_receipt_number = None
                transaction_date = None

                for item in metadata:
                    if item['Name'] == 'Amount':
                        amount = item['Value']
                    elif item['Name'] == 'MpesaReceiptNumber':
                        mpesa_receipt_number = item['Value']
                    elif item['Name'] == 'TransactionDate':
                        transaction_date = item['Value']
                    elif item['Name'] == 'PhoneNumber':
                        phone_number = item['Value']

                transaction.mpesa_receipt_number = mpesa_receipt_number
                transaction.transaction_date = transaction_date
                transaction.status = 'Completed'
            else:
                transaction.status = 'Failed'

            db.session.commit()

            # Convert transaction to dictionary
            transaction_data = {
                'id': transaction.id,
                'full_name': transaction.full_name,
                'phone_number': transaction.phone_number,
                'amount': transaction.amount,
                'checkout_request_id': transaction.checkout_request_id,
                'mpesa_receipt_number': transaction.mpesa_receipt_number,
                'transaction_date': transaction.transaction_date,
                'status': transaction.status,
                'result_desc': transaction.result_desc,
                'timestamp': transaction.timestamp
            }

            return jsonify({
                "Transaction": transaction_data
            }), 200

    return jsonify({"ResultCode": 1, "ResultDesc": "Failure"}), 400
