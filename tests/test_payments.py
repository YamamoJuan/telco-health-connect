"""
Tests for the payment endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
import json
import base64


class TestPaymentEndpoint:
    """Tests for POST /payments endpoint."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    @pytest.fixture
    def auth_header(self):
        """Generate authentication header for tests."""
        credentials = base64.b64encode(b"intern:intern123").decode('utf-8')
        return {"Authorization": f"Basic {credentials}"}
    
    def test_payment_valid_success(self, client, auth_header):
        """Valid payment request should succeed."""
        response = client.post(
            "/payments",
            json={
                "transaction_id": "TRX20241028ABC",
                "amount": 150000.50
            },
            headers=auth_header
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success"
        assert data["transaction_id"] == "TRX20241028ABC"
        assert data["amount"] == 150000.50
    
    def test_payment_valid_insufficient_funds(self, client, auth_header):
        """Payment with zero amount should fail."""
        response = client.post(
            "/payments",
            json={
                "transaction_id": "TRX20241028ABC",
                "amount": 0
            },
            headers=auth_header
        )
        
        assert response.status_code == 400
        data = response.json()
        
        assert data["error"] == "Bad Request"
        # Pydantic returns different message format
        assert "greater than 0" in data["detail"].lower()
    
    def test_payment_invalid_transaction_id(self, client, auth_header):
        """Invalid transaction ID format should fail."""
        response = client.post(
            "/payments",
            json={
                "transaction_id": "invalid_id",  # Too short and lowercase
                "amount": 1000
            },
            headers=auth_header
        )
        
        assert response.status_code == 400
        data = response.json()
        
        assert data["error"] == "Bad Request"
        assert "Transaction ID must be 8-20 uppercase alphanumeric characters" in data["detail"]
    
    def test_payment_invalid_amount(self, client, auth_header):
        """Negative amount should fail."""
        response = client.post(
            "/payments",
            json={
                "transaction_id": "TRX20241028ABC",
                "amount": -500
            },
            headers=auth_header
        )
        
        assert response.status_code == 400
        data = response.json()
        
        assert data["error"] == "Bad Request"
        assert "greater than 0" in data["detail"].lower()
    
    def test_payment_exceeds_max_amount(self, client, auth_header):
        """Amount exceeding maximum should fail."""
        response = client.post(
            "/payments",
            json={
                "transaction_id": "TRX20241028ABC",
                "amount": 200000000  # Exceeds 100 million limit
            },
            headers=auth_header
        )
        
        assert response.status_code == 400
        data = response.json()
        
        assert data["error"] == "Bad Request"
        assert "exceeds maximum allowed value" in data["detail"].lower()