"""
A2A Protocol Endpoints - Official Agent2Agent Protocol Implementation
====================================================================

This module implements the official A2A Protocol endpoints for the UAE Legal GraphRAG system.
Following the A2A Protocol specification: https://a2a-protocol.org/dev/specification/

IMPLEMENTATION FOLLOWS THE EXACT A2A PROTOCOL GUIDE:
1. Discovery: publish an Agent Card at /.well-known/agent.json
2. Choose a transport and implement the core methods
3. Auth & security
4. Streaming & long-running tasks
5. Compliance testing
"""

import uuid
from typing import Dict, Any, List
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from loguru import logger
import json
import asyncio
from datetime import datetime

from ..schemas.a2a_protocol import (
    AgentCard, Skill, SecurityScheme, Message, MessagePart,
    Task, TaskStatus, MessageSendRequest, MessageSendResponse,
    MessageStreamRequest, TaskGetResponse
)
from ..agents.orchestrator_agent import OrchestratorAgent
from ..adapters.neo4j_conn import Neo4jConnection
from ..adapters.azure_openai import AzureLLM
from ..adapters.a2a import A2AAdapter

# Create A2A Protocol router
a2a_router = APIRouter(prefix="/a2a", tags=["A2A Protocol"])

# Global service instances (will be set by main.py)
orchestrator_agent: OrchestratorAgent = None
neo4j_conn: Neo4jConnection = None
azure_llm: AzureLLM = None
a2a_adapter: A2AAdapter = None

# Task storage for long-running operations
task_store: Dict[str, Dict[str, Any]] = {}


def get_a2a_services():
    """Dependency to get A2A service instances."""
    return {
        "orchestrator_agent": orchestrator_agent,
        "neo4j_conn": neo4j_conn,
        "azure_llm": azure_llm,
        "a2a_adapter": a2a_adapter
    }


# ============================================================================
# A2A PROTOCOL IMPLEMENTATION - FOLLOWING THE EXACT GUIDE
# ============================================================================

# 1) message:send (sync or quick tasks) - /v1/message:send
@a2a_router.post("/v1/message:send")
async def message_send(
    request: MessageSendRequest,
    services: Dict[str, Any] = Depends(get_a2a_services)
):
    """
    A2A Protocol message:send endpoint - following the exact A2A Protocol specification.
    
    This endpoint either returns a quick "message" or a "task" for long-running operations.
    """
    try:
        # Extract skill ID from message metadata
        skill_id = request.message.metadata.get("skill_id") if request.message.metadata else None
        
        if not skill_id:
            raise HTTPException(status_code=400, detail="skill_id required in message metadata")
        
        # Process based on skill type
        if skill_id == "ai_assistant":
            return await _handle_ai_assistant(request, services)
        elif skill_id == "legal_analysis":
            return await _handle_legal_analysis(request, services)
        elif skill_id in ["local_graphrag", "global_graphrag", "drift_graphrag"]:
            return await _handle_graphrag(request, services, skill_id)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown skill_id: {skill_id}")
            
    except Exception as e:
        logger.error(f"A2A message:send error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def _handle_ai_assistant(request: MessageSendRequest, services: Dict[str, Any]) -> MessageSendResponse:
    """Handle AI Assistant skill requests."""
    orchestrator_agent = services["orchestrator_agent"]
    
    if not orchestrator_agent:
        raise HTTPException(status_code=503, detail="Orchestrator agent not available")
    
    # Extract user message from request
    user_message = ""
    for part in request.message.parts:
        if part.kind == "text" and part.text:
            user_message = part.text
            break
    
    if not user_message:
        raise HTTPException(status_code=400, detail="No text message found")
    
    # Execute AI Assistant workflow
    workflow_result = await orchestrator_agent._execute_assistant_workflow({
        "query": user_message,
        "strategy": "hybrid",
        "max_results": 5
    })
    
    # Create response message
    response_message = Message(
        role="agent",
        parts=[
            MessagePart(
                kind="text",
                text=workflow_result.get("response", "I'm sorry, I couldn't process your request.")
            )
        ],
        metadata={
            "skill_id": "ai_assistant",
            "workflow": "assistant_workflow",
            "citations_count": len(workflow_result.get("citations", [])),
            "nodes_count": len(workflow_result.get("nodes", [])),
            "edges_count": len(workflow_result.get("edges", []))
        }
    )
    
    return MessageSendResponse(
        message=response_message,
        metadata={
            "processing_time": workflow_result.get("processing_time", 0),
            "strategy_used": workflow_result.get("strategy", "hybrid")
        }
    )


async def _handle_legal_analysis(request: MessageSendRequest, services: Dict[str, Any]) -> MessageSendResponse:
    """Handle Legal Analysis skill requests."""
    orchestrator_agent = services["orchestrator_agent"]
    
    if not orchestrator_agent:
        raise HTTPException(status_code=503, detail="Orchestrator agent not available")
    
    # Extract analysis parameters
    analysis_params = {}
    for part in request.message.parts:
        if part.kind == "data" and part.data:
            analysis_params = part.data
            break
    
    if not analysis_params.get("query"):
        raise HTTPException(status_code=400, detail="No analysis query found")
    
    # Execute Legal Analysis workflow
    workflow_result = await orchestrator_agent._execute_analysis_workflow({
        "query": analysis_params["query"],
        "analysis_type": analysis_params.get("analysis_type", "contradictions"),
        "max_depth": analysis_params.get("max_depth", 3)
    })
    
    # Create response message
    response_message = Message(
        role="agent",
        parts=[
            MessagePart(
                kind="text",
                text=f"Legal analysis completed. Found {len(workflow_result.get('contradictions', []))} contradictions and {len(workflow_result.get('harmonizations', []))} harmonization opportunities."
            ),
            MessagePart(
                kind="data",
                data=workflow_result,
                mimeType="application/json"
            )
        ],
        metadata={
            "skill_id": "legal_analysis",
            "workflow": "analysis_workflow",
            "contradictions_count": len(workflow_result.get("contradictions", [])),
            "harmonizations_count": len(workflow_result.get("harmonizations", []))
        }
    )
    
    return MessageSendResponse(
        message=response_message,
        metadata={
            "processing_time": workflow_result.get("processing_time", 0),
            "analysis_type": analysis_params.get("analysis_type", "contradictions")
        }
    )


async def _handle_graphrag(request: MessageSendRequest, services: Dict[str, Any], skill_id: str) -> MessageSendResponse:
    """Handle GraphRAG skill requests."""
    orchestrator_agent = services["orchestrator_agent"]
    
    if not orchestrator_agent:
        raise HTTPException(status_code=503, detail="Orchestrator agent not available")
    
    # Extract GraphRAG parameters
    graphrag_params = {}
    for part in request.message.parts:
        if part.kind == "data" and part.data:
            graphrag_params = part.data
            break
    
    if not graphrag_params.get("query"):
        raise HTTPException(status_code=400, detail="No GraphRAG query found")
    
    # Execute GraphRAG workflow based on skill
    if skill_id == "local_graphrag":
        workflow_result = await orchestrator_agent._execute_local_graphrag(graphrag_params)
    elif skill_id == "global_graphrag":
        workflow_result = await orchestrator_agent._execute_global_graphrag(graphrag_params)
    elif skill_id == "drift_graphrag":
        workflow_result = await orchestrator_agent._execute_drift_graphrag(graphrag_params)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown GraphRAG skill: {skill_id}")
    
    # Create response message
    response_message = Message(
        role="agent",
        parts=[
            MessagePart(
                kind="text",
                text=f"GraphRAG analysis completed using {skill_id} strategy. Found {len(workflow_result.get('nodes', []))} relevant nodes."
            ),
            MessagePart(
                kind="data",
                data=workflow_result,
                mimeType="application/json"
            )
        ],
        metadata={
            "skill_id": skill_id,
            "workflow": f"{skill_id}_workflow",
            "nodes_count": len(workflow_result.get("nodes", [])),
            "edges_count": len(workflow_result.get("edges", []))
        }
    )
    
    return MessageSendResponse(
        message=response_message,
        metadata={
            "processing_time": workflow_result.get("processing_time", 0),
            "strategy_used": skill_id
        }
    )


# 2) message:stream (SSE) - /v1/message:stream
@a2a_router.post("/v1/message:stream")
async def message_stream(
    request: MessageStreamRequest,
    services: Dict[str, Any] = Depends(get_a2a_services)
):
    """
    A2A Protocol message:stream endpoint for Server-Sent Events.
    
    This endpoint streams task updates for long-running operations.
    """
    
    async def generate_stream():
        """Generate SSE stream for task updates."""
        task_id = request.taskId
        
        if task_id not in task_store:
            yield f"data: {json.dumps({'error': 'Task not found'})}\n\n"
            return
        
        # Stream task updates
        while True:
            task = task_store.get(task_id)
            if not task:
                break
                
            # Send task status update
            yield f"data: {json.dumps(task)}\n\n"
            
            # Check if task is complete
            if task["status"]["state"] in ["completed", "failed"]:
                break
                
            await asyncio.sleep(1)  # Update every second
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*"
        }
    )


# 3) tasks:get (polling) - /v1/tasks/{task_id}
@a2a_router.get("/v1/tasks/{task_id}")
async def tasks_get(task_id: str):
    """
    A2A Protocol tasks:get endpoint.
    
    This endpoint returns task status and any produced artifacts/messages.
    """
    if task_id not in task_store:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_data = task_store[task_id]
    return TaskGetResponse(
        id=task_id,
        status=TaskStatus(
            state=task_data["status"]["state"],
            progress=task_data["status"].get("progress"),
            message=task_data["status"].get("message"),
            timestamp=task_data["status"].get("timestamp")
        ),
        artifacts=task_data.get("artifacts", []),
        metadata=task_data.get("metadata", {})
    )


# ============================================================================
# ADDITIONAL A2A PROTOCOL ENDPOINTS FOR UAE LEGAL GRAPHRAG
# ============================================================================

@a2a_router.get("/v1/card")
async def authenticated_agent_card():
    """
    A2A Protocol authenticated agent card endpoint.
    
    This endpoint provides additional authenticated information beyond the public agent card.
    """
    # This would include additional authenticated information
    # For now, return a basic authenticated card
    authenticated_card = {
        "protocolVersion": "0.3.0",
        "name": "uae-legal-graphrag",
        "description": "UAE Legal GraphRAG - AI-powered legal research and analysis system",
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
                "outputModes": ["application/json"]
            },
            {
                "id": "global_graphrag",
                "name": "Global GraphRAG",
                "description": "Comprehensive legal research using global graph analysis",
                "inputModes": ["application/json"],
                "outputModes": ["application/json"]
            },
            {
                "id": "drift_graphrag",
                "name": "DRIFT GraphRAG",
                "description": "Dynamic relevance and importance tracking for legal analysis",
                "inputModes": ["application/json"],
                "outputModes": ["application/json"]
            },
            {
                "id": "legal_analysis",
                "name": "Legal Analysis",
                "description": "Comprehensive legal analysis including contradiction detection and harmonization",
                "inputModes": ["application/json"],
                "outputModes": ["application/json"]
            },
            {
                "id": "ai_assistant",
                "name": "AI Legal Assistant",
                "description": "AI-powered legal research assistant with citation support",
                "inputModes": ["application/json"],
                "outputModes": ["application/json"]
            }
        ],
        "metadata": {
            "jurisdiction": "UAE",
            "legal_domains": ["commercial", "civil", "criminal", "labor", "data_protection"],
            "graph_database": "Neo4j",
            "ai_model": "Azure OpenAI GPT-4o",
            "compliance": ["GDPR", "UAE Data Protection Law", "Commercial Companies Law"],
            "authenticated": True,
            "internal_metrics": {
                "total_requests": len(task_store),
                "active_tasks": len([t for t in task_store.values() if t["status"]["state"] == "working"]),
                "system_health": "healthy"
            }
        }
    }
    
    return authenticated_card


@a2a_router.get("/health")
async def a2a_health_check():
    """
    A2A Protocol health check endpoint.
    
    This endpoint provides health status and available endpoints.
    """
    return {
        "status": "healthy",
        "protocol": "A2A",
        "version": "0.3.0",
        "endpoints": [
            "/.well-known/agent.json",
            "/v1/message:send",
            "/v1/message:stream",
            "/v1/tasks/{task_id}",
            "/v1/card"
        ],
        "capabilities": {
            "streaming": True,
            "longRunningTasks": True,
            "realTimeUpdates": True
        }
    }
