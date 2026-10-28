"""
Tests for the webhook endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.security import compute_webhook_signature
import json
import os
import base64


class TestWebhookEndpoint:
    """Tests for POST /webhooks/payment endpoint."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    @pytest.fixture
    def webhook_secret(self):
        """Get webhook secret from environment or default."""
        return os.getenv("WEBHOOK_SECRET", "default_secret_for_demo")
    
    @pytest.fixture
    def auth_header(self):
        """Generate authentication header for tests."""
        credentials = base64.b64encode(b"intern:intern123").decode('utf-8')
        return {"Authorization": f"Basic {credentials}"}
    
    def test_webhook_valid_signature(self, client, webhook_secret, auth_header):
        """Webhook with valid signature should succeed."""
        payload = json.dumps({
            "transaction_id": "TRX20241028ABC",
            "amount": 150000
        })
        signature = compute_webhook_signature(payload.encode('utf-8'), webhook_secret)
        
        headers = auth_header.copy()
        headers["X-Signature"] = signature
        headers["Content-Type"] = "application/json"
        
        response = client.post(
            "/webhooks/payment",
            data=payload,
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success"
        assert data["transaction_id"] == "TRX20241028ABC"
    
    def test_webhook_invalid_signature(self, client, auth_header):
        """Webhook with invalid signature should fail with 401."""
        payload = json.dumps({
            "transaction_id": "TRX20241028ABC",
            "amount": 150000
        })
        
        headers = auth_header.copy()
        headers["X-Signature"] = "sha256=invalid_signature_value"
        headers["Content-Type"] = "application/json"
        
        response = client.post(
            "/webhooks/payment",
            data=payload,
            headers=headers
        )
        
        assert response.status_code == 401
        data = response.json()
        
        # HTTPException returns detail, not error field
        assert "Invalid webhook signature" in data["detail"]
    
    def test_webhook_missing_signature(self, client, auth_header):
        """Webhook without signature should fail with 400."""
        payload = json.dumps({
            "transaction_id": "TRX20241028ABC",
            "amount": 150000
        })
        
        headers = auth_header.copy()
        headers["Content-Type"] = "application/json"
        
        response = client.post(
            "/webhooks/payment",
            data=payload,
            headers=headers
        )
        
        assert response.status_code == 400
        data = response.json()
        
        assert "Missing webhook signature" in data["detail"]
    
    def test_webhook_missing_required_fields(self, client, webhook_secret, auth_header):
        """Webhook with missing required fields should fail."""
        payload = json.dumps({
            "transaction_id": "TRX20241028ABC"
            # Missing amount
        })
        signature = compute_webhook_signature(payload.encode('utf-8'), webhook_secret)
        
        headers = auth_header.copy()
        headers["X-Signature"] = signature
        headers["Content-Type"] = "application/json"
        
        response = client.post(
            "/webhooks/payment",
            data=payload,
            headers=headers
        )
        
        assert response.status_code == 400
        data = response.json()
        
        assert "Missing required fields" in data["detail"]
    
    def test_webhook_invalid_json(self, client, webhook_secret, auth_header):
        """Webhook with invalid JSON should fail."""
        payload = "not valid json"
        signature = compute_webhook_signature(payload.encode('utf-8'), webhook_secret)
        
        headers = auth_header.copy()
        headers["X-Signature"] = signature
        headers["Content-Type"] = "application/json"
        
        response = client.post(
            "/webhooks/payment",
            data=payload,
            headers=headers
        )
        
        assert response.status_code == 400
        data = response.json()
        
        assert "Invalid JSON" in data["detail"]