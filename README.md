# Telco Health Connect Payment Service

## Overview
Simulated third-party payment integration service for educational purposes. This is a mock payment gateway that demonstrates secure payment processing patterns without integrating with real payment providers.

## Technology Stack
- Python 3.12
- FastAPI
- Uvicorn
- Pydantic
- Pytest
- HTTPX
- Docker (multi-stage build)

## Project Structure
```
telco-health-connect/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   ├── security.py
│   └── payment_service.py
├── tests/
│   ├── __init__.py
│   ├── test_health.py
│   ├── test_payments.py
│   └── test_webhooks.py
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── .dockerignore
├── .env.example
├── .gitignore
├── README.md
├── SECURITY.md
├── docs/
│   ├── API.md
│   ├── SECURITY_AUDIT.md
│   ├── DEVELOPMENT_LOG.md
│   └── CODE_REVIEW.md
├── scripts/
│   └── security_scan.ps1
└── evidence/
```

## Installation

### Prerequisites
- Python 3.12+
- pip (Python package manager)
- Docker (optional, for containerized deployment)

### Local Development Setup
1. Clone this repository
2. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

### Running the Application
```bash
uvicorn app.main:app --reload
```

The application will be available at http://localhost:8000

### Testing
```bash
pytest tests/
```

## Docker Usage

### Build the Docker image
```bash
docker build -t telco-health-connect .
```

### Run the Docker container
```bash
docker run -p 8000:8000 \
  -e WEBHOOK_SECRET=your_secure_secret \
  --name telco-payment-service \
  telco-health-connect
```

## Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| WEBHOOK_SECRET | Secret key for HMAC signature verification | required |

## API Endpoints

### GET /health
Returns application health status.

### POST /payments
Accepts payment requests with transaction ID and amount. Validates input and simulates payment processing.

### POST /webhooks/payment
Receives payment status notifications with HMAC-SHA256 signature verification.

## Security Features
- Input validation using Pydantic
- HMAC-SHA256 signature verification for webhooks
- Non-root user execution in Docker
- Multi-stage Docker build for security
- Environment variable configuration
- No sensitive data logging

## Documentation
- API documentation: http://localhost:8000/docs
- OpenAPI JSON: http://localhost:8000/openapi.json

## Limitations
- This is a simulated service - no real payment processing
- No database integration
- In-memory transaction storage (not persistent)
- For educational purposes only