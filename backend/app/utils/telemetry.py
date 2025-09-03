import uuid
import time
from typing import Dict, Any, Optional
from contextlib import asynccontextmanager
from datetime import datetime
from loguru import logger


class TelemetryContext:
    """Telemetry context for request tracing."""
    
    def __init__(self, request_id: str = None):
        """Initialize telemetry context."""
        self.request_id = request_id or str(uuid.uuid4())
        self.start_time = time.time()
        self.spans: Dict[str, Dict[str, Any]] = {}
        self.metadata: Dict[str, Any] = {}
        
    def add_span(self, name: str, start_time: float = None, end_time: float = None, metadata: Dict[str, Any] = None):
        """Add a span to the telemetry context."""
        self.spans[name] = {
            "start_time": start_time or time.time(),
            "end_time": end_time,
            "metadata": metadata or {}
        }
        
    def end_span(self, name: str, metadata: Dict[str, Any] = None):
        """End a span in the telemetry context."""
        if name in self.spans:
            self.spans[name]["end_time"] = time.time()
            if metadata:
                self.spans[name]["metadata"].update(metadata)
                
    def add_metadata(self, key: str, value: Any):
        """Add metadata to the telemetry context."""
        self.metadata[key] = value
        
    def get_duration(self) -> float:
        """Get total duration of the telemetry context."""
        return time.time() - self.start_time
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert telemetry context to dictionary."""
        return {
            "request_id": self.request_id,
            "start_time": self.start_time,
            "duration": self.get_duration(),
            "spans": self.spans,
            "metadata": self.metadata
        }


# Global telemetry context storage
_telemetry_contexts: Dict[str, TelemetryContext] = {}


def get_telemetry_context(request_id: str = None) -> TelemetryContext:
    """Get or create telemetry context."""
    if request_id and request_id in _telemetry_contexts:
        return _telemetry_contexts[request_id]
    
    context = TelemetryContext(request_id)
    _telemetry_contexts[context.request_id] = context
    return context


def log_request_start(request_id: str, method: str, path: str, metadata: Dict[str, Any] = None):
    """Log the start of a request."""
    context = get_telemetry_context(request_id)
    context.add_span("request", metadata={
        "method": method,
        "path": path,
        **(metadata or {})
    })
    logger.info(f"Request started: {method} {path} (ID: {request_id})")


def log_request_end(request_id: str, status_code: int, metadata: Dict[str, Any] = None):
    """Log the end of a request."""
    context = get_telemetry_context(request_id)
    context.end_span("request", metadata={
        "status_code": status_code,
        **(metadata or {})
    })
    duration = context.get_duration()
    logger.info(f"Request completed: {status_code} in {duration:.3f}s (ID: {request_id})")


def log_agent_call(request_id: str, agent_name: str, operation: str, metadata: Dict[str, Any] = None):
    """Log an agent call."""
    context = get_telemetry_context(request_id)
    span_name = f"agent.{agent_name}.{operation}"
    context.add_span(span_name, metadata=metadata or {})
    logger.debug(f"Agent call: {agent_name}.{operation} (ID: {request_id})")


def log_agent_result(request_id: str, agent_name: str, operation: str, success: bool, metadata: Dict[str, Any] = None):
    """Log an agent call result."""
    context = get_telemetry_context(request_id)
    span_name = f"agent.{agent_name}.{operation}"
    context.end_span(span_name, metadata={
        "success": success,
        **(metadata or {})
    })
    logger.debug(f"Agent result: {agent_name}.{operation} success={success} (ID: {request_id})")


def log_rag_operation(request_id: str, operation: str, strategy: str, metadata: Dict[str, Any] = None):
    """Log a RAG operation."""
    context = get_telemetry_context(request_id)
    span_name = f"rag.{operation}"
    context.add_span(span_name, metadata={
        "strategy": strategy,
        **(metadata or {})
    })
    logger.debug(f"RAG operation: {operation} strategy={strategy} (ID: {request_id})")


def log_rag_result(request_id: str, operation: str, results_count: int, metadata: Dict[str, Any] = None):
    """Log a RAG operation result."""
    context = get_telemetry_context(request_id)
    span_name = f"rag.{operation}"
    context.end_span(span_name, metadata={
        "results_count": results_count,
        **(metadata or {})
    })
    logger.debug(f"RAG result: {operation} count={results_count} (ID: {request_id})")


@asynccontextmanager
async def telemetry_span(request_id: str, span_name: str, metadata: Dict[str, Any] = None):
    """Context manager for telemetry spans."""
    context = get_telemetry_context(request_id)
    context.add_span(span_name, metadata=metadata or {})
    try:
        yield context
    finally:
        context.end_span(span_name)


def cleanup_telemetry_context(request_id: str):
    """Clean up telemetry context."""
    if request_id in _telemetry_contexts:
        del _telemetry_contexts[request_id]


# OpenTelemetry integration (stub for future implementation)
def setup_opentelemetry():
    """Setup OpenTelemetry integration."""
    # TODO: Implement OpenTelemetry setup
    logger.info("OpenTelemetry integration not yet implemented")


def get_trace_id(request_id: str) -> str:
    """Get trace ID for a request (stub for OpenTelemetry)."""
    return request_id


def get_span_id(request_id: str, span_name: str) -> str:
    """Get span ID for a span (stub for OpenTelemetry)."""
    return f"{request_id}:{span_name}"
