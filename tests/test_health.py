"""
Tests for the health endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime


class TestHealthEndpoint:
    """Tests for GET /health endpoint."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    def test_health_check_success(self, client):
        """Health endpoint should return healthy status."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["version"] == "0.1.0"
    
    def test_health_check_response_schema(self, client):
        """Health endpoint response should match schema."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate required fields
        assert isinstance(data, dict)
        assert "status" in data
        assert "timestamp" in data
        assert "version" in data
    
    def test_health_check_content_type(self, client):
        """Health endpoint should return JSON content type."""
        response = client.get("/health")
        
        assert response.headers["content-type"] == "application/json"