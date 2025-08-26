"""
Basic tests for the GraphRAG API.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Test client fixture."""
    return TestClient(app)


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "status" in data


def test_health_endpoint(client):
    """Test the health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "version" in data
    assert "dependencies" in data


def test_config_endpoint(client):
    """Test the config endpoint."""
    response = client.get("/api/config")
    assert response.status_code == 200
    data = response.json()
    assert "app_env" in data
    assert "port" in data
    assert "azure_openai_configured" in data
    assert "neo4j_configured" in data


def test_rate_limit_info_endpoint(client):
    """Test the rate limit info endpoint."""
    response = client.get("/api/rate-limit-info")
    assert response.status_code == 200
    data = response.json()
    assert "remaining" in data
    assert "limit" in data
    assert "window_seconds" in data


def test_chat_endpoint_validation(client):
    """Test chat endpoint validation."""
    # Test with missing required field
    response = client.post("/api/chat", json={})
    assert response.status_code == 422
    
    # Test with valid request
    valid_request = {
        "message": "What is the UAE Civil Code?",
        "strategy": "hybrid",
        "max_results": 10
    }
    response = client.post("/api/chat", json=valid_request)
    # Should return 503 if services not available, or 200 if working
    assert response.status_code in [200, 503]


def test_analysis_endpoint_validation(client):
    """Test analysis endpoint validation."""
    # Test with missing required field
    response = client.post("/api/analysis", json={})
    assert response.status_code == 422
    
    # Test with valid request
    valid_request = {
        "query": "Analyze contradictions in employment law",
        "analysis_type": "contradiction",
        "max_depth": 3
    }
    response = client.post("/api/analysis", json=valid_request)
    # Should return 503 if services not available, or 200 if working
    assert response.status_code in [200, 503]


def test_debug_stats_endpoint(client):
    """Test debug stats endpoint."""
    response = client.get("/api/debug/stats")
    assert response.status_code == 200
    data = response.json()
    # Should contain rate limit info at minimum
    assert "rate_limit" in data


def test_cors_headers(client):
    """Test CORS headers are present."""
    response = client.options("/")
    # CORS headers should be present
    assert "access-control-allow-origin" in response.headers


def test_request_id_header(client):
    """Test that request ID is added to response headers."""
    response = client.get("/health")
    assert "x-request-id" in response.headers
    assert response.headers["x-request-id"] is not None
