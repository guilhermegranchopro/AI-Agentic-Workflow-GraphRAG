"""
Tests for Neo4j service functionality.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.services.neo4j_service import Neo4jService
from app.schemas.rag import Source
import os


@pytest.fixture
def neo4j_service():
    """Create Neo4j service instance."""
    return Neo4jService()


@pytest.fixture
def mock_driver():
    """Mock Neo4j driver."""
    with patch("app.services.neo4j_service.GraphDatabase") as mock_graph_db:
        driver = Mock()
        mock_graph_db.driver.return_value = driver
        yield driver


@pytest.fixture
def mock_session():
    """Mock Neo4j session."""
    session = Mock()
    session.run = AsyncMock()
    session.close = AsyncMock()
    return session


class TestNeo4jService:
    """Test Neo4j service functionality."""

    @pytest.mark.asyncio
    async def test_neo4j_service_initialization(self, mock_driver):
        """Test Neo4j service initialization."""
        service = Neo4jService()
        assert service is not None
        assert hasattr(service, 'driver')

    @pytest.mark.asyncio
    async def test_search_knowledge_graph(self, neo4j_service, mock_driver, mock_session):
        """Test knowledge graph search."""
        # Mock session and results
        mock_driver.session.return_value.__aenter__.return_value = mock_session
        
        mock_result = Mock()
        mock_result.data.return_value = [
            {
                "node": {"id": "node1", "content": "Test content"},
                "score": 0.9
            }
        ]
        mock_session.run.return_value = mock_result

        results = await neo4j_service.search_knowledge_graph("test query", 5)

        assert isinstance(results, list)
        assert len(results) > 0
        assert "id" in results[0]
        assert "content" in results[0]
        assert "score" in results[0]

    @pytest.mark.asyncio
    async def test_search_vector_store(self, neo4j_service, mock_driver, mock_session):
        """Test vector store search."""
        # Mock session and results
        mock_driver.session.return_value.__aenter__.return_value = mock_session
        
        mock_result = Mock()
        mock_result.data.return_value = [
            {
                "node": {"id": "vec1", "content": "Vector content", "embedding": [0.1, 0.2, 0.3]},
                "score": 0.85
            }
        ]
        mock_session.run.return_value = mock_result

        results = await neo4j_service.search_vector_store("test query", 5)

        assert isinstance(results, list)
        assert len(results) > 0
        assert "id" in results[0]
        assert "content" in results[0]
        assert "score" in results[0]

    @pytest.mark.asyncio
    async def test_get_node_details(self, neo4j_service, mock_driver, mock_session):
        """Test getting node details."""
        # Mock session and results
        mock_driver.session.return_value.__aenter__.return_value = mock_session
        
        mock_result = Mock()
        mock_result.data.return_value = [
            {
                "node": {
                    "id": "node1",
                    "content": "Detailed content",
                    "type": "Article",
                    "metadata": {"source": "test"}
                }
            }
        ]
        mock_session.run.return_value = mock_result

        details = await neo4j_service.get_node_details("node1")

        assert details is not None
        assert "id" in details
        assert "content" in details
        assert "type" in details

    @pytest.mark.asyncio
    async def test_search_knowledge_graph_no_results(self, neo4j_service, mock_driver, mock_session):
        """Test knowledge graph search with no results."""
        # Mock session and empty results
        mock_driver.session.return_value.__aenter__.return_value = mock_session
        
        mock_result = Mock()
        mock_result.data.return_value = []
        mock_session.run.return_value = mock_result

        results = await neo4j_service.search_knowledge_graph("nonexistent query", 5)

        assert isinstance(results, list)
        assert len(results) == 0

    @pytest.mark.asyncio
    async def test_search_vector_store_no_results(self, neo4j_service, mock_driver, mock_session):
        """Test vector store search with no results."""
        # Mock session and empty results
        mock_driver.session.return_value.__aenter__.return_value = mock_session
        
        mock_result = Mock()
        mock_result.data.return_value = []
        mock_session.run.return_value = mock_result

        results = await neo4j_service.search_vector_store("nonexistent query", 5)

        assert isinstance(results, list)
        assert len(results) == 0

    @pytest.mark.asyncio
    async def test_connection_error_handling(self, neo4j_service, mock_driver):
        """Test handling of connection errors."""
        # Mock driver to raise connection error
        mock_driver.session.side_effect = Exception("Connection failed")

        with pytest.raises(Exception):
            await neo4j_service.search_knowledge_graph("test query", 5)

    @pytest.mark.asyncio
    async def test_query_error_handling(self, neo4j_service, mock_driver, mock_session):
        """Test handling of query errors."""
        # Mock session to raise query error
        mock_driver.session.return_value.__aenter__.return_value = mock_session
        mock_session.run.side_effect = Exception("Query failed")

        with pytest.raises(Exception):
            await neo4j_service.search_knowledge_graph("test query", 5)

    @pytest.mark.asyncio
    async def test_max_results_limit(self, neo4j_service, mock_driver, mock_session):
        """Test that max_results limit is respected."""
        # Mock session and results
        mock_driver.session.return_value.__aenter__.return_value = mock_session
        
        mock_result = Mock()
        mock_result.data.return_value = [
            {"node": {"id": f"node{i}", "content": f"Content {i}"}, "score": 0.9 - i*0.1}
            for i in range(10)
        ]
        mock_session.run.return_value = mock_result

        results = await neo4j_service.search_knowledge_graph("test query", 3)

        assert len(results) <= 3

    @pytest.mark.asyncio
    async def test_result_ordering_by_score(self, neo4j_service, mock_driver, mock_session):
        """Test that results are ordered by score."""
        # Mock session and results with different scores
        mock_driver.session.return_value.__aenter__.return_value = mock_session
        
        mock_result = Mock()
        mock_result.data.return_value = [
            {"node": {"id": "node1", "content": "Content 1"}, "score": 0.5},
            {"node": {"id": "node2", "content": "Content 2"}, "score": 0.9},
            {"node": {"id": "node3", "content": "Content 3"}, "score": 0.7}
        ]
        mock_session.run.return_value = mock_result

        results = await neo4j_service.search_knowledge_graph("test query", 5)

        # Results should be ordered by score (descending)
        scores = [result["score"] for result in results]
        assert scores == sorted(scores, reverse=True)

    @pytest.mark.asyncio
    async def test_close_connection(self, neo4j_service, mock_driver):
        """Test closing Neo4j connection."""
        await neo4j_service.close()
        mock_driver.close.assert_called_once()


@pytest.mark.integration
class TestNeo4jServiceIntegration:
    """Integration tests for Neo4j service (requires actual Neo4j instance)."""

    @pytest.mark.asyncio
    async def test_real_connection(self):
        """Test connection to real Neo4j instance (if available)."""
        # This test would require a real Neo4j instance
        # For now, we'll skip it in CI/CD environments
        if os.environ.get("CI"):
            pytest.skip("Skipping integration test in CI environment")
        
        # Test would go here if Neo4j instance is available
        pass
