"""
Pytest configuration and fixtures for GraphRAG tests.
"""

import pytest
import os
import tempfile
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient

# Set test environment
os.environ["APP_ENV"] = "test"
os.environ["LOG_LEVEL"] = "DEBUG"

# Mock environment variables for testing
os.environ["AZURE_OPENAI_API_KEY"] = "test-key"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://test.openai.azure.com/"
os.environ["AZURE_OPENAI_API_VERSION"] = "2024-02-15-preview"
os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = "test-deployment"
os.environ["NEO4J_URI"] = "bolt://localhost:7687"
os.environ["NEO4J_USER"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "test-password"


@pytest.fixture(scope="session")
def test_app():
    """Create test app instance."""
    from app.main import app
    return app


@pytest.fixture
def client(test_app):
    """Create test client."""
    return TestClient(test_app)


@pytest.fixture
def mock_openai():
    """Mock OpenAI client."""
    with patch("app.services.openai_service.OpenAIClient") as mock:
        client_instance = Mock()
        mock.return_value = client_instance
        yield client_instance


@pytest.fixture
def mock_neo4j():
    """Mock Neo4j client."""
    with patch("app.services.neo4j_service.Neo4jService") as mock:
        service_instance = Mock()
        mock.return_value = service_instance
        yield service_instance


@pytest.fixture
def mock_rate_limiter():
    """Mock rate limiter."""
    with patch("app.utils.rate_limiter.RateLimiter") as mock:
        limiter_instance = Mock()
        limiter_instance.is_allowed.return_value = True
        limiter_instance.get_remaining.return_value = 100
        limiter_instance.get_limit.return_value = 100
        mock.return_value = limiter_instance
        yield limiter_instance


@pytest.fixture
def sample_chat_request():
    """Sample chat request data."""
    return {
        "message": "What is the UAE Civil Code?",
        "strategy": "hybrid",
        "max_results": 10,
        "include_sources": True,
        "stream": False
    }


@pytest.fixture
def sample_analysis_request():
    """Sample analysis request data."""
    return {
        "query": "Analyze contradictions in employment law",
        "analysis_type": "contradiction",
        "max_depth": 3,
        "include_graph": True
    }


@pytest.fixture
def sample_rag_response():
    """Sample RAG response data."""
    return {
        "answer": "The UAE Civil Code is the primary source of civil law in the UAE...",
        "sources": [
            {
                "id": "law_001",
                "title": "UAE Civil Code Article 1",
                "content": "The Civil Code governs civil transactions...",
                "relevance_score": 0.95
            }
        ],
        "metadata": {
            "strategy_used": "hybrid",
            "processing_time": 1.2,
            "tokens_used": 150
        }
    }


@pytest.fixture
def sample_graph_response():
    """Sample graph analysis response data."""
    return {
        "analysis": {
            "type": "contradiction",
            "findings": [
                {
                    "node_id": "law_001",
                    "contradicts_with": ["law_002"],
                    "description": "Employment termination rules conflict"
                }
            ]
        },
        "graph_data": {
            "nodes": [
                {"id": "law_001", "label": "Employment Law", "type": "law"}
            ],
            "relationships": [
                {"source": "law_001", "target": "law_002", "type": "contradicts"}
            ]
        },
        "metadata": {
            "analysis_time": 2.1,
            "nodes_analyzed": 10
        }
    }


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment before each test."""
    # Create temporary directory for test files
    with tempfile.TemporaryDirectory() as temp_dir:
        os.environ["TEMP_DIR"] = temp_dir
        yield


@pytest.fixture(autouse=True)
def mock_external_services():
    """Mock external services to avoid actual API calls."""
    with patch("app.services.openai_service.OpenAIClient"), \
         patch("app.services.neo4j_service.Neo4jService"), \
         patch("app.utils.rate_limiter.RateLimiter"):
        yield


# Test markers
pytest_plugins = []


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running"
    )
    config.addinivalue_line(
        "markers", "api: marks tests as API tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers."""
    for item in items:
        if "test_health" in item.nodeid:
            item.add_marker(pytest.mark.api)
        if "test_chat" in item.nodeid or "test_analysis" in item.nodeid:
            item.add_marker(pytest.mark.integration)
