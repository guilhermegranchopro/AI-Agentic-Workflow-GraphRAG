"""
Tests for Pydantic schemas and data validation.
"""

import pytest
from datetime import datetime
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.rag import RAGResponse, Source, GraphResponse
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
from pydantic import ValidationError


class TestChatRequest:
    """Test ChatRequest schema."""

    def test_valid_chat_request(self):
        """Test valid chat request creation."""
        request = ChatRequest(
            message="What is the UAE Civil Code?",
            strategy="hybrid",
            max_results=10
        )
        
        assert request.message == "What is the UAE Civil Code?"
        assert request.strategy == "hybrid"
        assert request.max_results == 10

    def test_chat_request_defaults(self):
        """Test chat request with default values."""
        request = ChatRequest(message="Test message")
        
        assert request.message == "Test message"
        assert request.strategy == "hybrid"  # Default
        assert request.max_results == 5      # Default

    def test_chat_request_invalid_strategy(self):
        """Test chat request with invalid strategy."""
        with pytest.raises(ValidationError):
            ChatRequest(
                message="Test message",
                strategy="invalid_strategy"
            )

    def test_chat_request_empty_message(self):
        """Test chat request with empty message."""
        with pytest.raises(ValidationError):
            ChatRequest(message="")

    def test_chat_request_negative_max_results(self):
        """Test chat request with negative max_results."""
        with pytest.raises(ValidationError):
            ChatRequest(
                message="Test message",
                max_results=-1
            )

    def test_chat_request_zero_max_results(self):
        """Test chat request with zero max_results."""
        with pytest.raises(ValidationError):
            ChatRequest(
                message="Test message",
                max_results=0
            )

    def test_chat_request_large_max_results(self):
        """Test chat request with very large max_results."""
        with pytest.raises(ValidationError):
            ChatRequest(
                message="Test message",
                max_results=1000
            )

    def test_chat_request_strategy_values(self):
        """Test all valid strategy values."""
        strategies = ["hybrid", "vector", "graph"]
        
        for strategy in strategies:
            request = ChatRequest(
                message="Test message",
                strategy=strategy
            )
            assert request.strategy == strategy

    def test_chat_request_serialization(self):
        """Test chat request serialization."""
        request = ChatRequest(
            message="Test message",
            strategy="vector",
            max_results=15
        )
        
        data = request.model_dump()
        assert data["message"] == "Test message"
        assert data["strategy"] == "vector"
        assert data["max_results"] == 15

    def test_chat_request_from_dict(self):
        """Test chat request creation from dictionary."""
        data = {
            "message": "Test message",
            "strategy": "graph",
            "max_results": 20
        }
        
        request = ChatRequest(**data)
        assert request.message == "Test message"
        assert request.strategy == "graph"
        assert request.max_results == 20


class TestChatResponse:
    """Test ChatResponse schema."""

    def test_valid_chat_response(self):
        """Test valid chat response creation."""
        sources = [
            Source(
                id="source1",
                content="Test content 1",
                score=0.9,
                type="article",
                metadata={"source": "test"}
            )
        ]
        
        response = ChatResponse(
            answer="Test answer",
            sources=sources,
            strategy_used="hybrid",
            processing_time=1.5
        )
        
        assert response.answer == "Test answer"
        assert len(response.sources) == 1
        assert response.strategy_used == "hybrid"
        assert response.processing_time == 1.5

    def test_chat_response_defaults(self):
        """Test chat response with default values."""
        response = ChatResponse(answer="Test answer")
        
        assert response.answer == "Test answer"
        assert response.sources == []  # Default
        assert response.strategy_used == "hybrid"  # Default
        assert response.processing_time == 0.0  # Default

    def test_chat_response_empty_answer(self):
        """Test chat response with empty answer."""
        with pytest.raises(ValidationError):
            ChatResponse(answer="")

    def test_chat_response_negative_processing_time(self):
        """Test chat response with negative processing time."""
        with pytest.raises(ValidationError):
            ChatResponse(
                answer="Test answer",
                processing_time=-1.0
            )

    def test_chat_response_serialization(self):
        """Test chat response serialization."""
        sources = [
            Source(
                id="source1",
                content="Test content",
                score=0.8,
                type="article"
            )
        ]
        
        response = ChatResponse(
            answer="Test answer",
            sources=sources,
            strategy_used="vector",
            processing_time=2.0
        )
        
        data = response.model_dump()
        assert data["answer"] == "Test answer"
        assert len(data["sources"]) == 1
        assert data["strategy_used"] == "vector"
        assert data["processing_time"] == 2.0


class TestSource:
    """Test Source schema."""

    def test_valid_source(self):
        """Test valid source creation."""
        source = Source(
            id="source1",
            content="Test content",
            score=0.85,
            type="article",
            metadata={"source": "test", "page": 1}
        )
        
        assert source.id == "source1"
        assert source.content == "Test content"
        assert source.score == 0.85
        assert source.type == "article"
        assert source.metadata["source"] == "test"
        assert source.metadata["page"] == 1

    def test_source_defaults(self):
        """Test source with default values."""
        source = Source(
            id="source1",
            content="Test content",
            score=0.8
        )
        
        assert source.id == "source1"
        assert source.content == "Test content"
        assert source.score == 0.8
        assert source.type == "unknown"  # Default
        assert source.metadata == {}  # Default

    def test_source_empty_id(self):
        """Test source with empty id."""
        with pytest.raises(ValidationError):
            Source(
                id="",
                content="Test content",
                score=0.8
            )

    def test_source_empty_content(self):
        """Test source with empty content."""
        with pytest.raises(ValidationError):
            Source(
                id="source1",
                content="",
                score=0.8
            )

    def test_source_invalid_score(self):
        """Test source with invalid score."""
        # Score should be between 0 and 1
        with pytest.raises(ValidationError):
            Source(
                id="source1",
                content="Test content",
                score=1.5
            )
        
        with pytest.raises(ValidationError):
            Source(
                id="source1",
                content="Test content",
                score=-0.1
            )

    def test_source_serialization(self):
        """Test source serialization."""
        source = Source(
            id="source1",
            content="Test content",
            score=0.9,
            type="document",
            metadata={"author": "John Doe"}
        )
        
        data = source.model_dump()
        assert data["id"] == "source1"
        assert data["content"] == "Test content"
        assert data["score"] == 0.9
        assert data["type"] == "document"
        assert data["metadata"]["author"] == "John Doe"


class TestRAGResponse:
    """Test RAGResponse schema."""

    def test_valid_rag_response(self):
        """Test valid RAG response creation."""
        sources = [
            Source(
                id="source1",
                content="Test content 1",
                score=0.9,
                type="article"
            ),
            Source(
                id="source2",
                content="Test content 2",
                score=0.8,
                type="document"
            )
        ]
        
        response = RAGResponse(
            query="Test query",
            results=sources,
            strategy="hybrid",
            total_results=2,
            processing_time=1.2
        )
        
        assert response.query == "Test query"
        assert len(response.results) == 2
        assert response.strategy == "hybrid"
        assert response.total_results == 2
        assert response.processing_time == 1.2

    def test_rag_response_defaults(self):
        """Test RAG response with default values."""
        response = RAGResponse(
            query="Test query",
            results=[]
        )
        
        assert response.query == "Test query"
        assert response.results == []
        assert response.strategy == "hybrid"  # Default
        assert response.total_results == 0  # Default
        assert response.processing_time == 0.0  # Default

    def test_rag_response_empty_query(self):
        """Test RAG response with empty query."""
        with pytest.raises(ValidationError):
            RAGResponse(
                query="",
                results=[]
            )

    def test_rag_response_negative_total_results(self):
        """Test RAG response with negative total_results."""
        with pytest.raises(ValidationError):
            RAGResponse(
                query="Test query",
                results=[],
                total_results=-1
            )

    def test_rag_response_serialization(self):
        """Test RAG response serialization."""
        sources = [
            Source(
                id="source1",
                content="Test content",
                score=0.85,
                type="article"
            )
        ]
        
        response = RAGResponse(
            query="Test query",
            results=sources,
            strategy="vector",
            total_results=1,
            processing_time=0.8
        )
        
        data = response.model_dump()
        assert data["query"] == "Test query"
        assert len(data["results"]) == 1
        assert data["strategy"] == "vector"
        assert data["total_results"] == 1
        assert data["processing_time"] == 0.8


class TestGraphResponse:
    """Test GraphResponse schema."""

    def test_valid_graph_response(self):
        """Test valid graph response creation."""
        response = GraphResponse(
            nodes=[
                {"id": "node1", "label": "Article", "properties": {"title": "Test"}},
                {"id": "node2", "label": "Concept", "properties": {"name": "Law"}}
            ],
            relationships=[
                {"source": "node1", "target": "node2", "type": "CONTAINS"}
            ],
            query="Test query",
            total_nodes=2,
            total_relationships=1
        )
        
        assert response.query == "Test query"
        assert len(response.nodes) == 2
        assert len(response.relationships) == 1
        assert response.total_nodes == 2
        assert response.total_relationships == 1

    def test_graph_response_defaults(self):
        """Test graph response with default values."""
        response = GraphResponse(query="Test query")
        
        assert response.query == "Test query"
        assert response.nodes == []  # Default
        assert response.relationships == []  # Default
        assert response.total_nodes == 0  # Default
        assert response.total_relationships == 0  # Default

    def test_graph_response_empty_query(self):
        """Test graph response with empty query."""
        with pytest.raises(ValidationError):
            GraphResponse(query="")

    def test_graph_response_serialization(self):
        """Test graph response serialization."""
        response = GraphResponse(
            query="Test query",
            nodes=[{"id": "node1", "label": "Article"}],
            relationships=[{"source": "node1", "target": "node2", "type": "RELATES"}],
            total_nodes=1,
            total_relationships=1
        )
        
        data = response.model_dump()
        assert data["query"] == "Test query"
        assert len(data["nodes"]) == 1
        assert len(data["relationships"]) == 1
        assert data["total_nodes"] == 1
        assert data["total_relationships"] == 1


class TestAnalysisRequest:
    """Test AnalysisRequest schema."""

    def test_valid_analysis_request(self):
        """Test valid analysis request creation."""
        request = AnalysisRequest(
            query="Analyze the UAE Civil Code",
            analysis_type="comprehensive",
            include_graph=True,
            max_depth=3
        )
        
        assert request.query == "Analyze the UAE Civil Code"
        assert request.analysis_type == "comprehensive"
        assert request.include_graph is True
        assert request.max_depth == 3

    def test_analysis_request_defaults(self):
        """Test analysis request with default values."""
        request = AnalysisRequest(query="Test query")
        
        assert request.query == "Test query"
        assert request.analysis_type == "basic"  # Default
        assert request.include_graph is False  # Default
        assert request.max_depth == 2  # Default

    def test_analysis_request_empty_query(self):
        """Test analysis request with empty query."""
        with pytest.raises(ValidationError):
            AnalysisRequest(query="")

    def test_analysis_request_invalid_analysis_type(self):
        """Test analysis request with invalid analysis type."""
        with pytest.raises(ValidationError):
            AnalysisRequest(
                query="Test query",
                analysis_type="invalid_type"
            )

    def test_analysis_request_negative_max_depth(self):
        """Test analysis request with negative max_depth."""
        with pytest.raises(ValidationError):
            AnalysisRequest(
                query="Test query",
                max_depth=-1
            )

    def test_analysis_request_serialization(self):
        """Test analysis request serialization."""
        request = AnalysisRequest(
            query="Test query",
            analysis_type="detailed",
            include_graph=True,
            max_depth=5
        )
        
        data = request.model_dump()
        assert data["query"] == "Test query"
        assert data["analysis_type"] == "detailed"
        assert data["include_graph"] is True
        assert data["max_depth"] == 5


class TestAnalysisResponse:
    """Test AnalysisResponse schema."""

    def test_valid_analysis_response(self):
        """Test valid analysis response creation."""
        response = AnalysisResponse(
            query="Test query",
            analysis="This is a comprehensive analysis.",
            insights=["Insight 1", "Insight 2"],
            graph_data={
                "nodes": [{"id": "node1", "label": "Concept"}],
                "relationships": []
            },
            processing_time=2.5
        )
        
        assert response.query == "Test query"
        assert response.analysis == "This is a comprehensive analysis."
        assert len(response.insights) == 2
        assert "nodes" in response.graph_data
        assert response.processing_time == 2.5

    def test_analysis_response_defaults(self):
        """Test analysis response with default values."""
        response = AnalysisResponse(
            query="Test query",
            analysis="Test analysis"
        )
        
        assert response.query == "Test query"
        assert response.analysis == "Test analysis"
        assert response.insights == []  # Default
        assert response.graph_data == {}  # Default
        assert response.processing_time == 0.0  # Default

    def test_analysis_response_empty_query(self):
        """Test analysis response with empty query."""
        with pytest.raises(ValidationError):
            AnalysisResponse(
                query="",
                analysis="Test analysis"
            )

    def test_analysis_response_empty_analysis(self):
        """Test analysis response with empty analysis."""
        with pytest.raises(ValidationError):
            AnalysisResponse(
                query="Test query",
                analysis=""
            )

    def test_analysis_response_serialization(self):
        """Test analysis response serialization."""
        response = AnalysisResponse(
            query="Test query",
            analysis="Test analysis",
            insights=["Key insight"],
            graph_data={"nodes": []},
            processing_time=1.0
        )
        
        data = response.model_dump()
        assert data["query"] == "Test query"
        assert data["analysis"] == "Test analysis"
        assert len(data["insights"]) == 1
        assert "nodes" in data["graph_data"]
        assert data["processing_time"] == 1.0
