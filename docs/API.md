# API Documentation

## OpenAPI Documentation

When the application is running, you can access:

### Swagger UI
- URL: http://localhost:8000/docs
- Provides interactive API testing interface

### ReDoc
- URL: http://localhost:8000/redoc
- Alternative documentation format

### OpenAPI JSON Schema
- URL: http://localhost:8000/openapi.json
- Machine-readable API specification

## Endpoints

### GET /health

Returns the health status of the payment service.

**Response Schema:**
```json
{
  "status": "healthy",
  "timestamp": "2024-10-28T10:30:00.000Z",
  "version": "0.1.0"
}
```

**Status Codes:**
- 200: Success - Service is healthy

**Example:**
```bash
curl -X GET http://localhost:8000/health
```

### POST /payments

Process a payment request.

**Request Body Schema:**
```json
{
  "transaction_id": "TRX20241028ABC",
  "amount": 150000.50
}
```

**Validation Rules:**
- `transaction_id`: 8-20 uppercase alphanumeric characters
- `amount`: Must be > 0 and <= 100,000,000 IDR

**Response Schema:**
```json
{
  "status": "success",
  "transaction_id": "TRX20241028ABC",
  "amount": 150000.50,
  "processed_at": "2024-10-28T10:30:00.000Z",
  "gateway_response": "Simulated payment approved"
}
```

**Headers:**
- Authorization: Basic base64-encoded credentials

**Status Codes:**
- 200: Success - Payment processed
- 400: Bad Request - Invalid input validation
- 401: Unauthorized - Missing or invalid authentication
- 500: Internal Server Error - Payment processing failed

**Example:**
```bash
curl -X POST http://localhost:8000/payments \
  -H "Authorization: Basic aW50ZW46aW50ZTEyMw==" \
  -H "Content-Type: application/json" \
  -d '{"transaction_id": "TRX20241028ABC", "amount": 150000.50}'
```

### POST /webhooks/payment

Receive payment status notifications with HMAC signature verification.

**Request Body Schema:**
```json
{
  "transaction_id": "TRX20241028ABC",
  "amount": 150000
}
```

**Headers:**
- `X-Signature`: HMAC-SHA256 signature of request body
- `Authorization`: Basic base64-encoded credentials

**Webhook Signature Format:**
```
sha256=<hex_encoded_hmac_digest>
```

**Signature Generation (Python example):**
```python
import hmac
import hashlib

def sign_payload(payload: str, secret: str) -> str:
    sig = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return f"sha256={sig}"
```

**Status Codes:**
- 200: Success - Webhook received and verified
- 400: Bad Request - Missing signature or invalid JSON
- 401: Unauthorized - Invalid signature
- 500: Internal Server Error - Processing failed

**Example:**
```bash
# Generate signature
SIGNATURE=$(python -c "import hmac,hashlib; print(f'sha256={hmac.new(b\"secret\", b\"{\\\"transaction_id\\\": \\\"TRX...\\\", \\\"amount\\\": 1000}\", hashlib.sha256).hexdigest()}')")

curl -X POST http://localhost:8000/webhooks/payment \
  -H "X-Signature: $SIGNATURE" \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic aW50ZW46aW50ZTEyMw==" \
  -d '{"transaction_id": "TRX20241028ABC", "amount": 150000}'
```

## Authentication

All endpoints require HTTP Basic Authentication:

**Credentials:**
- Username: `intern`
- Password: `intern123`

**Encode for curl:**
```bash
# echo -n "intern:intern123" | base64
# Result: aW50ZW46aW50ZTEyMw==
```

## Error Responses

**Format:**
```json
{
  "error": "Bad Request",
  "detail": "Error description"
}
```

**Common Errors:**
- Bad Request (400): Invalid input or missing data
- Unauthorized (401): Authentication or signature failure
- Internal Server Error (500): Unexpected processing error

## Simulated Nature

This service **does not** connect to any real payment gateway. All transactions are simulated for educational purposes. No actual money is processed.