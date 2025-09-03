"""
DRIFT GraphRAG Agent
===================

Handles dynamic relevance and importance tracking in the UAE Legal GraphRAG system.
"""

from typing import Dict, Any, Optional
from loguru import logger
from .base_agent import BaseAgent
from ..schemas.a2a import A2AEnvelope, MessageType
from ..rag.graph_interface import DRIFTGraphRAG


class DRIFTGraphRAGAgent(BaseAgent):
    """Agent responsible for dynamic relevance and importance tracking."""
    
    def __init__(self, neo4j_conn, azure_llm):
        super().__init__("drift_graphrag_agent", neo4j_conn, azure_llm)
        self.drift_rag = DRIFTGraphRAG(neo4j_conn)
        
    async def handle_message(self, envelope: A2AEnvelope) -> Optional[A2AEnvelope]:
        """Handle DRIFT GraphRAG retrieval requests."""
        try:
            task_type = envelope.payload.get("task_type")
            data = envelope.payload.get("data", {})
            
            if task_type == "retrieve":
                return await self._perform_drift_retrieval(data, envelope)
            else:
                return await self.send_error_response(envelope, f"Unknown task type: {task_type}")
                
        except Exception as e:
            self.logger.error(f"DRIFT GraphRAG agent error: {e}")
            return await self.send_error_response(envelope, str(e))
    
    async def _perform_drift_retrieval(self, data: Dict[str, Any], envelope: A2AEnvelope) -> A2AEnvelope:
        """Perform dynamic relevance tracking retrieval."""
        query = data.get("query", "")
        max_results = data.get("max_results", 10)
        
        self.logger.info(f"Performing DRIFT GraphRAG retrieval for query: {query}")
        
        try:
            # Execute DRIFT GraphRAG retrieval
            rag_result = await self.drift_rag.retrieve(query, max_results)
            
            # Transform results for response
            result = {
                "agent_id": self.agent_id,
                "strategy": "drift",
                "query": query,
                "nodes_found": len(rag_result.nodes),
                "edges_found": len(rag_result.edges),
                "citations_found": len(rag_result.citations),
                "coverage": rag_result.coverage,
                "confidence": rag_result.confidence,
                "nodes": [{"id": n.id, "type": n.type, "content": n.content[:200]} for n in rag_result.nodes],
                "edges": [{"source": e.source, "target": e.target, "type": e.type} for e in rag_result.edges],
                "citations": [{"node_id": c.node_id, "content": c.content[:200], "score": c.score} for c in rag_result.citations]
            }
            
            return await self.send_response(envelope, result, True)
            
        except Exception as e:
            self.logger.error(f"DRIFT retrieval error: {e}")
            return await self.send_error_response(envelope, str(e))
