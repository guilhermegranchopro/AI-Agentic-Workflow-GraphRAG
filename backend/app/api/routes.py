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
from ..agents.orchestrator_agent import OrchestratorAgent
from ..agents.local_graphrag_agent import LocalGraphRAGAgent
from ..agents.global_graphrag_agent import GlobalGraphRAGAgent
from ..agents.drift_graphrag_agent import DRIFTGraphRAGAgent

# Create router
api_router = APIRouter()

# Global service instances (will be set by main.py)
azure_llm: AzureLLM = None
neo4j_conn: Neo4jConnection = None
a2a_adapter: A2AAdapter = None
faiss_db: FAISSVectorDB = None

# Agent instances
orchestrator_agent: OrchestratorAgent = None
local_graphrag_agent: LocalGraphRAGAgent = None
global_graphrag_agent: GlobalGraphRAGAgent = None
drift_graphrag_agent: DRIFTGraphRAGAgent = None


def get_services():
    """Dependency to get service instances."""
    return {
        "azure_llm": azure_llm,
        "neo4j_conn": neo4j_conn,
        "a2a_adapter": a2a_adapter,
        "faiss_db": faiss_db,
        "orchestrator_agent": orchestrator_agent,
        "local_graphrag_agent": local_graphrag_agent,
        "global_graphrag_agent": global_graphrag_agent,
        "drift_graphrag_agent": drift_graphrag_agent
    }


@api_router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    req: Request,
    services: Dict[str, Any] = Depends(get_services)
):
    """Chat endpoint for AI assistant using multi-agent workflow."""
    request_id = req.headers.get("X-Request-ID", "unknown")
    context = get_telemetry_context(request_id)
    
    try:
        # Log agent call
        log_agent_call(request_id, "assistant", "chat", {
            "strategy": request.strategy,
            "max_results": request.max_results,
            "workflow": "multi_agent"
        })
        
        # Get services
        orchestrator_agent = services["orchestrator_agent"]
        a2a_adapter = services["a2a_adapter"]
        
        if not orchestrator_agent or not a2a_adapter:
            # Fallback to direct GraphRAG if agents not available
            logger.warning("Agents not available, falling back to direct GraphRAG")
            return await _fallback_chat_endpoint(request, req, services)
        
        # Create conversation ID if not provided
        conversation_id = request.conversation_id or f"conv_{request_id}"
        
        # Execute multi-agent workflow
        workflow_result = await a2a_adapter.send_task(
            conversation_id=conversation_id,
            sender="api_gateway",
            recipient="orchestrator_agent",
            task_type="assistant_workflow",
            payload={
                "query": request.message,
                "strategy": request.strategy,
                "max_results": request.max_results
            }
        )
        
        if not workflow_result or not workflow_result.payload.get("success", False):
            logger.error("Multi-agent workflow failed, falling back to direct GraphRAG")
            return await _fallback_chat_endpoint(request, req, services)
        
        result_data = workflow_result.payload.get("result", {})
        
        # Log success
        log_agent_result(request_id, "assistant", "chat", True, {
            "conversation_id": conversation_id,
            "citations_count": len(result_data.get("citations", [])),
            "workflow": "multi_agent"
        })
        
        return ChatResponse(
            response=result_data.get("response", ""),
            conversation_id=conversation_id,
            citations=result_data.get("citations", []),
            nodes=result_data.get("nodes", []),
            edges=result_data.get("edges", []),
            metadata=result_data.get("metadata", {})
        )
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        log_agent_result(request_id, "assistant", "chat", False, {"error": str(e)})
        raise HTTPException(status_code=500, detail=str(e))


async def _fallback_chat_endpoint(
    request: ChatRequest,
    req: Request,
    services: Dict[str, Any]
) -> ChatResponse:
    """Fallback to direct GraphRAG when agents are not available."""
    logger.info("Using fallback direct GraphRAG approach")
    
    # Get services
    azure_llm = services["azure_llm"]
    neo4j_conn = services["neo4j_conn"]
    
    if not azure_llm or not neo4j_conn:
        raise HTTPException(status_code=503, detail="Services not available")
    
    # Create conversation ID
    conversation_id = request.conversation_id or f"conv_{req.headers.get('X-Request-ID', 'unknown')}"
    
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
        None
    )
    
    return ChatResponse(
        response=response,
        conversation_id=conversation_id,
        citations=rag_result.citations,
        nodes=rag_result.nodes,
        edges=rag_result.edges,
        metadata={
            "strategy": request.strategy,
            "coverage": rag_result.coverage,
            "confidence": rag_result.confidence,
            "workflow": "fallback_direct"
        }
    )


@api_router.post("/analysis", response_model=AnalysisResponse)
async def analysis_endpoint(
    request: AnalysisRequest,
    req: Request,
    services: Dict[str, Any] = Depends(get_services)
):
    """Legal analysis endpoint using multi-agent workflow."""
    request_id = req.headers.get("X-Request-ID", "unknown")
    context = get_telemetry_context(request_id)
    
    try:
        # Log agent call
        log_agent_call(request_id, "analyzer", "analysis", {
            "analysis_type": request.analysis_type,
            "max_depth": request.max_depth,
            "workflow": "multi_agent"
        })
        
        # Get services
        orchestrator_agent = services["orchestrator_agent"]
        a2a_adapter = services["a2a_adapter"]
        
        if not orchestrator_agent or not a2a_adapter:
            # Fallback to direct analysis if agents not available
            logger.warning("Agents not available, falling back to direct analysis")
            return await _fallback_analysis_endpoint(request, req, services)
        
        # Execute multi-agent workflow
        workflow_result = await a2a_adapter.send_task(
            conversation_id=f"analysis_{request_id}",
            sender="api_gateway",
            recipient="orchestrator_agent",
            task_type="analysis_workflow",
            payload={
                "query": request.query,
                "analysis_type": request.analysis_type,
                "max_depth": request.max_depth
            }
        )
        
        if not workflow_result or not workflow_result.payload.get("success", False):
            logger.error("Multi-agent analysis workflow failed, falling back to direct analysis")
            return await _fallback_analysis_endpoint(request, req, services)
        
        result_data = workflow_result.payload.get("result", {})
        
        logger.info(f"Analysis result received: {result_data}")
        
        # Log success
        log_agent_result(request_id, "analyzer", "analysis", True, {
            "contradictions_count": len(result_data.get("contradictions", [])),
            "harmonizations_count": len(result_data.get("harmonizations", [])),
            "workflow": "multi_agent"
        })
        
        # Transform analysis result to match frontend expectations
        contradictions = result_data.get("contradictions", [])
        harmonizations = result_data.get("harmonizations", [])
        citations = result_data.get("citations", [])
        
        logger.info(f"Transformed data - contradictions: {len(contradictions)}, harmonizations: {len(harmonizations)}")
        
        # Generate detailed recommendations from harmonizations and contradictions
        recommendations = []
        
        # Add harmonization recommendations
        for harm in harmonizations:
            recommendations.append({
                "id": harm["id"],
                "title": harm["title"],
                "description": harm["description"],
                "action": harm["approach"],
                "priority": "high",
                "timeline": "Immediate (30 days)",
                "cost_impact": "High - Legal harmonization and compliance costs"
            })
        
        # Add specific recommendations based on contradiction severity
        for contradiction in contradictions:
            severity = contradiction.get("severity", "medium")
            category = contradiction.get("category", "Legal Compliance")
            
            if severity == "critical":
                priority = "high"
                timeline = "Immediate (7 days)"
                cost_impact = "Critical - Immediate compliance costs"
            elif severity == "high":
                priority = "high"
                timeline = "Short-term (30 days)"
                cost_impact = "High - Compliance and harmonization costs"
            elif severity == "medium":
                priority = "medium"
                timeline = "Medium-term (90 days)"
                cost_impact = "Medium - Review and alignment costs"
            else:
                priority = "low"
                timeline = "Long-term (180 days)"
                cost_impact = "Low - Monitoring and review costs"
            
            recommendations.append({
                "id": f"rec_{contradiction['id']}",
                "title": f"Address {category} Contradiction",
                "description": f"Implement measures to resolve the contradiction in {category}: {contradiction['title']}",
                "action": contradiction.get("recommendation", "Review and harmonize conflicting provisions"),
                "priority": priority,
                "timeline": timeline,
                "cost_impact": cost_impact
            })
        
        # Generate detailed summary
        if contradictions:
            severity_counts = {
                "critical": len([c for c in contradictions if c.get("severity") == "critical"]),
                "high": len([c for c in contradictions if c.get("severity") == "high"]),
                "medium": len([c for c in contradictions if c.get("severity") == "medium"]),
                "low": len([c for c in contradictions if c.get("severity") == "low"])
            }
            
            severity_text = []
            if severity_counts["critical"] > 0:
                severity_text.append(f"{severity_counts['critical']} critical")
            if severity_counts["high"] > 0:
                severity_text.append(f"{severity_counts['high']} high priority")
            if severity_counts["medium"] > 0:
                severity_text.append(f"{severity_counts['medium']} medium priority")
            if severity_counts["low"] > 0:
                severity_text.append(f"{severity_counts['low']} low priority")
            
            severity_summary = ", ".join(severity_text)
            summary = f"Analysis of '{request.query}' identified {len(contradictions)} legal contradictions ({severity_summary}) requiring immediate attention. Found {len(harmonizations)} harmonization opportunities across {len(set(c.get('type', 'unknown') for c in citations))} legal domains."
        else:
            summary = f"Analysis of '{request.query}' found no explicit contradictions in the current knowledge base. Consider expanding the legal data or refining the search criteria."
        
        # Calculate stats
        stats = {
            "total_contradictions": len(contradictions),
            "critical_priority": len([c for c in contradictions if c.get("severity") == "critical"]),
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
            "stats": stats,
            "harmonizations": harmonizations,
            "citations": citations
        }
        
    except Exception as e:
        logger.error(f"Analysis endpoint error: {e}")
        log_agent_result(request_id, "analyzer", "analysis", False, {"error": str(e)})
        raise HTTPException(status_code=500, detail=str(e))


async def _fallback_analysis_endpoint(
    request: AnalysisRequest,
    req: Request,
    services: Dict[str, Any]
) -> AnalysisResponse:
    """Fallback to direct analysis when agents are not available."""
    logger.info("Using fallback direct analysis approach")
    
    # Get services
    azure_llm = services["azure_llm"]
    neo4j_conn = services["neo4j_conn"]
    
    if not azure_llm or not neo4j_conn:
        raise HTTPException(status_code=503, detail="Services not available")
    
    # Perform legal analysis using existing function
    analysis_result = await perform_legal_analysis(
        request.query,
        request.analysis_type,
        request.max_depth,
        azure_llm,
        neo4j_conn,
        None
    )
    
    return analysis_result


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
        
        # Get all relationships from Neo4j with properties
        edges_query = "MATCH (a:LegalNode)-[r]->(b:LegalNode) RETURN a, type(r) as rel_type, properties(r) as rel_props, b"
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
            if "a" in record and record["a"] and "b" in record and record["b"] and "rel_type" in record and "rel_props" in record:
                start_node = record["a"]
                end_node = record["b"]
                rel_type = record["rel_type"]
                rel_props = record["rel_props"]
                
                # Extract relationship type from properties if available
                if isinstance(rel_props, dict) and "type" in rel_props:
                    relationship_type = rel_props["type"]
                else:
                    relationship_type = str(rel_type)
                
                edges.append({
                    "source": start_node.get("id", "") if isinstance(start_node, dict) else str(start_node),
                    "target": end_node.get("id", "") if isinstance(end_node, dict) else str(end_node),
                    "type": relationship_type,
                    "weight": 1.0,
                    "metadata": rel_props if isinstance(rel_props, dict) else {}
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
    """Generate AI response using RAG results and web search when needed."""
    
    # Check if we have sufficient GraphRAG results
    has_graphrag_data = len(rag_result.citations) > 0 and len(rag_result.nodes) > 0
    
    if has_graphrag_data:
        # Use GraphRAG results
    context_text = "\n\n".join([
        f"Source {i+1}: {citation.content}"
        for i, citation in enumerate(rag_result.citations[:5])  # Top 5 citations
    ])
    
        # Create system prompt for GraphRAG-based response
        system_prompt = """You are a legal research assistant for UAE law. Use the provided GraphRAG sources to answer questions accurately and cite your sources. 

IMPORTANT: Always mention that you used GraphRAG techniques and cite the specific nodes/edges from the knowledge graph that were relevant to your answer.

Format your response as follows:
1. Answer the question based on the GraphRAG sources
2. Mention which GraphRAG strategy was used (Local, Global, or Hybrid)
3. Cite specific nodes from the knowledge graph that were relevant
4. If you used relationships between nodes, mention those as well"""
    
    # Prepare messages
    messages = [
        {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Question: {message}\n\nGraphRAG Sources:\n{context_text}\n\nPlease provide a comprehensive answer based on the GraphRAG sources provided."}
        ]
        
        # Generate response
        response = await azure_llm.chat(messages, temperature=0.7, max_tokens=1500)
        return response
    
    else:
        # No GraphRAG data available, use web search capabilities
        system_prompt = """You are a legal research assistant for UAE law. Since no specific GraphRAG sources were found in the knowledge graph, you should use your general knowledge about UAE law and legal principles to provide a helpful response.

IMPORTANT: 
1. Clearly state that you are providing information based on general knowledge since no specific GraphRAG sources were found
2. Mention that you did not use GraphRAG techniques for this response
3. Provide accurate and helpful information about UAE law
4. If the question is very specific and requires current legal information, suggest consulting with a legal professional

For complex or time-sensitive legal matters, always recommend consulting with qualified legal professionals."""
        
        # Prepare messages for web-based response
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Question: {message}\n\nPlease provide a helpful response about UAE law based on your general knowledge. Clearly state that no GraphRAG sources were found and you are using general knowledge."}
    ]
    
    # Generate response
        response = await azure_llm.chat(messages, temperature=0.7, max_tokens=1500)
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
        # Use GraphRAG to find relevant nodes
        from ..rag.graph_interface import GlobalGraphRAG
        graph_rag = GlobalGraphRAG(neo4j_conn)
        rag_result = await graph_rag.retrieve(query, max_results=10)
        
        if not rag_result.nodes:
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
        
        # Find CONTRADICTS relationships involving the retrieved nodes
        node_ids = [node.id for node in rag_result.nodes]
        contradictions_query = """
        MATCH (a:LegalNode)-[r:RELATES_TO]->(b:LegalNode)
        WHERE a.id IN $node_ids AND b.id IN $node_ids AND r.type = 'CONTRADICTS'
        RETURN a, b, properties(r) as r_props
        """
        
        contradictions_result = await neo4j_conn.run_cypher(contradictions_query, {"node_ids": node_ids})
        
        # Analyze contradictions
        contradictions = []
        harmonizations = []
        citations = []
        
        # Process explicit contradictions
        for record in contradictions_result:
            if "a" in record and "b" in record and "r_props" in record:
                node_a = record["a"]
                node_b = record["b"]
                relationship_props = record["r_props"]
                
                # Extract priority and category from relationship properties
                priority = relationship_props.get("priority", "medium")
                severity = relationship_props.get("severity", "medium")
                category = relationship_props.get("category", "Legal Compliance")
                description = relationship_props.get("description", f"Contradiction between {node_a.get('title', '')} and {node_b.get('title', '')}")
                
                # Map priority to severity if not provided
                if not relationship_props.get("severity"):
                    if priority == "critical":
                        severity = "critical"
                    elif priority == "high":
                        severity = "high"
                    elif priority == "medium":
                        severity = "medium"
                    else:
                        severity = "low"
                
                contradiction = {
                    "id": f"cont_{node_a.get('id', '')}_{node_b.get('id', '')}",
                    "title": f"Legal Contradiction: {node_a.get('title', '')} vs {node_b.get('title', '')}",
                    "description": description,
                    "severity": severity,
                    "priority": priority,
                    "category": category,
                    "sources": [node_a.get("title", ""), node_b.get("title", "")],
                    "impact": f"High impact on {category.lower()} compliance and regulatory alignment",
                    "recommendation": f"Review and harmonize the conflicting provisions between {node_a.get('title', '')} and {node_b.get('title', '')} to ensure {category.lower()} compliance"
                }
                contradictions.append(contradiction)
        
        # If no explicit contradictions found, look for potential contradictions
        if not contradictions:
            # Group nodes by type to identify potential contradictions
            node_types = {}
            for node in rag_result.nodes:
                node_type = node.type
                if node_type not in node_types:
                    node_types[node_type] = []
                node_types[node_type].append(node)
            
            # Generate contradictions based on node analysis
            for node_type, nodes in node_types.items():
                if len(nodes) > 1:
                    # Multiple nodes of same type might indicate contradictions
                    contradiction = {
                        "id": f"cont_{node_type}_{len(contradictions) + 1}",
                        "title": f"Multiple {node_type} Provisions Found",
                        "description": f"Found {len(nodes)} different {node_type} provisions that may contain contradictions or inconsistencies.",
                        "severity": "medium",
                        "sources": [node.id for node in nodes[:3]],
                        "recommendation": f"Review and harmonize {node_type} provisions to ensure consistency"
                    }
                    contradictions.append(contradiction)
        
        # Generate harmonization opportunities
        if contradictions:
            harmonization = {
                "id": f"harm_{len(harmonizations) + 1}",
                "title": "Legal Harmonization Required",
                "description": f"Found {len(contradictions)} contradictions that require legal harmonization to ensure consistency and compliance.",
                "approach": "Legal harmonization and regulatory alignment",
                "sources": [node.id for node in rag_result.nodes[:5]]
            }
            harmonizations.append(harmonization)
        
        # Generate citations from found nodes
        for node in rag_result.nodes:
            citations.append({
                "node_id": node.id,
                "node_type": node.type,
                "content": node.content[:200] + "..." if len(node.content) > 200 else node.content,
                "score": node.score or 1.0,
                "metadata": {}
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
