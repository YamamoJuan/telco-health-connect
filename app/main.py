"""
Main FastAPI application for Telco Health Connect Payment Service.
Simulated third-party payment integration prototype.
"""

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.security import HTTPBasicCredentials
from fastapi import security
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
import os
import logging
from datetime import datetime
import json

# Import local modules
from .schemas import PaymentRequest, PaymentResponse, HealthResponse
from .security import verify_webhook_signature, compute_webhook_signature
from .payment_service import simulate_payment_gateway, validate_payment_request

# Initialize logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("telco-health-connect")

app = FastAPI(
    title="Telco Health Connect Payment Service",
    description="Simulated third-party payment integration service",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Security configuration
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "default_secret_for_demo")
http_basic = security.HTTPBasic()

def authenticate_user(credentials: HTTPBasicCredentials = Depends(http_basic)):
    """Basic authentication for protected endpoints."""
    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Missing authentication credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    if not credentials.username or not credentials.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    if credentials.username != "intern" or credentials.password != "intern123":
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Override validation error handler to return 400 instead of 422
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Return 400 Bad Request instead of 422 for validation errors."""
    errors = exc.errors()
    error_messages = []
    for error in errors:
        field = ".".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        error_messages.append(f"{field}: {message}")
    
    return JSONResponse(
        status_code=400,
        content={
            "error": "Bad Request",
            "detail": "; ".join(error_messages)
        }
    )

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Return application health status."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="0.1.0"
    )

@app.post("/payments", response_model=PaymentResponse)
def create_payment(request: PaymentRequest, _: str = Depends(authenticate_user)):
    """Accept a payment request with transaction ID and amount."""
    try:
        response = simulate_payment_gateway(
            transaction_id=request.transaction_id,
            amount=request.amount
        )
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Payment processing failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Payment processing failed"
        )

@app.post("/webhooks/payment")
async def payment_webhook(request: Request, _: str = Depends(authenticate_user)):
    """Receive simulated payment status notifications with HMAC signature verification."""
    # Read request body as bytes
    body_bytes = await request.body()
    body_str = body_bytes.decode('utf-8')
    
    # Parse body for validation
    try:
        body_data = json.loads(body_str)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in webhook body: {e}")
        raise HTTPException(
            status_code=400,
            detail="Invalid JSON in request body"
        )
    
    # Validate required fields
    transaction_id = body_data.get("transaction_id")
    amount = body_data.get("amount")
    
    if not transaction_id or not amount:
        raise HTTPException(
            status_code=400,
            detail="Missing required fields: transaction_id or amount"
        )
    
    # Check if signature is provided in headers
    signature = request.headers.get("X-Signature")
    if not signature:
        raise HTTPException(
            status_code=400,
            detail="Missing webhook signature"
        )
    
    # Verify webhook signature
    is_valid = verify_webhook_signature(
        payload=body_str,
        signature=signature,
        secret=WEBHOOK_SECRET
    )
    
    if not is_valid:
        logger.warning(f"Invalid webhook signature for transaction: {transaction_id}")
        raise HTTPException(
            status_code=401,
            detail="Invalid webhook signature"
        )
    
    # Process payment notification (simulated)
    logger.info(f"Payment webhook received for transaction: {transaction_id}")
    
    return {
        "status": "success",
        "message": "Payment status notification received",
        "transaction_id": transaction_id,
        "amount": amount,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )