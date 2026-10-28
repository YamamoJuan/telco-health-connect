"""
Security utilities for webhook signature verification.
Implements HMAC-SHA256 signature verification with constant-time comparison.
"""

import hmac
import hashlib
import logging
from typing import Union

logger = logging.getLogger("telco-health-connect")

# Signature format: "sha256=<hex_digest>"
SIGNATURE_PREFIX = "sha256="


def verify_webhook_signature(
    payload: Union[str, bytes],
    signature: str,
    secret: str
) -> bool:
    """
    Verify webhook signature using HMAC-SHA256.
    
    Args:
        payload: The raw request body (string or bytes)
        signature: The signature from X-Signature header
        secret: The webhook secret key
        
    Returns:
        True if signature is valid, False otherwise
        
    Signing Procedure:
        1. Compute HMAC-SHA256 of payload using secret
        2. Prefix hex digest with "sha256="
        3. Compare with provided signature using constant-time comparison
        
    Example:
        signature = compute_webhook_signature(payload, secret)
        # Returns: "sha256=abc123..."
    """
    if not signature:
        logger.warning("Webhook signature is missing or empty")
        return False
    
    if not secret:
        logger.error("Webhook secret is not configured")
        return False
    
    try:
        # Convert payload to bytes if needed
        if isinstance(payload, str):
            payload_bytes = payload.encode('utf-8')
        else:
            payload_bytes = payload
        
        # Compute expected signature
        expected_signature = compute_webhook_signature(payload_bytes, secret)
        
        # Constant-time comparison to prevent timing attacks
        is_valid = hmac.compare_digest(signature, expected_signature)
        
        if not is_valid:
            logger.warning("Webhook signature verification failed")
        
        return is_valid
        
    except Exception as e:
        logger.error(f"Signature verification error: {str(e)}")
        return False


def compute_webhook_signature(payload: bytes, secret: str) -> str:
    """
    Compute webhook signature.
    
    Args:
        payload: The raw request body as bytes
        secret: The webhook secret key
        
    Returns:
        Signature in format "sha256=<hex_digest>"
    """
    if isinstance(secret, str):
        secret_bytes = secret.encode('utf-8')
    else:
        secret_bytes = secret
    
    hmac_hash = hmac.new(
        secret_bytes,
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return f"{SIGNATURE_PREFIX}{hmac_hash}"


def generate_secure_token(length: int = 32) -> str:
    """Generate a secure random token."""
    import secrets
    return secrets.token_hex(length)