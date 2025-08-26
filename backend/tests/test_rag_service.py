"""
Tests for RAG service functionality.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.rag.rag_service import RAGService
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.rag import RAGResponse, Source


@pytest.fixture
def rag_service():
    """Create RAG service instance."""
    return RAGService()


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client."""
    with patch("app.services.openai_service.OpenAIClient") as mock:
        client = Mock()
        client.generate_response = AsyncMock(return_value="Test response")
        mock.return_value = client
        yield client


@pytest.fixture
def mock_neo4j_service():
    """Mock Neo4j service."""
    with patch("app.services.neo4j_service.Neo4jService") as mock:
        service = Mock()
        service.search_knowledge_graph = AsyncMock(return_value=[])
        service.search_vector_store = AsyncMock(return_value=[])
        mock.return_value = service
        yield service


class TestRAGService:
    """Test RAG service functionality."""

    @pytest.mark.asyncio
    async def test_rag_service_initialization(self, rag_service):
        """Test RAG service initialization."""
        assert rag_service is not None
        assert hasattr(rag_service, 'openai_client')
        assert hasattr(rag_service, 'neo4j_service')

    @pytest.mark.asyncio
    async def test_hybrid_strategy(self, rag_service, mock_openai_client, mock_neo4j_service):
        """Test hybrid RAG strategy."""
        # Mock responses
        mock_neo4j_service.search_knowledge_graph.return_value = [
            {"id": "kg_1", "content": "Knowledge graph result", "score": 0.9}
        ]
        mock_neo4j_service.search_vector_store.return_value = [
            {"id": "vec_1", "content": "Vector search result", "score": 0.8}
        ]
        mock_openai_client.generate_response.return_value = "Combined response"

        request = ChatRequest(
            message="Test query",
            strategy="hybrid",
            max_results=5
        )

        response = await rag_service.process_chat_request(request)

        assert response is not None
        assert isinstance(response, ChatResponse)
        assert response.answer == "Combined response"
        assert len(response.sources) > 0

    @pytest.mark.asyncio
    async def test_vector_only_strategy(self, rag_service, mock_openai_client, mock_neo4j_service):
        """Test vector-only RAG strategy."""
        mock_neo4j_service.search_vector_store.return_value = [
            {"id": "vec_1", "content": "Vector result", "score": 0.85}
        ]
        mock_openai_client.generate_response.return_value = "Vector-based response"

        request = ChatRequest(
            message="Test query",
            strategy="vector",
            max_results=3
        )

        response = await rag_service.process_chat_request(request)

        assert response is not None
        assert response.answer == "Vector-based response"
        mock_neo4j_service.search_vector_store.assert_called_once()
        mock_neo4j_service.search_knowledge_graph.assert_not_called()

    @pytest.mark.asyncio
    async def test_graph_only_strategy(self, rag_service, mock_openai_client, mock_neo4j_service):
        """Test graph-only RAG strategy."""
        mock_neo4j_service.search_knowledge_graph.return_value = [
            {"id": "kg_1", "content": "Graph result", "score": 0.95}
        ]
        mock_openai_client.generate_response.return_value = "Graph-based response"

        request = ChatRequest(
            message="Test query",
            strategy="graph",
            max_results=3
        )

        response = await rag_service.process_chat_request(request)

        assert response is not None
        assert response.answer == "Graph-based response"
        mock_neo4j_service.search_knowledge_graph.assert_called_once()
        mock_neo4j_service.search_vector_store.assert_not_called()

    @pytest.mark.asyncio
    async def test_no_results_found(self, rag_service, mock_openai_client, mock_neo4j_service):
        """Test behavior when no results are found."""
        mock_neo4j_service.search_knowledge_graph.return_value = []
        mock_neo4j_service.search_vector_store.return_value = []
        mock_openai_client.generate_response.return_value = "No relevant information found"

        request = ChatRequest(
            message="Test query",
            strategy="hybrid",
            max_results=5
        )

        response = await rag_service.process_chat_request(request)

        assert response is not None
        assert "No relevant information" in response.answer
        assert len(response.sources) == 0

    @pytest.mark.asyncio
    async def test_error_handling(self, rag_service, mock_neo4j_service):
        """Test error handling in RAG service."""
        mock_neo4j_service.search_knowledge_graph.side_effect = Exception("Database error")

        request = ChatRequest(
            message="Test query",
            strategy="hybrid",
            max_results=5
        )

        with pytest.raises(Exception):
            await rag_service.process_chat_request(request)

    @pytest.mark.asyncio
    async def test_source_formatting(self, rag_service, mock_openai_client, mock_neo4j_service):
        """Test that sources are properly formatted."""
        mock_neo4j_service.search_knowledge_graph.return_value = [
            {
                "id": "test_1",
                "title": "Test Document",
                "content": "Test content",
                "score": 0.9,
                "url": "http://example.com"
            }
        ]
        mock_openai_client.generate_response.return_value = "Test response"

        request = ChatRequest(
            message="Test query",
            strategy="graph",
            max_results=5,
            include_sources=True
        )

        response = await rag_service.process_chat_request(request)

        assert len(response.sources) == 1
        source = response.sources[0]
        assert source.id == "test_1"
        assert source.title == "Test Document"
        assert source.content == "Test content"
        assert source.relevance_score == 0.9

    @pytest.mark.asyncio
    async def test_max_results_limit(self, rag_service, mock_openai_client, mock_neo4j_service):
        """Test that max_results limit is respected."""
        # Return more results than requested
        mock_neo4j_service.search_knowledge_graph.return_value = [
            {"id": f"kg_{i}", "content": f"Result {i}", "score": 0.9 - i*0.1}
            for i in range(10)
        ]
        mock_openai_client.generate_response.return_value = "Limited response"

        request = ChatRequest(
            message="Test query",
            strategy="graph",
            max_results=3
        )

        response = await rag_service.process_chat_request(request)

        assert len(response.sources) <= 3

    @pytest.mark.asyncio
    async def test_streaming_response(self, rag_service, mock_openai_client, mock_neo4j_service):
        """Test streaming response generation."""
        mock_neo4j_service.search_knowledge_graph.return_value = [
            {"id": "kg_1", "content": "Test content", "score": 0.9}
        ]
        mock_openai_client.generate_response.return_value = "Streaming response"

        request = ChatRequest(
            message="Test query",
            strategy="hybrid",
            max_results=5,
            stream=True
        )

        # This would need to be implemented in the actual service
        # For now, just test that the request is processed
        response = await rag_service.process_chat_request(request)
        assert response is not None
