"""AI Agents Framework for UAE Legal GraphRAG System.

This module implements the Agent-to-Agent (A2A) protocol framework with:
- Orchestrator Agent: Main coordinator and UI interface
- Local RAG Agent: Specialized in specific provision retrieval
- Global RAG Agent: Expert in conceptual understanding and broad queries
- DRIFT RAG Agent: Focused on temporal analysis and legal evolution

All agents communicate via Google's A2A protocol for distributed processing.
"""

from .base import BaseAgent, AgentMessage, AgentCapability
from .orchestrator import OrchestratorAgent
from .local_rag_agent import LocalRAGAgent
from .global_rag_agent import GlobalRAGAgent
from .drift_rag_agent import DriftRAGAgent
from .protocol import A2AProtocol, MessageType, AgentRegistry

__all__ = [
    'BaseAgent',
    'AgentMessage', 
    'AgentCapability',
    'OrchestratorAgent',
    'LocalRAGAgent',
    'GlobalRAGAgent', 
    'DriftRAGAgent',
    'A2AProtocol',
    'MessageType',
    'AgentRegistry'
]
