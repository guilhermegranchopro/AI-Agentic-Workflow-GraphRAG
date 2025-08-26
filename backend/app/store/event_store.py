import asyncio
from typing import List, Optional
from datetime import datetime, timedelta
from sqlmodel import SQLModel, Field, create_engine, Session, select
from loguru import logger
from ..schemas.a2a import A2AEnvelope


class A2AEvent(SQLModel, table=True):
    """A2A event model for storing messages."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    message_id: str = Field(index=True)
    conversation_id: str = Field(index=True)
    message_type: str = Field(index=True)
    sender: str = Field(index=True)
    recipient: Optional[str] = Field(default=None, index=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    ttl: int = Field(default=60)
    payload: str = Field()  # JSON string
    metadata: str = Field(default="{}")  # JSON string
    created_at: datetime = Field(default_factory=datetime.utcnow)


class EventStore:
    """Event store for A2A message persistence."""
    
    def __init__(self, db_url: str = "sqlite:///./data/a2a_events.db"):
        """Initialize event store."""
        self.db_url = db_url
        self.engine = None
        self._init_engine()
        
    def _init_engine(self):
        """Initialize database engine."""
        try:
            self.engine = create_engine(
                self.db_url,
                echo=False,
                connect_args={"check_same_thread": False} if "sqlite" in self.db_url else {}
            )
            SQLModel.metadata.create_all(self.engine)
            logger.info(f"Event store initialized: {self.db_url}")
        except Exception as e:
            logger.error(f"Failed to initialize event store: {e}")
            self.engine = None
            
    def _envelope_to_event(self, envelope: A2AEnvelope) -> A2AEvent:
        """Convert A2A envelope to event."""
        import json
        
        return A2AEvent(
            message_id=envelope.message_id,
            conversation_id=envelope.conversation_id,
            message_type=envelope.message_type.value,
            sender=envelope.sender,
            recipient=envelope.recipient,
            timestamp=envelope.timestamp,
            ttl=envelope.ttl,
            payload=json.dumps(envelope.payload),
            metadata=json.dumps(envelope.metadata)
        )
        
    def _event_to_envelope(self, event: A2AEvent) -> A2AEnvelope:
        """Convert event to A2A envelope."""
        import json
        
        return A2AEnvelope(
            message_id=event.message_id,
            conversation_id=event.conversation_id,
            message_type=event.message_type,
            sender=event.sender,
            recipient=event.recipient,
            timestamp=event.timestamp,
            ttl=event.ttl,
            payload=json.loads(event.payload),
            metadata=json.loads(event.metadata)
        )
        
    async def store_envelope(self, envelope: A2AEnvelope) -> bool:
        """Store A2A envelope in event store."""
        if not self.engine:
            logger.error("Event store not initialized")
            return False
            
        try:
            event = self._envelope_to_event(envelope)
            
            with Session(self.engine) as session:
                session.add(event)
                session.commit()
                
            logger.debug(f"Stored A2A envelope: {envelope.message_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to store A2A envelope: {e}")
            return False
            
    async def get_envelopes_by_conversation(self, conversation_id: str) -> List[A2AEnvelope]:
        """Get all envelopes for a conversation."""
        if not self.engine:
            logger.error("Event store not initialized")
            return []
            
        try:
            with Session(self.engine) as session:
                statement = select(A2AEvent).where(
                    A2AEvent.conversation_id == conversation_id
                ).order_by(A2AEvent.timestamp)
                
                events = session.exec(statement).all()
                return [self._event_to_envelope(event) for event in events]
        except Exception as e:
            logger.error(f"Failed to get envelopes for conversation {conversation_id}: {e}")
            return []
            
    async def get_conversation_stats(self, conversation_id: str) -> dict:
        """Get statistics for a conversation."""
        if not self.engine:
            return {"error": "Event store not initialized"}
            
        try:
            with Session(self.engine) as session:
                # Count messages by type
                statement = select(A2AEvent.message_type, A2AEvent).where(
                    A2AEvent.conversation_id == conversation_id
                )
                events = session.exec(statement).all()
                
                stats = {
                    "total_messages": len(events),
                    "by_type": {},
                    "participants": set(),
                    "duration": 0
                }
                
                if events:
                    timestamps = [event.timestamp for event in events]
                    stats["duration"] = (max(timestamps) - min(timestamps)).total_seconds()
                    
                    for event in events:
                        msg_type = event.message_type
                        stats["by_type"][msg_type] = stats["by_type"].get(msg_type, 0) + 1
                        stats["participants"].add(event.sender)
                        if event.recipient:
                            stats["participants"].add(event.recipient)
                            
                    stats["participants"] = list(stats["participants"])
                    
                return stats
        except Exception as e:
            logger.error(f"Failed to get conversation stats: {e}")
            return {"error": str(e)}
            
    async def cleanup_old_events(self, days: int = 7) -> int:
        """Clean up events older than specified days."""
        if not self.engine:
            return 0
            
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            with Session(self.engine) as session:
                statement = select(A2AEvent).where(A2AEvent.timestamp < cutoff_date)
                old_events = session.exec(statement).all()
                
                for event in old_events:
                    session.delete(event)
                    
                session.commit()
                deleted_count = len(old_events)
                logger.info(f"Cleaned up {deleted_count} old events")
                return deleted_count
        except Exception as e:
            logger.error(f"Failed to cleanup old events: {e}")
            return 0
            
    async def close(self):
        """Close event store."""
        if self.engine:
            self.engine.dispose()
            logger.info("Event store closed")
