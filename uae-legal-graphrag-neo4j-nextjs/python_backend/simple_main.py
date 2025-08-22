"""
Simple working FastAPI backend for testing
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import time
import asyncio

app = FastAPI(title="Simple Legal GraphRAG Backend", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class TestRequest(BaseModel):
    query: str
    mode: str = "standard"

class GraphRAGQuery(BaseModel):
    query: str
    search_mode: str = "hybrid"
    max_results: int = 5

class AssistantRequest(BaseModel):
    messages: List[Dict[str, str]]

@app.get("/health")
async def health_check():
    return {"status": "healthy", "backend": "python_fastapi_simple"}

@app.post("/api/test")
async def test_endpoint(request: TestRequest):
    return {
        "success": True,
        "message": f"Python backend received query: {request.query}",
        "mode": request.mode
    }

@app.post("/api/graphrag/query")
async def graphrag_query(request: GraphRAGQuery):
    """Simple GraphRAG query endpoint"""
    
    # Simulate processing
    await asyncio.sleep(1.0)
    
    passages = [
        {
            "text": f"🔍 Advanced GraphRAG Analysis: '{request.query}'\n\nThis demonstrates the Python backend's advanced capabilities including:\n• Semantic embeddings with sentence-transformers\n• Graph community detection algorithms\n• Multi-agent legal analysis\n• Advanced NLP for legal text processing",
            "node_id": "python_graphrag_001",
            "score": 0.95,
            "metadata": {
                "backend": "python_fastapi",
                "search_mode": request.search_mode,
                "advanced_processing": True,
                "techniques": ["semantic_search", "community_detection", "legal_nlp"]
            }
        },
        {
            "text": f"🧠 Python Backend Capabilities:\n\n1. **Semantic Search**: Uses sentence-transformers for deep understanding\n2. **Graph Algorithms**: NetworkX for sophisticated graph analysis\n3. **Legal NLP**: Specialized legal text processing\n4. **Multi-Agent System**: Collaborative AI agents for comprehensive analysis",
            "node_id": "python_capabilities_002", 
            "score": 0.88,
            "metadata": {
                "backend": "python_fastapi",
                "category": "system_capabilities",
                "ml_enhanced": True
            }
        }
    ]
    
    agent_results = [
        {
            "agent": "PythonGraphRAGAgent",
            "findings": {
                "analysis": f"Processed query '{request.query}' using advanced Python ML stack",
                "capabilities": [
                    "sentence-transformers embeddings",
                    "NetworkX graph algorithms", 
                    "Advanced legal pattern recognition",
                    "Multi-modal semantic search"
                ],
                "performance": {
                    "processing_time": 1.0,
                    "accuracy": 0.95,
                    "model_confidence": 0.92
                }
            },
            "confidence": 0.95
        }
    ]
    
    return {
        "passages": passages,
        "agent_results": agent_results,
        "metadata": {
            "query": request.query,
            "search_mode": request.search_mode,
            "total_results": len(passages),
            "backend": "python_fastapi_enhanced",
            "timestamp": time.time()
        }
    }

@app.post("/api/assistant/stream")
async def assistant_stream(request: AssistantRequest):
    """Streaming assistant with progress updates"""
    
    async def generate():
        # Get latest message
        latest_msg = request.messages[-1] if request.messages else {"content": "test"}
        query = latest_msg.get("content", "test query")
        
        # Progress stages
        stages = [
            {"stage": "initialization", "message": "🚀 Initializing Python backend..."},
            {"stage": "analysis", "message": "🔍 Analyzing legal context with advanced NLP..."},
            {"stage": "agents", "message": "🤖 Multi-agent system processing..."},
            {"stage": "synthesis", "message": "🧠 Synthesizing comprehensive response..."}
        ]
        
        for stage_info in stages:
            yield f"data: {json.dumps({'type': 'progress', 'data': stage_info})}\n\n"
            await asyncio.sleep(0.8)
        
        # Final response
        final_response = {
            "passages": [
                {
                    "text": f"✨ **Advanced Python Backend Response**\n\nQuery: '{query}'\n\n**Analysis Results:**\n• Applied sentence-transformers for semantic understanding\n• Used NetworkX algorithms for graph analysis\n• Employed multi-agent AI system for comprehensive research\n• Integrated legal domain expertise\n\n**Python Advantages:**\n• Superior ML/AI ecosystem\n• Advanced NLP capabilities\n• Sophisticated graph algorithms\n• Real-time streaming responses",
                    "node_id": "python_stream_response",
                    "score": 0.96,
                    "metadata": {
                        "backend": "python_streaming",
                        "advanced_features": True,
                        "response_time": 3.2
                    }
                }
            ],
            "agent_results": [
                {
                    "agent": "PythonStreamingAgent",
                    "findings": {
                        "analysis": "Successfully demonstrated Python backend streaming capabilities",
                        "features_used": [
                            "AsyncIO for concurrent processing",
                            "Server-Sent Events (SSE) streaming",
                            "Real-time progress updates",
                            "Advanced AI processing pipeline"
                        ]
                    },
                    "confidence": 0.96
                }
            ],
            "metadata": {
                "backend": "python_fastapi_streaming",
                "query": query,
                "total_processing_time": 3.2,
                "timestamp": time.time()
            }
        }
        
        yield f"data: {json.dumps(final_response)}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache", 
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
