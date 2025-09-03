from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime
from .a2a import RAGNode, RAGEdge, RAGCitation


class ChatRequest(BaseModel):
    """Chat request model."""
    message: str = Field(..., description="User message")
    conversation_id: Optional[str] = Field(default=None, description="Conversation identifier")
    max_results: int = Field(default=10, description="Maximum retrieval results")
    strategy: str = Field(default="hybrid", description="Retrieval strategy (local/global/drift/hybrid)")


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str = Field(..., description="AI response")
    conversation_id: str = Field(..., description="Conversation identifier")
    citations: List[RAGCitation] = Field(default_factory=list, description="Source citations")
    nodes: List[RAGNode] = Field(default_factory=list, description="Retrieved nodes")
    edges: List[RAGEdge] = Field(default_factory=list, description="Retrieved edges")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Response metadata")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")


class AnalysisRequest(BaseModel):
    """Legal analysis request model."""
    query: str = Field(..., description="Analysis query")
    legal_documents: Optional[List[str]] = Field(default=None, description="Legal documents to analyze")
    analysis_type: str = Field(default="contradiction", description="Analysis type")
    max_depth: int = Field(default=3, description="Maximum analysis depth")


class AnalysisResponse(BaseModel):
    """Legal analysis response model."""
    query: str = Field(..., description="Original query")
    contradictions: List[Dict[str, Any]] = Field(default_factory=list, description="Found contradictions")
    recommendations: List[Dict[str, Any]] = Field(default_factory=list, description="Generated recommendations")
    summary: str = Field(default="", description="Analysis summary")
    confidence: float = Field(default=0.85, description="Analysis confidence score")
    stats: Dict[str, int] = Field(default_factory=dict, description="Analysis statistics")
    harmonizations: List[Dict[str, Any]] = Field(default_factory=list, description="Legal harmonizations")
    citations: List[RAGCitation] = Field(default_factory=list, description="Source citations")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Analysis metadata")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Analysis timestamp")


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Health check timestamp")
    version: str = Field(default="1.0.0", description="Service version")
    dependencies: Dict[str, str] = Field(default_factory=dict, description="Dependency status")


class TraceResponse(BaseModel):
    """Conversation trace response model."""
    conversation_id: str = Field(..., description="Conversation identifier")
    messages: List[Dict[str, Any]] = Field(default_factory=list, description="Message trace")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Trace metadata")
