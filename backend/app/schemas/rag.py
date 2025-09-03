from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from enum import Enum
from .a2a import RAGNode, RAGEdge, RAGCitation


class RetrievalStrategy(str, Enum):
    """RAG retrieval strategies."""
    LOCAL = "local"
    GLOBAL = "global"
    DRIFT = "drift"
    HYBRID = "hybrid"


class AnalysisType(str, Enum):
    """Legal analysis types."""
    CONTRADICTION = "contradiction"
    HARMONIZATION = "harmonization"
    COMPLIANCE = "compliance"
    INTERPRETATION = "interpretation"


class RAGQuery(BaseModel):
    """RAG query model."""
    query: str = Field(..., description="Search query")
    strategy: RetrievalStrategy = Field(default=RetrievalStrategy.HYBRID, description="Retrieval strategy")
    max_results: int = Field(default=10, description="Maximum results")
    similarity_threshold: float = Field(default=0.7, description="Similarity threshold")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Query filters")


class RAGResult(BaseModel):
    """RAG result model."""
    query: str = Field(..., description="Original query")
    nodes: List[RAGNode] = Field(default_factory=list, description="Retrieved nodes")
    edges: List[RAGEdge] = Field(default_factory=list, description="Retrieved edges")
    citations: List[RAGCitation] = Field(default_factory=list, description="Citations")
    coverage: float = Field(default=0.0, description="Knowledge graph coverage")
    confidence: float = Field(default=0.0, description="Result confidence")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Result metadata")


class AnalysisRule(BaseModel):
    """Legal analysis rule."""
    rule_id: str = Field(..., description="Rule identifier")
    name: str = Field(..., description="Rule name")
    description: str = Field(..., description="Rule description")
    category: str = Field(..., description="Rule category")
    severity: str = Field(..., description="Rule severity")
    conditions: List[Dict[str, Any]] = Field(default_factory=list, description="Rule conditions")


class AnalysisFinding(BaseModel):
    """Legal analysis finding."""
    finding_id: str = Field(..., description="Finding identifier")
    rule_id: str = Field(..., description="Related rule ID")
    severity: str = Field(..., description="Finding severity")
    description: str = Field(..., description="Finding description")
    evidence: List[RAGCitation] = Field(default_factory=list, description="Supporting evidence")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Finding metadata")


class AnalysisReport(BaseModel):
    """Legal analysis report."""
    report_id: str = Field(..., description="Report identifier")
    query: str = Field(..., description="Analysis query")
    findings: List[AnalysisFinding] = Field(default_factory=list, description="Analysis findings")
    summary: str = Field(..., description="Report summary")
    risk_level: str = Field(..., description="Overall risk level")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Report metadata")
