"""
Well-Known Endpoints for A2A Protocol Discovery
===============================================

This module implements the well-known endpoints required by the A2A Protocol specification.
These endpoints must be accessible at /.well-known/ paths for agent discovery.
"""

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from loguru import logger

# Create well-known router
well_known_router = APIRouter(tags=["Well-Known"])


@well_known_router.get("/.well-known/agent.json")
async def agent_discovery():
    """A2A Protocol Agent Card for public discovery at /.well-known/agent.json"""
    
    # This is the public agent card that other agents can discover
    # Following the A2A Protocol specification exactly
    agent_card = {
        "protocolVersion": "0.3.0",
        "name": "uae-legal-graphrag",
        "description": "UAE Legal GraphRAG - AI-powered legal research and analysis system using GraphRAG and multi-agent workflows",
        "service": {
            "baseUrl": "https://uae-legal-graphrag.azurewebsites.net",
            "version": "1.0.0"
        },
        "transports": [
            {"transport": "HTTP+JSON"},
            {"transport": "JSON-RPC"}
        ],
        "capabilities": {
            "streaming": True,
            "longRunningTasks": True,
            "batchProcessing": False,
            "realTimeUpdates": True
        },
        "securitySchemes": [
            {
                "type": "http",
                "scheme": "bearer",
                "description": "Bearer token authentication for API access"
            },
            {
                "type": "apiKey",
                "scheme": "x-api-key",
                "description": "API key authentication for service-to-service communication"
            }
        ],
        "skills": [
            {
                "id": "local_graphrag",
                "name": "Local GraphRAG",
                "description": "Focused legal research using local graph neighborhood traversal",
                "inputModes": ["application/json"],
                "outputModes": ["application/json"],
                "parameters": {
                    "max_depth": {"type": "integer", "default": 2, "description": "Maximum traversal depth"},
                    "strategy": {"type": "string", "enum": ["local", "hybrid"], "description": "Search strategy"}
                }
            },
            {
                "id": "global_graphrag",
                "name": "Global GraphRAG",
                "description": "Comprehensive legal research using global graph analysis",
                "inputModes": ["application/json"],
                "outputModes": ["application/json"],
                "parameters": {
                    "max_results": {"type": "integer", "default": 10, "description": "Maximum results to return"},
                    "threshold": {"type": "number", "default": 0.7, "description": "Relevance threshold"}
                }
            },
            {
                "id": "drift_graphrag",
                "name": "DRIFT GraphRAG",
                "description": "Dynamic relevance and importance tracking for legal analysis",
                "inputModes": ["application/json"],
                "outputModes": ["application/json"],
                "parameters": {
                    "time_window": {"type": "integer", "default": 30, "description": "Time window in days"},
                    "importance_threshold": {"type": "number", "default": 0.8, "description": "Importance threshold"}
                }
            },
            {
                "id": "legal_analysis",
                "name": "Legal Analysis",
                "description": "Comprehensive legal analysis including contradiction detection and harmonization",
                "inputModes": ["application/json"],
                "outputModes": ["application/json"],
                "parameters": {
                    "analysis_type": {"type": "string", "enum": ["contradictions", "harmonizations", "compliance"], "description": "Type of analysis"},
                    "max_depth": {"type": "integer", "default": 3, "description": "Analysis depth"}
                }
            },
            {
                "id": "ai_assistant",
                "name": "AI Legal Assistant",
                "description": "AI-powered legal research assistant with citation support",
                "inputModes": ["application/json"],
                "outputModes": ["application/json"],
                "parameters": {
                    "strategy": {"type": "string", "enum": ["local", "global", "hybrid"], "description": "GraphRAG strategy"},
                    "max_results": {"type": "integer", "default": 5, "description": "Maximum results"}
                }
            }
        ],
        "metadata": {
            "jurisdiction": "UAE",
            "legal_domains": ["commercial", "civil", "criminal", "labor", "data_protection"],
            "graph_database": "Neo4j",
            "ai_model": "Azure OpenAI GPT-4o",
            "compliance": ["GDPR", "UAE Data Protection Law", "Commercial Companies Law"],
            "contact": {
                "email": "support@uae-legal-graphrag.com",
                "website": "https://uae-legal-graphrag.azurewebsites.net"
            },
            "documentation": {
                "api_docs": "https://uae-legal-graphrag.azurewebsites.net/docs",
                "a2a_spec": "https://a2a-protocol.org/dev/specification/"
            }
        }
    }
    
    return JSONResponse(
        content=agent_card,
        headers={
            "Content-Type": "application/json",
            "Cache-Control": "public, max-age=3600",  # Cache for 1 hour
            "Access-Control-Allow-Origin": "*"
        }
    )


@well_known_router.get("/.well-known/agent")
async def agent_discovery_alt():
    """Alternative agent discovery endpoint for compatibility."""
    return await agent_discovery()


@well_known_router.get("/.well-known/")
async def well_known_index():
    """Well-known endpoints index."""
    return {
        "endpoints": [
            {
                "path": "/.well-known/agent.json",
                "description": "A2A Protocol Agent Card",
                "content_type": "application/json"
            },
            {
                "path": "/.well-known/agent",
                "description": "Alternative agent discovery endpoint",
                "content_type": "application/json"
            }
        ],
        "protocol": "A2A",
        "version": "0.3.0",
        "specification": "https://a2a-protocol.org/dev/specification/"
    }


@well_known_router.get("/.well-known/health")
async def well_known_health():
    """Well-known health check endpoint."""
    return {
        "status": "healthy",
        "protocol": "A2A",
        "version": "0.3.0",
        "timestamp": "2024-01-01T00:00:00Z",
        "endpoints": [
            "/.well-known/agent.json",
            "/.well-known/agent",
            "/.well-known/health"
        ]
    }
