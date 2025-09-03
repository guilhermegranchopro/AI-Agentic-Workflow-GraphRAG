# UAE Legal GraphRAG - API Reference

## Overview

This document provides comprehensive API documentation for the UAE Legal GraphRAG system, including both the core GraphRAG API endpoints and the A2A Protocol implementation.

## Base URLs

- **Development**: http://localhost:8000
- **Production**: https://uae-legal-graphrag.azurewebsites.net

## Authentication

### Bearer Token Authentication
```http
Authorization: Bearer <your-token>
```

### API Key Authentication
```http
X-API-Key: <your-api-key>
```

## Core GraphRAG API Endpoints

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-08-01T12:00:00Z",
  "services": {
    "neo4j": "connected",
    "azure_openai": "connected",
    "faiss": "ready"
  }
}
```

### Graph Data
```http
GET /api/graph
```

**Query Parameters:**
- `limit` (optional): Maximum number of nodes to return (default: 100)
- `filter` (optional): Filter nodes by type or property

**Response:**
```json
{
  "nodes": [
    {
      "id": "law_001",
      "type": "law",
      "properties": {
        "name": "UAE Corporate Tax Law",
        "year": 2022,
        "status": "active"
      }
    }
  ],
  "edges": [
    {
      "source": "law_001",
      "target": "article_001",
      "type": "CONTAINS"
    }
  ]
}
```

### Chat/Assistant API
```http
POST /api/chat
```

**Request Body:**
```json
{
  "message": "What are the UAE Corporate Tax Law requirements?",
  "strategy": "auto",
  "conversation_id": "conv_123"
}
```

**Response:**
```json
{
  "response": "Based on the UAE Corporate Tax Law...",
  "conversation_id": "conv_123",
  "citations": [
    {
      "source": "UAE Corporate Tax Law Article 1",
      "relevance": 0.95
    }
  ],
  "metadata": {
    "strategy": "hybrid",
    "agents_used": ["local_graphrag", "global_graphrag"]
  }
}
```

### Legal Analysis API
```http
POST /api/analysis
```

**Request Body:**
```json
{
  "query": "Corporate Tax contradictions",
  "analysis_type": "contradictions",
  "max_depth": 3
}
```

**Response:**
```json
{
  "analysis": {
    "type": "contradictions",
    "findings": [
      {
        "issue": "Tax rate discrepancy",
        "severity": "high",
        "description": "Conflict between Article 3 and Article 7"
      }
    ]
  },
  "recommendations": [
    "Review Article 3 implementation",
    "Align with Article 7 requirements"
  ]
}
```

## A2A Protocol Endpoints

### Agent Discovery
```http
GET /.well-known/agent.json
```

**Response:** Public agent card with capabilities and endpoints

```http
GET /.well-known/agent
```

**Response:** Alternative discovery endpoint

```http
GET /.well-known/health
```

**Response:** Well-known health check

### Core A2A Protocol

#### Send Message
```http
POST /a2a/v1/message:send
```

**Request Body:**
```json
{
  "message": {
    "role": "user",
    "parts": [
      {
        "kind": "text",
        "text": "What are the UAE Data Protection Law requirements?"
      }
    ],
    "metadata": {
      "skill_id": "ai_assistant"
    }
  },
  "configuration": {
    "strategy": "hybrid",
    "max_results": 5
  }
}
```

**Response:**
```json
{
  "message": {
    "role": "agent",
    "parts": [
      {
        "kind": "text",
        "text": "Based on the UAE Data Protection Law..."
      }
    ],
    "metadata": {
      "skill_id": "ai_assistant",
      "workflow": "assistant_workflow"
    }
  }
}
```

#### Stream Messages
```http
POST /a2a/v1/message:stream
```

**Request Body:** Same as message:send

**Response:** Server-Sent Events (SSE) stream

#### Get Task Status
```http
GET /a2a/v1/tasks/{task_id}
```

**Response:**
```json
{
  "id": "task_123",
  "status": {
    "state": "completed",
    "progress": 100.0,
    "message": "Analysis completed"
  },
  "artifacts": [
    {
      "type": "analysis_result",
      "data": {...}
    }
  ]
}
```

#### Authenticated Agent Card
```http
GET /a2a/v1/card
```

**Headers:** Requires authentication

**Response:** Extended agent card with additional details

#### A2A Health Check
```http
GET /a2a/health
```

**Response:**
```json
{
  "status": "healthy",
  "protocol_version": "0.3.0",
  "endpoints": {
    "message:send": "available",
    "message:stream": "available",
    "tasks:get": "available"
  }
}
```

## Error Handling

### Standard Error Response
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request format",
    "details": {
      "field": "skill_id",
      "issue": "Required field missing"
    }
  },
  "timestamp": "2025-08-01T12:00:00Z"
}
```

### HTTP Status Codes
- **200**: Success
- **400**: Bad Request (validation error)
- **401**: Unauthorized (authentication required)
- **403**: Forbidden (insufficient permissions)
- **404**: Not Found
- **422**: Unprocessable Entity (semantic validation error)
- **500**: Internal Server Error

## Rate Limiting

- **Default**: 60 requests per minute
- **Headers**: 
  - `X-RateLimit-Limit`: Request limit
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Reset time

## Pagination

For endpoints returning multiple items:

**Query Parameters:**
- `page`: Page number (default: 1)
- `size`: Items per page (default: 20)

**Response Headers:**
- `X-Total-Count`: Total number of items
- `X-Page-Count`: Total number of pages

## Data Formats

### Supported Content Types
- **Request**: `application/json`
- **Response**: `application/json`
- **Streaming**: `text/event-stream`

### Date Format
All dates are in ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`

## SDK and Client Libraries

### Python Client
```python
import requests

base_url = "http://localhost:8000"
headers = {"Authorization": "Bearer your-token"}

# Send message
response = requests.post(
    f"{base_url}/a2a/v1/message:send",
    json={"message": {...}},
    headers=headers
)
```

### JavaScript/TypeScript Client
```typescript
const baseUrl = "http://localhost:8000";
const headers = { "Authorization": "Bearer your-token" };

// Send message
const response = await fetch(`${baseUrl}/a2a/v1/message:send`, {
  method: 'POST',
  headers: { ...headers, 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: {...} })
});
```

## Testing

### Test Endpoints
- **Health Check**: `/health`
- **A2A Health**: `/a2a/health`
- **Agent Discovery**: `/.well-known/agent.json`

### Test Data
The system includes mock UAE legal data for testing purposes. Use the provided Neo4j dump file to populate your test database.

## Support

For API-related questions or issues:
1. Check the health endpoints for service status
2. Review error messages and status codes
3. Consult the A2A Protocol documentation
4. Check system logs for detailed error information
