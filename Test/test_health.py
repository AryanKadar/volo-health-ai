"""
test_health.py – pytest tests for the /health endpoint
Run from intern/Backend/ with venv active:
    pytest ../Test/test_health.py -v
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Backend'))

import pytest
from fastapi.testclient import TestClient

# Import the FastAPI app (main.py must be importable from Backend/)
try:
    from main import app
    client = TestClient(app)
    BACKEND_AVAILABLE = True
except ImportError:
    BACKEND_AVAILABLE = False


@pytest.mark.skipif(not BACKEND_AVAILABLE, reason="Backend main.py not found")
class TestHealthEndpoint:
    def test_health_returns_200(self):
        """Health endpoint should return HTTP 200."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_status_ok(self):
        """Response body should contain status='ok'."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "ok"

    def test_health_has_service_key(self):
        """Response body should contain a 'service' key."""
        response = client.get("/health")
        data = response.json()
        assert "service" in data

    def test_health_content_type_json(self):
        """Response content-type should be application/json."""
        response = client.get("/health")
        assert "application/json" in response.headers.get("content-type", "")
