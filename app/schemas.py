"""
Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import re


class PaymentRequest(BaseModel):
    """Payment request schema."""
    transaction_id: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0, description="Payment amount in IDR")
    
    @field_validator('transaction_id')
    @classmethod
    def validate_transaction_id(cls, v: str) -> str:
        """Validate transaction ID format."""
        if not re.match(r'^[A-Z0-9]{8,20}$', v):
            raise ValueError('Transaction ID must be 8-20 uppercase alphanumeric characters')
        return v
    
    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: float) -> float:
        """Validate payment amount."""
        if v <= 0:
            raise ValueError('Amount must be greater than zero')
        if v > 100000000:  # 100 million IDR max
            raise ValueError('Amount exceeds maximum allowed value')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "transaction_id": "TRX20241028ABC",
                "amount": 150000.50
            }
        }


class PaymentResponse(BaseModel):
    """Payment response schema."""
    status: str
    transaction_id: str
    amount: float
    processed_at: str
    gateway_response: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "transaction_id": "TRX20241028ABC",
                "amount": 150000.50,
                "processed_at": "2024-10-28T10:30:00.000Z",
                "gateway_response": "Simulated payment approved"
            }
        }


class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str
    timestamp: str
    version: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2024-10-28T10:30:00.000Z",
                "version": "0.1.0"
            }
        }


class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str
    detail: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Bad Request",
                "detail": "Invalid amount provided"
            }
        }