from typing import Dict, Any, Optional
from fastapi import HTTPException, status


class GraphRAGError(Exception):
    """Base exception for GraphRAG application."""
    
    def __init__(self, message: str, error_code: str = None, details: Dict[str, Any] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}


class ConfigurationError(GraphRAGError):
    """Configuration-related errors."""
    pass


class Neo4jConnectionError(GraphRAGError):
    """Neo4j connection and query errors."""
    pass


class AzureOpenAIError(GraphRAGError):
    """Azure OpenAI API errors."""
    pass


class RAGError(GraphRAGError):
    """RAG retrieval and processing errors."""
    pass


class AgentError(GraphRAGError):
    """Agent execution errors."""
    pass


class A2AError(GraphRAGError):
    """A2A protocol errors."""
    pass


def map_exception_to_http(exception: GraphRAGError) -> HTTPException:
    """Map GraphRAG exceptions to HTTP exceptions."""
    if isinstance(exception, ConfigurationError):
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Configuration Error",
                "message": exception.message,
                "code": exception.error_code
            }
        )
    elif isinstance(exception, Neo4jConnectionError):
        return HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": "Database Error",
                "message": exception.message,
                "code": exception.error_code
            }
        )
    elif isinstance(exception, AzureOpenAIError):
        return HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": "AI Service Error",
                "message": exception.message,
                "code": exception.error_code
            }
        )
    elif isinstance(exception, RAGError):
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": "RAG Error",
                "message": exception.message,
                "code": exception.error_code
            }
        )
    elif isinstance(exception, AgentError):
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Agent Error",
                "message": exception.message,
                "code": exception.error_code
            }
        )
    elif isinstance(exception, A2AError):
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Communication Error",
                "message": exception.message,
                "code": exception.error_code
            }
        )
    else:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal Server Error",
                "message": str(exception)
            }
        )


async def handle_exception(exception: Exception) -> HTTPException:
    """Handle any exception and return appropriate HTTP response."""
    if isinstance(exception, GraphRAGError):
        return map_exception_to_http(exception)
    else:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal Server Error",
                "message": str(exception)
            }
        )
