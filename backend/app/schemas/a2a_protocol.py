"""
A2A Protocol Schemas - Official Agent2Agent Protocol Implementation
==================================================================

This module implements the official A2A Protocol schemas for the UAE Legal GraphRAG system.
Following the A2A Protocol specification: https://a2a-protocol.org/dev/specification/
"""

from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class TransportType(str, Enum):
    """A2A Protocol transport types."""
    HTTP_JSON = "HTTP+JSON"
    JSON_RPC = "JSON-RPC"
    GRPC = "gRPC"


class SecurityScheme(BaseModel):
    """A2A Protocol security scheme."""
    type: str = Field(..., description="Security scheme type")
    scheme: str = Field(..., description="Security scheme scheme")
    description: Optional[str] = Field(None, description="Security scheme description")


class Skill(BaseModel):
    """A2A Protocol skill definition."""
    id: str = Field(..., description="Unique skill identifier")
    name: str = Field(..., description="Human-readable skill name")
    description: str = Field(..., description="Skill description")
    inputModes: List[str] = Field(..., description="Supported input modes")
    outputModes: List[str] = Field(..., description="Supported output modes")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Skill parameters")


class AgentCard(BaseModel):
    """A2A Protocol Agent Card - public discovery document."""
    protocolVersion: str = Field("0.3.0", description="A2A Protocol version")
    name: str = Field(..., description="Agent name")
    description: str = Field(..., description="Agent description")
    service: Dict[str, str] = Field(..., description="Service information")
    transports: List[Dict[str, str]] = Field(..., description="Supported transports")
    capabilities: Dict[str, Any] = Field(..., description="Agent capabilities")
    securitySchemes: List[SecurityScheme] = Field(..., description="Security schemes")
    skills: List[Skill] = Field(..., description="Available skills")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class MessagePart(BaseModel):
    """A2A Protocol message part."""
    kind: str = Field(..., description="Message part kind")
    text: Optional[str] = Field(None, description="Text content")
    data: Optional[Dict[str, Any]] = Field(None, description="Data content")
    mimeType: Optional[str] = Field(None, description="MIME type")


class Message(BaseModel):
    """A2A Protocol message."""
    role: str = Field(..., description="Message role")
    parts: List[MessagePart] = Field(..., description="Message parts")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Message metadata")


class TaskStatus(BaseModel):
    """A2A Protocol task status."""
    state: str = Field(..., description="Task state")
    progress: Optional[float] = Field(None, description="Progress percentage")
    message: Optional[str] = Field(None, description="Status message")
    timestamp: Optional[datetime] = Field(None, description="Status timestamp")


class Task(BaseModel):
    """A2A Protocol task."""
    id: str = Field(..., description="Task identifier")
    status: TaskStatus = Field(..., description="Task status")
    artifacts: Optional[List[Dict[str, Any]]] = Field(None, description="Task artifacts")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Task metadata")


class MessageSendRequest(BaseModel):
    """A2A Protocol message:send request."""
    message: Message = Field(..., description="Message to send")
    configuration: Optional[Dict[str, Any]] = Field(None, description="Configuration")
    context: Optional[Dict[str, Any]] = Field(None, description="Request context")


class MessageSendResponse(BaseModel):
    """A2A Protocol message:send response."""
    message: Optional[Message] = Field(None, description="Response message")
    task: Optional[Task] = Field(None, description="Task for long-running operations")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Response metadata")


class MessageStreamRequest(BaseModel):
    """A2A Protocol message:stream request."""
    taskId: str = Field(..., description="Task identifier to stream")
    configuration: Optional[Dict[str, Any]] = Field(None, description="Stream configuration")


class TaskGetResponse(BaseModel):
    """A2A Protocol tasks:get response."""
    id: str = Field(..., description="Task identifier")
    status: TaskStatus = Field(..., description="Task status")
    artifacts: List[Dict[str, Any]] = Field(..., description="Task artifacts")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Task metadata")


# UAE Legal GraphRAG specific A2A schemas
class LegalAnalysisRequest(BaseModel):
    """Legal analysis request for A2A Protocol."""
    query: str = Field(..., description="Legal analysis query")
    analysis_type: str = Field(..., description="Type of analysis")
    max_depth: int = Field(default=3, description="Analysis depth")
    strategy: str = Field(default="hybrid", description="GraphRAG strategy")


class LegalAnalysisResponse(BaseModel):
    """Legal analysis response for A2A Protocol."""
    contradictions: List[Dict[str, Any]] = Field(..., description="Found contradictions")
    harmonizations: List[Dict[str, Any]] = Field(..., description="Harmonization opportunities")
    citations: List[Dict[str, Any]] = Field(..., description="Legal citations")
    metadata: Dict[str, Any] = Field(..., description="Analysis metadata")


class GraphRAGRequest(BaseModel):
    """GraphRAG request for A2A Protocol."""
    message: str = Field(..., description="User message")
    strategy: str = Field(..., description="GraphRAG strategy")
    max_results: int = Field(default=5, description="Maximum results")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")


class GraphRAGResponse(BaseModel):
    """GraphRAG response for A2A Protocol."""
    response: str = Field(..., description="AI-generated response")
    citations: List[Dict[str, Any]] = Field(..., description="Legal citations")
    nodes: List[Dict[str, Any]] = Field(..., description="Knowledge graph nodes")
    edges: List[Dict[str, Any]] = Field(..., description="Knowledge graph edges")
    metadata: Dict[str, Any] = Field(..., description="Response metadata")
