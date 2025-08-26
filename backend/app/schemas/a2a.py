from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from enum import Enum
from datetime import datetime


class MessageType(str, Enum):
    """A2A message types."""
    TASK = "task"
    RESULT = "result"
    ERROR = "error"
    HEARTBEAT = "heartbeat"


class RAGNode(BaseModel):
    """RAG graph node representation."""
    id: str = Field(..., description="Unique node identifier")
    type: str = Field(..., description="Node type (e.g., 'law', 'article', 'case')")
    content: str = Field(..., description="Node content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Node metadata")
    score: Optional[float] = Field(default=None, description="Relevance score")


class RAGEdge(BaseModel):
    """RAG graph edge representation."""
    source: str = Field(..., description="Source node ID")
    target: str = Field(..., description="Target node ID")
    type: str = Field(..., description="Edge type (e.g., 'references', 'contradicts')")
    weight: Optional[float] = Field(default=None, description="Edge weight")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Edge metadata")


class RAGCitation(BaseModel):
    """Citation information for RAG results."""
    node_id: str = Field(..., description="Cited node ID")
    node_type: str = Field(..., description="Cited node type")
    content: str = Field(..., description="Cited content excerpt")
    score: float = Field(..., description="Citation relevance score")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Citation metadata")


class A2AEnvelope(BaseModel):
    """A2A protocol envelope for message routing."""
    message_id: str = Field(..., description="Unique message identifier")
    conversation_id: str = Field(..., description="Conversation identifier")
    message_type: MessageType = Field(..., description="Message type")
    sender: str = Field(..., description="Sender agent identifier")
    recipient: Optional[str] = Field(default=None, description="Recipient agent identifier")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Message timestamp")
    ttl: int = Field(default=60, description="Time to live in seconds")
    payload: Dict[str, Any] = Field(..., description="Message payload")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Message metadata")
