"""
Base Agent Class
===============

Base class for all AI agents in the UAE Legal GraphRAG system.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from loguru import logger
from ..schemas.a2a import A2AEnvelope, MessageType
from ..adapters.neo4j_conn import Neo4jConnection
from ..adapters.azure_openai import AzureLLM


class BaseAgent(ABC):
    """Base class for all AI agents."""
    
    def __init__(self, agent_id: str, neo4j_conn: Neo4jConnection, azure_llm: AzureLLM):
        self.agent_id = agent_id
        self.neo4j_conn = neo4j_conn
        self.azure_llm = azure_llm
        self.logger = logger.bind(agent=agent_id)
        
    @abstractmethod
    async def handle_message(self, envelope: A2AEnvelope) -> Optional[A2AEnvelope]:
        """Handle incoming A2A message."""
        pass
        
    async def send_response(self, original_envelope: A2AEnvelope, result: Dict[str, Any], success: bool = True) -> A2AEnvelope:
        """Send response back to the original sender."""
        return A2AEnvelope(
            message_id=f"resp_{original_envelope.message_id}",
            conversation_id=original_envelope.conversation_id,
            message_type=MessageType.RESULT,
            sender=self.agent_id,
            recipient=original_envelope.sender,
            ttl=original_envelope.ttl,
            payload={
                "success": success,
                "result": result,
                "original_task": original_envelope.payload.get("task_type", "unknown"),
                "agent_id": self.agent_id
            }
        )
    
    async def send_error_response(self, original_envelope: A2AEnvelope, error: str) -> A2AEnvelope:
        """Send error response back to the original sender."""
        return await self.send_response(original_envelope, {"error": error}, False)
