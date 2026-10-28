"""
Simulated payment gateway service.
This is an educational prototype - NOT a real payment integration.
"""

import logging
from datetime import datetime
from typing import Dict, Any
import uuid

logger = logging.getLogger("telco-health-connect")

# NOTE: This is a SIMULATED payment gateway.
# No real money is processed, no actual payment provider is integrated.
# This is for demonstration and educational purposes only.

class PaymentGateway:
    """Simulated payment gateway for demonstration."""
    
    def __init__(self):
        self.transactions: Dict[str, Dict[str, Any]] = {}
        self.statuses = ["approved", "declined", "pending"]
    
    def process_payment(
        self,
        transaction_id: str,
        amount: float,
        payment_method: str = "simulated_card"
    ) -> Dict[str, Any]:
        """
        Simulate processing a payment.
        
        Args:
            transaction_id: Unique transaction identifier
            amount: Payment amount
            payment_method: Simulated payment method type
            
        Returns:
            Payment result dictionary
            
        Note:
            This simulates a payment gateway response.
            No external API calls are made.
        """
        # Generate simulated response
        timestamp = datetime.now().isoformat()
        
        # Simulate successful payment (in production, this would call actual gateway)
        result = {
            "transaction_id": transaction_id,
            "amount": amount,
            "status": "success",
            "processed_at": timestamp,
            "gateway_response": "Simulated payment approved",
            "gateway_reference": f"GATEWAY-{uuid.uuid4().hex[:8].upper()}",
            "payment_method": payment_method,
            "fees": 0,  # Simulated: no fees in demo
        }
        
        # Store transaction record (in-memory only)
        self.transactions[transaction_id] = result
        
        logger.info(f"Simulated payment processed: {transaction_id} - {amount}IDR")
        
        return result
    
    def get_transaction_status(self, transaction_id: str) -> Dict[str, Any]:
        """Get status of a simulated transaction."""
        if transaction_id in self.transactions:
            return self.transactions[transaction_id]
        return {"error": "Transaction not found"}


# Global payment gateway instance
_gateway = PaymentGateway()


def simulate_payment_gateway(
    transaction_id: str,
    amount: float,
    payment_method: str = "simulated_card",
    timeout: float = 30.0
) -> Dict[str, Any]:
    """
    Process a simulated payment.
    
    Args:
        transaction_id: Unique transaction identifier
        amount: Payment amount in IDR
        payment_method: Payment method type
        timeout: Request timeout in seconds (explicit timeout as per requirements)
        
    Returns:
        Dictionary with payment result
        
    Raises:
        ValueError: If validation fails
        ConnectionError: If gateway is unreachable (simulated)
        
    Note:
        This is a SIMULATION only. No real payment gateway is integrated.
        All data is purely for demonstration purposes.
    """
    # Validate inputs
    if not transaction_id:
        raise ValueError("Transaction ID is required")
    
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")
    
    if amount > 100000000:  # 100 million IDR max
        raise ValueError("Amount exceeds maximum allowed value")
    
    # Simulate gateway processing
    # In production: actual HTTP call to payment gateway with explicit timeout
    result = _gateway.process_payment(transaction_id, amount, payment_method)
    
    # Build response compatible with PaymentResponse schema
    return {
        "status": result["status"],
        "transaction_id": result["transaction_id"],
        "amount": result["amount"],
        "processed_at": result["processed_at"],
        "gateway_response": result["gateway_response"],
    }


def validate_payment_request(transaction_id: str, amount: float) -> bool:
    """
    Validate payment request parameters.
    
    Args:
        transaction_id: Transaction identifier
        amount: Payment amount
        
    Returns:
        True if valid, False otherwise
    """
    import re
    
    # Validate transaction ID format
    if not re.match(r'^[A-Z0-9]{8,20}$', transaction_id):
        return False
    
    # Validate amount
    if amount <= 0 or amount > 100000000:
        return False
    
    return True