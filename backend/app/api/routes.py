from typing import Dict, Any
from fastapi import APIRouter, Request, HTTPException, Depends
from loguru import logger

from ..schemas.messages import (
    ChatRequest, ChatResponse, AnalysisRequest, AnalysisResponse,
    TraceResponse
)
from ..schemas.rag import RAGQuery, RAGResult
from ..utils.telemetry import get_telemetry_context, log_agent_call, log_agent_result
from ..utils.rate_limit import get_rate_limit_info
from ..rag.graph_interface import LocalGraphRAG, GlobalGraphRAG, DRIFTGraphRAG
from ..adapters.azure_openai import AzureLLM
from ..adapters.neo4j_conn import Neo4jConnection
from ..adapters.a2a import A2AAdapter
from ..adapters.vectordb_faiss import FAISSVectorDB

# Create router
api_router = APIRouter()

# Global service instances (will be set by main.py)
azure_llm: AzureLLM = None
neo4j_conn: Neo4jConnection = None
a2a_adapter: A2AAdapter = None
faiss_db: FAISSVectorDB = None


def get_services():
    """Dependency to get service instances."""
    return {
        "azure_llm": azure_llm,
        "neo4j_conn": neo4j_conn,
        "a2a_adapter": a2a_adapter,
        "faiss_db": faiss_db
    }


@api_router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    req: Request,
    services: Dict[str, Any] = Depends(get_services)
):
    """Chat endpoint for AI assistant."""
    request_id = req.headers.get("X-Request-ID", "unknown")
    context = get_telemetry_context(request_id)
    
    try:
        # Log agent call
        log_agent_call(request_id, "assistant", "chat", {
            "strategy": request.strategy,
            "max_results": request.max_results
        })
        
        # Get services
        azure_llm = services["azure_llm"]
        neo4j_conn = services["neo4j_conn"]
        
        if not azure_llm or not neo4j_conn:
            raise HTTPException(status_code=503, detail="Services not available")
        
        # Create conversation ID if not provided
        conversation_id = request.conversation_id or f"conv_{request_id}"
        
        # Perform RAG retrieval based on strategy
        rag_result = await perform_rag_retrieval(
            request.message,
            request.strategy,
            request.max_results,
            neo4j_conn,
            faiss_db=services["faiss_db"]
        )
        
        # Generate AI response
        response = await generate_ai_response(
            request.message,
            rag_result,
            azure_llm,
            context
        )
        
        # Log success
        log_agent_result(request_id, "assistant", "chat", True, {
            "conversation_id": conversation_id,
            "citations_count": len(rag_result.citations)
        })
        
        return ChatResponse(
            response=response,
            conversation_id=conversation_id,
            citations=rag_result.citations,
            nodes=rag_result.nodes,
            edges=rag_result.edges,
            metadata={
                "strategy": request.strategy,
                "coverage": rag_result.coverage,
                "confidence": rag_result.confidence
            }
        )
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        log_agent_result(request_id, "assistant", "chat", False, {"error": str(e)})
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/analysis", response_model=AnalysisResponse)
async def analysis_endpoint(
    request: AnalysisRequest,
    req: Request,
    services: Dict[str, Any] = Depends(get_services)
):
    """Legal analysis endpoint."""
    request_id = req.headers.get("X-Request-ID", "unknown")
    context = get_telemetry_context(request_id)
    
    try:
        # Log agent call
        log_agent_call(request_id, "analyzer", "analysis", {
            "analysis_type": request.analysis_type,
            "max_depth": request.max_depth
        })
        
        # Get services
        azure_llm = services["azure_llm"]
        neo4j_conn = services["neo4j_conn"]
        
        if not azure_llm or not neo4j_conn:
            raise HTTPException(status_code=503, detail="Services not available")
        
        # Perform legal analysis
        analysis_result = await perform_legal_analysis(
            request.query,
            request.analysis_type,
            request.max_depth,
            azure_llm,
            neo4j_conn,
            context
        )
        
        # Log success
        log_agent_result(request_id, "analyzer", "analysis", True, {
            "contradictions_count": len(analysis_result.get("contradictions", [])),
            "harmonizations_count": len(analysis_result.get("harmonizations", []))
        })
        
        # Transform analysis result to match frontend expectations
        contradictions = analysis_result.get("contradictions", [])
        harmonizations = analysis_result.get("harmonizations", [])
        citations = analysis_result.get("citations", [])
        
        # Generate recommendations from harmonizations
        recommendations = []
        for harm in harmonizations:
            recommendations.append({
                "id": harm["id"],
                "title": harm["title"],
                "description": harm["description"],
                "action": harm["approach"],
                "priority": "medium",
                "timeline": "Medium-term (90 days)",
                "cost_impact": "Medium - Harmonization costs"
            })
        
        # Generate summary
        summary = f"Analysis of '{request.query}' revealed {len(contradictions)} potential contradictions and {len(harmonizations)} harmonization opportunities across {len(set(c.get('type', 'unknown') for c in citations))} legal domains."
        
        # Calculate stats
        stats = {
            "total_contradictions": len(contradictions),
            "high_priority": len([c for c in contradictions if c.get("severity") == "high"]),
            "medium_priority": len([c for c in contradictions if c.get("severity") == "medium"]),
            "low_priority": len([c for c in contradictions if c.get("severity") == "low"])
        }
        
        return {
            "query": request.query,
            "contradictions": contradictions,
            "recommendations": recommendations,
            "summary": summary,
            "confidence": 0.85,
            "stats": stats
        }
        
    except Exception as e:
        logger.error(f"Analysis endpoint error: {e}")
        log_agent_result(request_id, "analyzer", "analysis", False, {"error": str(e)})
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/debug/trace/{conversation_id}", response_model=TraceResponse)
async def debug_trace_endpoint(
    conversation_id: str,
    req: Request,
    services: Dict[str, Any] = Depends(get_services)
):
    """Debug endpoint to get conversation trace."""
    try:
        a2a_adapter = services["a2a_adapter"]
        if not a2a_adapter:
            raise HTTPException(status_code=503, detail="A2A adapter not available")
        
        # Get conversation trace
        messages = await a2a_adapter.get_conversation_trace(conversation_id)
        
        return TraceResponse(
            conversation_id=conversation_id,
            messages=messages,
            metadata={"total_messages": len(messages)}
        )
        
    except Exception as e:
        logger.error(f"Debug trace endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/debug/stats")
async def debug_stats_endpoint(
    req: Request,
    services: Dict[str, Any] = Depends(get_services)
):
    """Debug endpoint to get system statistics."""
    try:
        stats = {}
        
        # Neo4j stats
        neo4j_conn = services["neo4j_conn"]
        if neo4j_conn:
            stats["neo4j"] = await neo4j_conn.get_graph_stats()
        
        # FAISS stats
        faiss_db = services["faiss_db"]
        if faiss_db:
            stats["faiss"] = faiss_db.get_stats()
        
        # Rate limit info
        stats["rate_limit"] = get_rate_limit_info(req)
        
        return stats
        
    except Exception as e:
        logger.error(f"Debug stats endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/rate-limit-info")
async def rate_limit_info_endpoint(req: Request):
    """Get rate limit information for the current request."""
    return get_rate_limit_info(req)


@api_router.get("/config")
async def config_endpoint():
    """Get configuration information (without sensitive data)."""
    from ..schemas.config import settings
    
    return {
        "app_env": settings.app_env,
        "port": settings.port,
        "azure_openai_configured": bool(settings.azure_openai_api_key),
        "neo4j_configured": bool(settings.neo4j_uri),
        "faiss_index_path": settings.faiss_index_path,
        "max_retrieval_results": settings.max_retrieval_results,
        "similarity_threshold": settings.similarity_threshold,
        "rate_limit_requests": settings.rate_limit_requests,
        "rate_limit_window": settings.rate_limit_window
    }


@api_router.get("/graph")
async def graph_endpoint(
    req: Request,
    services: Dict[str, Any] = Depends(get_services)
):
    """Graph data endpoint for Neo4j knowledge graph."""
    try:
        # Get services
        neo4j_conn = services["neo4j_conn"]
        
        if not neo4j_conn:
            raise HTTPException(status_code=503, detail="Neo4j service not available")
        
        # Get all nodes from Neo4j
        nodes_query = "MATCH (n:LegalNode) RETURN n"
        nodes_result = await neo4j_conn.run_cypher(nodes_query)
        
        # Get all relationships from Neo4j
        edges_query = "MATCH (a:LegalNode)-[r:RELATES_TO]->(b:LegalNode) RETURN a, r, b"
        edges_result = await neo4j_conn.run_cypher(edges_query)
        
        # Transform nodes
        nodes = []
        for record in nodes_result:
            if "n" in record and record["n"]:
                node_data = record["n"]
                nodes.append({
                    "id": node_data.get("id", ""),
                    "title": node_data.get("title", ""),
                    "content": node_data.get("content", ""),
                    "type": node_data.get("type", "unknown"),
                    "metadata": node_data.get("metadata", {}),
                    "score": node_data.get("score", 1.0)
                })
        
        # Transform edges
        edges = []
        for record in edges_result:
            if "r" in record and record["r"] and "a" in record and record["a"] and "b" in record and record["b"]:
                # Handle relationship tuple format: (start_node, relationship_type, end_node)
                if isinstance(record["r"], tuple) and len(record["r"]) >= 3:
                    start_node = record["r"][0]
                    rel_type = record["r"][1]
                    end_node = record["r"][2]
                    
                    edges.append({
                        "source": start_node.get("id", "") if isinstance(start_node, dict) else str(start_node),
                        "target": end_node.get("id", "") if isinstance(end_node, dict) else str(end_node),
                        "type": rel_type,
                        "weight": 1.0,
                        "metadata": {}
                    })
        
        return {
            "nodes": nodes,
            "edges": edges,
            "stats": {
                "nodeCount": len(nodes),
                "edgeCount": len(edges),
                "nodeTypes": {},
                "edgeTypes": {}
            }
        }
        
    except Exception as e:
        logger.error(f"Graph endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Helper functions
async def perform_rag_retrieval(
    query: str,
    strategy: str,
    max_results: int,
    neo4j_conn: Neo4jConnection,
    faiss_db: FAISSVectorDB = None
) -> RAGResult:
    """Perform RAG retrieval based on strategy."""
    # Create appropriate GraphRAG instance
    if strategy == "local":
        graph_rag = LocalGraphRAG(neo4j_conn)
    elif strategy == "global":
        graph_rag = GlobalGraphRAG(neo4j_conn)
    elif strategy == "drift":
        graph_rag = DRIFTGraphRAG(neo4j_conn)
    else:  # hybrid
        # Combine multiple strategies
        local_rag = LocalGraphRAG(neo4j_conn)
        global_rag = GlobalGraphRAG(neo4j_conn)
        
        local_result = await local_rag.retrieve(query, max_results // 2)
        global_result = await global_rag.retrieve(query, max_results // 2)
        
        # Merge results
        return RAGResult(
            query=query,
            nodes=local_result.nodes + global_result.nodes,
            edges=local_result.edges + global_result.edges,
            citations=local_result.citations + global_result.citations,
            coverage=(local_result.coverage + global_result.coverage) / 2,
            confidence=(local_result.confidence + global_result.confidence) / 2
        )
    
    return await graph_rag.retrieve(query, max_results)


async def generate_ai_response(
    message: str,
    rag_result: RAGResult,
    azure_llm: AzureLLM,
    context: Any
) -> str:
    """Generate AI response using RAG results."""
    # Prepare context from RAG results
    context_text = "\n\n".join([
        f"Source {i+1}: {citation.content}"
        for i, citation in enumerate(rag_result.citations[:5])  # Top 5 citations
    ])
    
    # Create system prompt
    system_prompt = """You are a legal research assistant for UAE law. Use the provided sources to answer questions accurately and cite your sources. If you cannot answer based on the sources, say so clearly."""
    
    # Prepare messages
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Question: {message}\n\nSources:\n{context_text}\n\nPlease provide a comprehensive answer based on the sources provided."}
    ]
    
    # Generate response
    response = await azure_llm.chat(messages, temperature=0.7, max_tokens=1000)
    return response


async def perform_legal_analysis(
    query: str,
    analysis_type: str,
    max_depth: int,
    azure_llm: AzureLLM,
    neo4j_conn: Neo4jConnection,
    context: Any
) -> Dict[str, Any]:
    """Perform legal analysis using Neo4j knowledge graph."""
    try:
        # Search for relevant legal nodes based on query
        search_query = """
        MATCH (n:LegalNode)
        WHERE n.content CONTAINS $query OR n.title CONTAINS $query
        RETURN n
        LIMIT 10
        """
        
        nodes_result = await neo4j_conn.run_cypher(search_query, {"query": query})
        
        if not nodes_result:
            # Fallback to mock analysis if no relevant nodes found
            return {
                "contradictions": [
                    {
                        "id": "cont_1",
                        "title": "No specific legal data found",
                        "description": f"No specific legal provisions found for query: {query}",
                        "severity": "low",
                        "sources": ["Knowledge Graph"],
                        "recommendation": "Consider expanding the knowledge base with more specific legal provisions"
                    }
                ],
                "harmonizations": [],
                "citations": []
            }
        
        # Analyze the found nodes for potential contradictions
        contradictions = []
        harmonizations = []
        citations = []
        
        # Group nodes by type to identify potential contradictions
        node_types = {}
        for record in nodes_result:
            if "n" in record and record["n"]:
                node_data = record["n"]
                node_type = node_data.get("type", "unknown")
                if node_type not in node_types:
                    node_types[node_type] = []
                node_types[node_type].append(node_data)
        
        # Generate contradictions based on node analysis
        for node_type, nodes in node_types.items():
            if len(nodes) > 1:
                # Multiple nodes of same type might indicate contradictions
                contradiction = {
                    "id": f"cont_{node_type}_{len(contradictions) + 1}",
                    "title": f"Multiple {node_type} Provisions Found",
                    "description": f"Found {len(nodes)} different {node_type} provisions that may contain contradictions or inconsistencies.",
                    "severity": "medium",
                    "sources": [node.get("title", node.get("id", "")) for node in nodes[:3]],
                    "recommendation": f"Review and harmonize {node_type} provisions to ensure consistency"
                }
                contradictions.append(contradiction)
        
        # Generate harmonization opportunities
        if len(node_types) > 1:
            harmonization = {
                "id": f"harm_{len(harmonizations) + 1}",
                "title": "Cross-Domain Legal Harmonization",
                "description": f"Analysis spans {len(node_types)} different legal domains: {', '.join(node_types.keys())}",
                "approach": "Cross-domain harmonization",
                "sources": [node.get("title", node.get("id", "")) for nodes in node_types.values() for node in nodes[:2]]
            }
            harmonizations.append(harmonization)
        
        # Generate citations from found nodes
        for record in nodes_result:
            if "n" in record and record["n"]:
                node_data = record["n"]
                citations.append({
                    "id": node_data.get("id", ""),
                    "title": node_data.get("title", ""),
                    "content": node_data.get("content", "")[:200] + "...",
                    "type": node_data.get("type", "unknown"),
                    "score": node_data.get("score", 1.0)
                })
        
        return {
            "contradictions": contradictions,
            "harmonizations": harmonizations,
            "citations": citations
        }
        
    except Exception as e:
        logger.error(f"Legal analysis error: {e}")
        # Fallback to mock analysis
        return {
            "contradictions": [
                {
                    "id": "cont_1",
                    "title": "Analysis Error",
                    "description": f"Error during analysis: {str(e)}",
                    "severity": "medium",
                    "sources": ["System Error"],
                    "recommendation": "Please try again or contact support"
                }
            ],
            "harmonizations": [],
            "citations": []
        }
