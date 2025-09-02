# **🤖 A2A Protocol Implementation - UAE Legal GraphRAG**

## **📋 Overview**

This document describes the **official A2A Protocol** implementation in the UAE Legal GraphRAG system. We have implemented the complete A2A Protocol specification following the official standards at [a2a-protocol.org](https://a2a-protocol.org/dev/specification/).

---

## **🔗 A2A Protocol Endpoints**

### **1. Agent Discovery (Public)**
- **`GET /.well-known/agent.json`** - Public agent card for discovery
- **`GET /.well-known/agent`** - Alternative discovery endpoint
- **`GET /.well-known/`** - Well-known endpoints index
- **`GET /.well-known/health`** - Well-known health check

### **2. Core A2A Protocol Endpoints**
- **`POST /a2a/v1/message:send`** - Send messages to agents
- **`POST /a2a/v1/message:stream`** - Stream task updates (SSE)
- **`GET /a2a/v1/tasks/{task_id}`** - Get task status
- **`GET /a2a/v1/card`** - Authenticated agent card
- **`GET /a2a/health`** - A2A Protocol health check

---

## **🎯 Agent Card (Agent Discovery)**

### **Public Agent Card Structure**
```json
{
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
    "streaming": true,
    "longRunningTasks": true,
    "batchProcessing": false,
    "realTimeUpdates": true
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
  "skills": [...],
  "metadata": {...}
}
```

### **Available Skills**

#### **1. Local GraphRAG (`local_graphrag`)**
- **Purpose**: Focused legal research using local graph neighborhood traversal
- **Parameters**:
  - `max_depth`: Maximum traversal depth (default: 2)
  - `strategy`: Search strategy (local, hybrid)

#### **2. Global GraphRAG (`global_graphrag`)**
- **Purpose**: Comprehensive legal research using global graph analysis
- **Parameters**:
  - `max_results`: Maximum results to return (default: 10)
  - `threshold`: Relevance threshold (default: 0.7)

#### **3. DRIFT GraphRAG (`drift_graphrag`)**
- **Purpose**: Dynamic relevance and importance tracking for legal analysis
- **Parameters**:
  - `time_window`: Time window in days (default: 30)
  - `importance_threshold`: Importance threshold (default: 0.8)

#### **4. Legal Analysis (`legal_analysis`)**
- **Purpose**: Comprehensive legal analysis including contradiction detection and harmonization
- **Parameters**:
  - `analysis_type`: Type of analysis (contradictions, harmonizations, compliance)
  - `max_depth`: Analysis depth (default: 3)

#### **5. AI Legal Assistant (`ai_assistant`)**
- **Purpose**: AI-powered legal research assistant with citation support
- **Parameters**:
  - `strategy`: GraphRAG strategy (local, global, hybrid)
  - `max_results`: Maximum results (default: 5)

---

## **📨 Message:Send Implementation**

### **Request Format**
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

### **Response Format**
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
      "workflow": "assistant_workflow",
      "citations_count": 3,
      "nodes_count": 5,
      "edges_count": 8
    }
  },
  "metadata": {
    "processing_time": 2.5,
    "strategy_used": "hybrid"
  }
}
```

---

## **🔄 Message:Stream Implementation**

### **Server-Sent Events (SSE)**
The system supports real-time streaming updates for long-running tasks:

```javascript
// Client-side SSE implementation
const eventSource = new EventSource('/a2a/v1/message:stream');

eventSource.onmessage = function(event) {
  const data = JSON.parse(event.data);
  console.log('Task update:', data);
  
  if (data.status.state === 'completed') {
    eventSource.close();
  }
};
```

### **Streaming Events**
```json
{
  "id": "task_123",
  "status": {
    "state": "working",
    "progress": 75.0,
    "message": "Analyzing legal contradictions...",
    "timestamp": "2024-01-01T12:00:00Z"
  },
  "artifacts": [],
  "metadata": {
    "skill_id": "legal_analysis",
    "workflow": "analysis_workflow"
  }
}
```

---

## **📊 Tasks:Get Implementation**

### **Task Status Endpoint**
```http
GET /a2a/v1/tasks/{task_id}
```

### **Task States**
- **`pending`**: Task is queued but not started
- **`working`**: Task is currently executing
- **`completed`**: Task has finished successfully
- **`failed`**: Task encountered an error
- **`cancelled`**: Task was cancelled by user

### **Task Response**
```json
{
  "id": "task_123",
  "status": {
    "state": "completed",
    "progress": 100.0,
    "message": "Legal analysis completed successfully",
    "timestamp": "2024-01-01T12:05:00Z"
  },
  "artifacts": [
    {
      "type": "contradictions",
      "data": [...],
      "mimeType": "application/json"
    }
  ],
  "metadata": {
    "skill_id": "legal_analysis",
    "processing_time": 5.2
  }
}
```

---

## **🔒 Security & Authentication**

### **Security Schemes**
1. **Bearer Token Authentication**
   - HTTP Authorization header with Bearer token
   - Used for API access and user authentication

2. **API Key Authentication**
   - X-API-Key header for service-to-service communication
   - Used for inter-agent communication

### **Authentication Headers**
```http
# Bearer token
Authorization: Bearer <your-token>

# API key
X-API-Key: <your-api-key>
```

---

## **🌐 Integration Examples**

### **1. Python Client Example**
```python
import requests
import json

# Discover agent capabilities
response = requests.get("https://uae-legal-graphrag.azurewebsites.net/.well-known/agent.json")
agent_card = response.json()

# Send AI Assistant request
message_request = {
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

response = requests.post(
    "https://uae-legal-graphrag.azurewebsites.net/a2a/v1/message:send",
    json=message_request,
    headers={"Authorization": "Bearer <your-token>"}
)

result = response.json()
print(f"AI Response: {result['message']['parts'][0]['text']}")
```

### **2. JavaScript Client Example**
```javascript
// Discover agent capabilities
const agentCard = await fetch('/.well-known/agent.json').then(r => r.json());

// Send Legal Analysis request
const analysisRequest = {
  message: {
    role: "user",
    parts: [
      {
        kind: "data",
        data: {
          query: "Data Protection Law contradictions",
          analysis_type: "contradictions",
          max_depth: 3
        }
      }
    ],
    metadata: {
      skill_id: "legal_analysis"
    }
  }
};

const response = await fetch('/a2a/v1/message:send', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <your-token>'
  },
  body: JSON.stringify(analysisRequest)
});

const result = await response.json();
console.log('Analysis result:', result);
```

---

## **🔍 A2A Protocol Compliance**

### **Compliance Checklist**
- ✅ **Agent Card**: Public discovery at `/.well-known/agent.json`
- ✅ **Message:Send**: Synchronous message handling
- ✅ **Message:Stream**: Server-Sent Events for streaming
- ✅ **Tasks:Get**: Task status polling
- ✅ **Transport**: HTTP+JSON and JSON-RPC support
- ✅ **Security**: Bearer token and API key authentication
- ✅ **Capabilities**: Streaming, long-running tasks, real-time updates

### **Protocol Version**
- **Current Version**: 0.3.0
- **Specification**: [a2a-protocol.org](https://a2a-protocol.org/dev/specification/)
- **Compliance**: Full A2A Protocol compliance

---

## **🚀 Testing A2A Protocol**

### **1. Test Agent Discovery**
```bash
curl https://uae-legal-graphrag.azurewebsites.net/.well-known/agent.json
```

### **2. Test Message:Send**
```bash
curl -X POST https://uae-legal-graphrag.azurewebsites.net/a2a/v1/message:send \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-token>" \
  -d '{
    "message": {
      "role": "user",
      "parts": [{"kind": "text", "text": "Hello"}],
      "metadata": {"skill_id": "ai_assistant"}
    }
  }'
```

### **3. Test Health Check**
```bash
curl https://uae-legal-graphrag.azurewebsites.net/a2a/health
```

---

## **📚 Additional Resources**

### **A2A Protocol Documentation**
- [Official Specification](https://a2a-protocol.org/dev/specification/)
- [Python SDK](https://github.com/a2aproject/a2a-python)
- [A2A Inspector](https://github.com/a2aproject/a2a-inspector)
- [Google Cloud A2A](https://cloud.google.com/run/docs/verify-deployment-a2a-agents)

### **UAE Legal GraphRAG A2A**
- **Base URL**: `https://uae-legal-graphrag.azurewebsites.net`
- **Agent Card**: `/.well-known/agent.json`
- **API Documentation**: `/docs`
- **Health Check**: `/a2a/health`

---

## **🎯 Summary**

The UAE Legal GraphRAG system now implements the **complete A2A Protocol** with:

1. **Full Protocol Compliance**: All required endpoints and capabilities
2. **Agent Discovery**: Public agent card for interoperability
3. **Message Handling**: Synchronous and streaming message support
4. **Task Management**: Long-running task support with status tracking
5. **Security**: Multiple authentication schemes
6. **Skills**: Five specialized legal AI skills
7. **Streaming**: Real-time updates via Server-Sent Events

This implementation enables **true agent-to-agent communication** following industry standards, making the UAE Legal GraphRAG system interoperable with other A2A-compliant agents and platforms.
