"""Base Agent classes and A2A Protocol implementation for the UAE Legal GraphRAG system."""

import asyncio
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
import json
import logging

logger = logging.getLogger(__name__)


class MessageType(Enum):
    """A2A Protocol message types."""
    REQUEST = "request"
    RESPONSE = "response" 
    HEARTBEAT = "heartbeat"
    REGISTRATION = "registration"
    CAPABILITY_QUERY = "capability_query"
    ERROR = "error"
    TASK_ASSIGNMENT = "task_assignment"
    TASK_RESULT = "task_result"


@dataclass
class AgentCapability:
    """Defines what an agent can do."""
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    confidence_threshold: float = 0.7
    performance_metrics: Dict[str, float] = field(default_factory=dict)


@dataclass
class AgentMessage:
    """A2A Protocol message structure."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: MessageType = MessageType.REQUEST
    sender_id: str = ""
    recipient_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    content: Dict[str, Any] = field(default_factory=dict)
    correlation_id: Optional[str] = None
    priority: int = 1  # 1=low, 5=high
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            'id': self.id,
            'type': self.type.value,
            'sender_id': self.sender_id,
            'recipient_id': self.recipient_id,
            'timestamp': self.timestamp.isoformat(),
            'content': self.content,
            'correlation_id': self.correlation_id,
            'priority': self.priority
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentMessage':
        """Create message from dictionary."""
        return cls(
            id=data['id'],
            type=MessageType(data['type']),
            sender_id=data['sender_id'],
            recipient_id=data['recipient_id'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            content=data['content'],
            correlation_id=data.get('correlation_id'),
            priority=data.get('priority', 1)
        )


class BaseAgent(ABC):
    """Base class for all agents in the A2A framework."""
    
    def __init__(self, agent_id: str, name: str, description: str):
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.capabilities: List[AgentCapability] = []
        self.is_active = False
        self.message_handlers: Dict[MessageType, Callable] = {}
        self.performance_metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'average_response_time': 0.0,
            'error_rate': 0.0
        }
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup message handlers."""
        self.message_handlers = {
            MessageType.REQUEST: self._handle_request,
            MessageType.HEARTBEAT: self._handle_heartbeat,
            MessageType.CAPABILITY_QUERY: self._handle_capability_query,
            MessageType.TASK_ASSIGNMENT: self._handle_task_assignment
        }
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the agent. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    async def process_request(self, request: AgentMessage) -> AgentMessage:
        """Process a request and return a response. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[AgentCapability]:
        """Return list of agent capabilities. Must be implemented by subclasses."""
        pass
    
    async def handle_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Handle incoming A2A message."""
        start_time = datetime.now()
        
        try:
            handler = self.message_handlers.get(message.type)
            if not handler:
                logger.warning(f"No handler for message type {message.type}")
                return self._create_error_response(message, f"Unsupported message type: {message.type}")
            
            response = await handler(message)
            
            # Update performance metrics
            self.performance_metrics['total_requests'] += 1
            if response and response.type != MessageType.ERROR:
                self.performance_metrics['successful_requests'] += 1
            
            response_time = (datetime.now() - start_time).total_seconds()
            self._update_response_time(response_time)
            
            return response
            
        except Exception as e:
            logger.error(f"Error handling message {message.id}: {e}")
            self.performance_metrics['total_requests'] += 1
            return self._create_error_response(message, str(e))
    
    async def _handle_request(self, message: AgentMessage) -> AgentMessage:
        """Handle generic request."""
        return await self.process_request(message)
    
    async def _handle_heartbeat(self, message: AgentMessage) -> AgentMessage:
        """Handle heartbeat message."""
        return AgentMessage(
            type=MessageType.RESPONSE,
            sender_id=self.agent_id,
            recipient_id=message.sender_id,
            correlation_id=message.id,
            content={
                'status': 'alive',
                'agent_id': self.agent_id,
                'name': self.name,
                'performance': self.performance_metrics
            }
        )
    
    async def _handle_capability_query(self, message: AgentMessage) -> AgentMessage:
        """Handle capability query."""
        capabilities = self.get_capabilities()
        return AgentMessage(
            type=MessageType.RESPONSE,
            sender_id=self.agent_id,
            recipient_id=message.sender_id,
            correlation_id=message.id,
            content={
                'capabilities': [cap.__dict__ for cap in capabilities],
                'agent_info': {
                    'id': self.agent_id,
                    'name': self.name,
                    'description': self.description
                }
            }
        )
    
    async def _handle_task_assignment(self, message: AgentMessage) -> AgentMessage:
        """Handle task assignment."""
        task = message.content.get('task', {})
        
        # Validate if we can handle this task
        if not self._can_handle_task(task):
            return self._create_error_response(
                message, 
                f"Agent {self.agent_id} cannot handle task type: {task.get('type', 'unknown')}"
            )
        
        # Process the task
        result = await self._process_task(task)
        
        return AgentMessage(
            type=MessageType.TASK_RESULT,
            sender_id=self.agent_id,
            recipient_id=message.sender_id,
            correlation_id=message.id,
            content={
                'task_id': task.get('id'),
                'result': result,
                'status': 'completed',
                'agent_id': self.agent_id
            }
        )
    
    def _can_handle_task(self, task: Dict[str, Any]) -> bool:
        """Check if agent can handle a specific task."""
        task_type = task.get('type', '')
        return any(cap.name == task_type for cap in self.get_capabilities())
    
    async def _process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a specific task. Override in subclasses."""
        return {'status': 'not_implemented'}
    
    def _create_error_response(self, original_message: AgentMessage, error: str) -> AgentMessage:
        """Create error response message."""
        return AgentMessage(
            type=MessageType.ERROR,
            sender_id=self.agent_id,
            recipient_id=original_message.sender_id,
            correlation_id=original_message.id,
            content={
                'error': error,
                'original_message_id': original_message.id
            }
        )
    
    def _update_response_time(self, response_time: float):
        """Update average response time metric."""
        current_avg = self.performance_metrics['average_response_time']
        total_requests = self.performance_metrics['total_requests']
        
        if total_requests == 1:
            self.performance_metrics['average_response_time'] = response_time
        else:
            # Running average
            self.performance_metrics['average_response_time'] = (
                (current_avg * (total_requests - 1) + response_time) / total_requests
            )
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status and metrics."""
        return {
            'agent_id': self.agent_id,
            'name': self.name,
            'description': self.description,
            'is_active': self.is_active,
            'capabilities': [cap.name for cap in self.get_capabilities()],
            'performance_metrics': self.performance_metrics
        }


class A2AProtocol:
    """A2A Protocol implementation for agent communication."""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.running = False
        
    async def register_agent(self, agent: BaseAgent) -> bool:
        """Register an agent with the protocol."""
        try:
            success = await agent.initialize()
            if success:
                self.agents[agent.agent_id] = agent
                agent.is_active = True
                logger.info(f"Agent {agent.agent_id} registered successfully")
                return True
            else:
                logger.error(f"Failed to initialize agent {agent.agent_id}")
                return False
        except Exception as e:
            logger.error(f"Error registering agent {agent.agent_id}: {e}")
            return False
    
    async def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent."""
        if agent_id in self.agents:
            self.agents[agent_id].is_active = False
            del self.agents[agent_id]
            logger.info(f"Agent {agent_id} unregistered")
            return True
        return False
    
    async def send_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Send message to an agent and get response."""
        recipient = self.agents.get(message.recipient_id)
        if not recipient:
            logger.error(f"Recipient agent {message.recipient_id} not found")
            return None
        
        try:
            response = await recipient.handle_message(message)
            return response
        except Exception as e:
            logger.error(f"Error sending message to {message.recipient_id}: {e}")
            return None
    
    async def broadcast_message(self, message: AgentMessage, exclude_sender: bool = True) -> List[AgentMessage]:
        """Broadcast message to all agents."""
        responses = []
        
        for agent_id, agent in self.agents.items():
            if exclude_sender and agent_id == message.sender_id:
                continue
                
            message.recipient_id = agent_id
            response = await self.send_message(message)
            if response:
                responses.append(response)
        
        return responses
    
    def get_agents_by_capability(self, capability_name: str) -> List[BaseAgent]:
        """Get agents that have a specific capability."""
        matching_agents = []
        
        for agent in self.agents.values():
            if any(cap.name == capability_name for cap in agent.get_capabilities()):
                matching_agents.append(agent)
        
        return matching_agents
    
    async def query_capabilities(self) -> Dict[str, List[AgentCapability]]:
        """Query all agents for their capabilities."""
        capabilities = {}
        
        for agent_id, agent in self.agents.items():
            capabilities[agent_id] = agent.get_capabilities()
        
        return capabilities
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status."""
        return {
            'total_agents': len(self.agents),
            'active_agents': len([a for a in self.agents.values() if a.is_active]),
            'agents': {agent_id: agent.get_status() for agent_id, agent in self.agents.items()}
        }


class AgentRegistry:
    """Centralized registry for agent discovery and management."""
    
    def __init__(self):
        self.protocol = A2AProtocol()
        self.agent_types = {
            'orchestrator': 'OrchestratorAgent',
            'local_rag': 'LocalRAGAgent', 
            'global_rag': 'GlobalRAGAgent',
            'drift_rag': 'DriftRAGAgent'
        }
    
    async def initialize_system(self) -> bool:
        """Initialize the complete agent system."""
        try:
            # This will be implemented when we create the specific agents
            logger.info("Agent system initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize agent system: {e}")
            return False
    
    def get_protocol(self) -> A2AProtocol:
        """Get the A2A protocol instance."""
        return self.protocol
    
    async def shutdown(self):
        """Shutdown all agents gracefully."""
        for agent_id in list(self.protocol.agents.keys()):
            await self.protocol.unregister_agent(agent_id)
        logger.info("Agent system shutdown complete")
