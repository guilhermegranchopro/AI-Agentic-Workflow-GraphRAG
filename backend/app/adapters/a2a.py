import asyncio
import uuid
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime, timedelta
from loguru import logger
from ..schemas.a2a import A2AEnvelope, MessageType
from ..schemas.config import settings
from ..store.event_store import EventStore


class A2AAdapter:
    """Agent-to-Agent protocol adapter for inter-agent communication."""
    
    def __init__(self):
        """Initialize A2A adapter."""
        self.routers: Dict[str, Callable] = {}
        self.event_store = EventStore()
        self.conversation_timeouts: Dict[str, datetime] = {}
        
    def encode(self, envelope: A2AEnvelope) -> Dict[str, Any]:
        """Encode A2A envelope to dictionary."""
        return {
            "message_id": envelope.message_id,
            "conversation_id": envelope.conversation_id,
            "message_type": envelope.message_type.value,
            "sender": envelope.sender,
            "recipient": envelope.recipient,
            "timestamp": envelope.timestamp.isoformat(),
            "ttl": envelope.ttl,
            "payload": envelope.payload,
            "metadata": envelope.metadata
        }
        
    def decode(self, data: Dict[str, Any]) -> A2AEnvelope:
        """Decode dictionary to A2A envelope."""
        return A2AEnvelope(
            message_id=data["message_id"],
            conversation_id=data["conversation_id"],
            message_type=MessageType(data["message_type"]),
            sender=data["sender"],
            recipient=data.get("recipient"),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            ttl=data["ttl"],
            payload=data["payload"],
            metadata=data.get("metadata", {})
        )
        
    def register_router(self, agent_id: str, handler: Callable):
        """Register message router for an agent."""
        self.routers[agent_id] = handler
        logger.info(f"Registered A2A router for agent: {agent_id}")
        
    async def route(self, envelope: A2AEnvelope) -> Optional[A2AEnvelope]:
        """Route A2A message to appropriate handler."""
        # Check TTL
        if datetime.utcnow() > envelope.timestamp + timedelta(seconds=envelope.ttl):
            logger.warning(f"Message {envelope.message_id} expired")
            return None
            
        # Store message
        await self.event_store.store_envelope(envelope)
        
        # Route to handler
        if envelope.recipient and envelope.recipient in self.routers:
            try:
                handler = self.routers[envelope.recipient]
                response = await handler(envelope)
                return response
            except Exception as e:
                logger.error(f"A2A routing error for {envelope.recipient}: {e}")
                return self._create_error_response(envelope, str(e))
        else:
            logger.warning(f"No router found for recipient: {envelope.recipient}")
            return None
            
    async def send_task(
        self,
        conversation_id: str,
        sender: str,
        recipient: str,
        task_type: str,
        payload: Dict[str, Any],
        timeout: int = None
    ) -> A2AEnvelope:
        """Send a task message to another agent."""
        envelope = A2AEnvelope(
            message_id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            message_type=MessageType.TASK,
            sender=sender,
            recipient=recipient,
            ttl=timeout or settings.a2a_timeout,
            payload={
                "task_type": task_type,
                "data": payload
            }
        )
        
        # Set conversation timeout
        self.conversation_timeouts[conversation_id] = datetime.utcnow() + timedelta(seconds=envelope.ttl)
        
        return await self.route(envelope)
        
    async def send_result(
        self,
        conversation_id: str,
        sender: str,
        recipient: str,
        result_data: Dict[str, Any],
        success: bool = True
    ) -> A2AEnvelope:
        """Send a result message to another agent."""
        envelope = A2AEnvelope(
            message_id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            message_type=MessageType.RESULT,
            sender=sender,
            recipient=recipient,
            ttl=settings.a2a_timeout,
            payload={
                "success": success,
                "data": result_data
            }
        )
        
        return await self.route(envelope)
        
    async def get_conversation_trace(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Get conversation trace from event store."""
        envelopes = await self.event_store.get_envelopes_by_conversation(conversation_id)
        return [self.encode(envelope) for envelope in envelopes]
        
    def _create_error_response(self, original_envelope: A2AEnvelope, error_message: str) -> A2AEnvelope:
        """Create error response envelope."""
        return A2AEnvelope(
            message_id=str(uuid.uuid4()),
            conversation_id=original_envelope.conversation_id,
            message_type=MessageType.ERROR,
            sender="system",
            recipient=original_envelope.sender,
            ttl=settings.a2a_timeout,
            payload={
                "error": error_message,
                "original_message_id": original_envelope.message_id
            }
        )
        
    async def cleanup_expired_conversations(self):
        """Clean up expired conversations."""
        now = datetime.utcnow()
        expired = [
            conv_id for conv_id, timeout in self.conversation_timeouts.items()
            if now > timeout
        ]
        
        for conv_id in expired:
            del self.conversation_timeouts[conv_id]
            logger.info(f"Cleaned up expired conversation: {conv_id}")
            
    async def close(self):
        """Close A2A adapter and cleanup."""
        await self.event_store.close()
        await self.cleanup_expired_conversations()
