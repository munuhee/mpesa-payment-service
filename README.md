# Mpesa Payment Service

<img src="https://res.cloudinary.com/murste/image/upload/v1713944812/icons/daraja_geyyh9.png" width="150" />

The Lipa na M-PESA Online API, also known as M-PESA Express (STK Push/NI Push), is a merchant-initiated Customer to Business (C2B) payment method.

The Lipa na M-PESA online API process is explained below:

1. The Merchant (Partner) captures and sets the API required parameters and sends the API request.

2. The API receives the request and validates it internally first, then sends you an acknowledgment response.

3. Through API Proxy, an STK Push trigger request is sent to the M-PESA registered phone number of the customer's making the payment.

4. The customer confirms by entering their M-PESA PIN.

5. The response is sent back to M-PESA and is processed as below:

   a) M-PESA validates the customer's PIN

   b) M-PESA debits the customer's Mobile Wallet.

   c) M-PESA credits the Merchant (Partner) account.

6. Once the request is processed send the RESULTS back to the API Management system, which is then forwarded to the merchant via the callback URL specified in the REQUEST.

7. The customer receives an SMS confirmation message of the payment.

This application allows you to integrate M-Pesa functionalities into your Flask application. It enables features like initiating STK push requests.


## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/munuhee/mpesa-payment-service.git
   cd mpesa-payment-service
   ```

2. **Virtual Environment Setup:**
   - It's a best practice to work within a virtual environment to manage package dependencies. Here's how to set it up based on your operating system:

     - **For Windows:**
       ```bash
       python -m venv venv
       venv\Scripts\activate
       ```
     - **For macOS/Linux:**
       ```bash
       python3 -m venv venv
       source venv/bin/activate
       ```

3. Upgrade `pip` and install the required packages:

   ```bash
   python3 -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Prerequisites

Before you begin, ensure you have the following:

- A Safaricom Developer Portal account. [Safaricom Developer Portal](https://developer.safaricom.co.ke/)
- Consumer Key and Consumer Secret obtained from the Safaricom Developer Portal.
- Test credentials assigned to you by Safaricom.

## Setup

1. **Environment Configuration:**
   - Create a `.env` file in the root directory of your Flask project.
   - Add the following credentials to your `.env` file:

     ```bash
     # Daraja API credentials
     CONSUMER_KEY= # Your Safaricom Consumer Key
     CONSUMER_SECRET= # Your Safaricom Consumer Secret
     SHORTCODE= # Your Safaricom Short Code
     PASSKEY= # Your Passkey
     CONFIRMATION_URL= # Your Url

     # Database URI
     SQLALCHEMY_DATABASE_URI= # Your  Database URI
     ```

2. **Environment Activation:**
   - Once the virtual environment is activated, depending on your operating system, run the appropriate command to source the `.env` file:

     - **For Linux/MacOS:**
       ```bash
       source .env
       ```
     - **For Windows:**
       ```bash
       call setenv.bat
       ```

## Database Migration

To manage database migrations, follow these steps:

1. Initialize the migration environment:
   ```bash
   flask db init
   ```

2. Create an initial migration:
   ```bash
   flask db migrate -m "Initial migration"
   ```

3. Apply the migration to the database:
   ```bash
   flask db upgrade
   ```

## Usage

- Run the application:

   ```bash
   python run.py
   ```

### Endpoints

1. Initiate STK Push for M-Pesa Payment

**Endpoint:** `/initiate_mpesa_stk_push`
**Method:** `POST`

**Description:**
Initiate an STK push request for M-Pesa payment.

**Request Body:**
```json
{
    "full_name": "string",      // Full name of the customer
    "phone_number": "string",   // Phone number of the customer
    "amount": int           // Amount to be paid
}
```

**Response:**
- **Success:** Returns the response from the STK push request.
- **Error:** Returns an error message if the request fails.

**Example Request:**
```bash
curl -X POST http://yourserver.com/initiate_mpesa_stk_push \
     -H "Content-Type: application/json" \
     -d '{
           "full_name": "John Doe",
           "phone_number": "254712345678",
           "amount": 1500
         }'
```

**Example Response:**
```json
{
    "MerchantRequestID": "1c5b-4ba8-815c-ac45c57a3db0683578",
    "CheckoutRequestID": "ws_CO_22052024141856201700000000",
    "ResponseCode": "0",
    "ResponseDescription": "Success. Request accepted for processing",
    "CustomerMessage": "Success. Request accepted for processing"
}
```

2. Query Transaction Status for M-Pesa Payment

**Endpoint:** `/query_transaction_status`
**Method:** `POST`

**Description:**
Query the status of a transaction for an M-Pesa payment.

**Request Body:**
```json
{
    "checkout_request_id": "string"  // ID of the checkout request
}
```

**Response:**
- **Success:** Returns the response from the transaction status query.
- **Error:** Returns an error message if the request fails.

**Example Request:**
```bash
curl -X POST http://yourserver.com/query_transaction_status \
     -H "Content-Type: application/json" \
     -d '{
           "checkout_request_id": "ws_CO_12345"
         }'
```

**Example Response:**
```json
{
    "ResponseCode": "0",
    "ResponseDescription": "The service request is processed successfully.",
    "MerchantRequestID": "12345",
    "CheckoutRequestID": "ws_CO_12345",
    "ResultCode": "0",
    "ResultDesc": "The transaction was successful."
}
```


## Conclusion

The Mpesa Payment Service simplifies integration of M-Pesa functionalities into your Flask application, enabling features like initiating STK push requests. By following the installation, setup, and usage instructions outlined in this README, you can incorporate M-Pesa payment capabilities into your project.

For any questions, feedback, or issues, please don't hesitate to reach out. Happy coding!

---

**Author:** [Stephen Murichu](https://github.com/munuhee)
