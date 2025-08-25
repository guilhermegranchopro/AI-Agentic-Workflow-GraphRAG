"""
UAE Legal GraphRAG - Python FastAPI Backend
Advanced GraphRAG processing and AI agents
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, AsyncGenerator
import json
import asyncio
from datetime import datetime

from app.config import Settings
from app.services.orchestrator import PythonOrchestrator
from app.services.graphrag import AdvancedGraphRAG
from app.services.legal_analysis import LegalAnalysisService
from app.agents.multi_agent_system import MultiAgentSystem

# Initialize FastAPI app
app = FastAPI(
    title="UAE Legal GraphRAG Backend",
    description="Advanced legal research with sophisticated GraphRAG and AI agents",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
settings = Settings()
orchestrator = PythonOrchestrator()
graphrag_service = AdvancedGraphRAG()
legal_analysis_service = LegalAnalysisService()
multi_agent_system = MultiAgentSystem()

# Pydantic models
class QueryRequest(BaseModel):
    query: str
    mode: Optional[str] = "hybrid"
    max_results: Optional[int] = 10
    include_metadata: Optional[bool] = True

class AnalysisRequest(BaseModel):
    query: str
    scope: Optional[str] = None
    max_findings: Optional[int] = 20
    include_contradictions: Optional[bool] = True

class GraphRequest(BaseModel):
    query: Optional[str] = None
    node_types: Optional[List[str]] = None
    max_nodes: Optional[int] = 100

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "graphrag": await graphrag_service.health_check(),
            "neo4j": await orchestrator.neo4j_health(),
            "openai": await orchestrator.openai_health()
        }
    }

@app.get("/env/present")
async def env_present():
    """Environment variables presence check"""
    return {
        "neo4j": {
            "configured": settings.validate_neo4j(),
            "uri": bool(settings.neo4j.uri),
            "username": bool(settings.neo4j.user),
            "password": bool(settings.neo4j.password),
            "database": bool(settings.neo4j.database),
        },
        "azure_openai": {
            "configured": settings.validate_azure_openai(),
            "api_key": bool(settings.azure_openai.api_key),
            "endpoint": bool(settings.azure_openai.endpoint),
            "deployment": bool(settings.azure_openai.deployment),
            "api_version": bool(settings.azure_openai.api_version),
        }
    }

# Advanced GraphRAG endpoint
@app.post("/api/graphrag/query")
async def advanced_graphrag_query(request: QueryRequest):
    """Advanced GraphRAG query with semantic search and graph algorithms"""
    try:
        results = await graphrag_service.advanced_retrieve(
            query=request.query,
            mode=request.mode,
            max_results=request.max_results,
            include_metadata=request.include_metadata
        )
        return {
            "success": True,
            "results": results,
            "metadata": {
                "query": request.query,
                "mode": request.mode,
                "timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GraphRAG query failed: {str(e)}")

# Streaming multi-agent assistant
@app.post("/api/assistant/stream")
async def stream_assistant_response(request: QueryRequest):
    """Streaming multi-agent assistant with advanced reasoning"""
    
    async def generate_response() -> AsyncGenerator[str, None]:
        try:
            async for chunk in multi_agent_system.stream_response(request.query):
                yield f"data: {json.dumps(chunk)}\n\n"
        except Exception as e:
            error_chunk = {
                "type": "error",
                "data": {"message": f"Assistant error: {str(e)}"}
            }
            yield f"data: {json.dumps(error_chunk)}\n\n"
    
    return StreamingResponse(
        generate_response(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*"
        }
    )

# Advanced legal analysis
@app.post("/api/analysis/advanced")
async def advanced_legal_analysis(request: AnalysisRequest):
    """Advanced legal analysis with NLP and contradiction detection"""
    try:
        results = await legal_analysis_service.comprehensive_analysis(
            query=request.query,
            scope=request.scope,
            max_findings=request.max_findings,
            include_contradictions=request.include_contradictions
        )
        return {
            "success": True,
            "analysis": results,
            "metadata": {
                "query": request.query,
                "scope": request.scope,
                "timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Legal analysis failed: {str(e)}")

# Graph data with advanced algorithms
@app.post("/api/graph/advanced")
async def advanced_graph_data(request: GraphRequest):
    """Graph data with community detection and semantic clustering"""
    try:
        graph_data = await graphrag_service.get_advanced_graph_data(
            query=request.query,
            node_types=request.node_types,
            max_nodes=request.max_nodes
        )
        return {
            "success": True,
            "graph": graph_data,
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "algorithms_applied": ["community_detection", "semantic_clustering"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Graph data retrieval failed: {str(e)}")

# Orchestrator endpoint for complex workflows
@app.post("/api/orchestrator/execute")
async def execute_orchestrator(request: QueryRequest):
    """Execute complex multi-step legal research workflow"""
    try:
        results = await orchestrator.execute_workflow(
            query=request.query,
            mode=request.mode,
            max_results=request.max_results
        )
        return {
            "success": True,
            "workflow_results": results,
            "metadata": {
                "query": request.query,
                "timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Orchestrator execution failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True,
        log_level="info"
    )
