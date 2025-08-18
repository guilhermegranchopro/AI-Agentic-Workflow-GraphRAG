"""Agent System Manager - Initializes and manages the AI Agents Workflow.

This module provides the main interface for:
- Initializing all agents (Orchestrator, Local RAG, Global RAG, DRIFT RAG)
- Setting up the A2A protocol communication
- Managing agent lifecycle and health monitoring
- Providing the interface for Streamlit integration
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from .base import AgentRegistry, A2AProtocol
from .orchestrator import OrchestratorAgent
from .local_rag_agent import LocalRAGAgent
from .global_rag_agent import GlobalRAGAgent
from .drift_rag_agent import DriftRAGAgent

logger = logging.getLogger(__name__)


class AgentSystemManager:
    """
    Main manager for the AI Agents Workflow system.
    
    Responsibilities:
    - Initialize and register all agents
    - Manage A2A protocol communication
    - Provide simplified interface for Streamlit
    - Monitor system health and performance
    - Handle graceful shutdown
    """
    
    def __init__(self):
        self.registry = AgentRegistry()
        self.protocol = self.registry.get_protocol()
        self.agents = {}
        self.orchestrator = None
        self.is_initialized = False
        self.system_status = 'stopped'
        
    async def initialize_system(self) -> bool:
        """Initialize the complete agent system."""
        try:
            logger.info("Initializing AI Agents Workflow system...")
            
            # Create all agents
            self.orchestrator = OrchestratorAgent()
            local_agent = LocalRAGAgent()
            global_agent = GlobalRAGAgent()
            drift_agent = DriftRAGAgent()
            
            # Store agents for management
            self.agents = {
                'orchestrator': self.orchestrator,
                'local_rag': local_agent,
                'global_rag': global_agent,
                'drift_rag': drift_agent
            }
            
            # Set protocol reference for orchestrator
            self.orchestrator.set_protocol(self.protocol)
            
            # Register all agents with the protocol
            registration_results = []
            for agent_name, agent in self.agents.items():
                logger.info(f"Registering {agent_name} agent...")
                success = await self.protocol.register_agent(agent)
                registration_results.append((agent_name, success))
                
                if success:
                    logger.info(f"✅ {agent_name} agent registered successfully")
                else:
                    logger.error(f"❌ Failed to register {agent_name} agent")
            
            # Check if all agents registered successfully
            successful_registrations = [result for result in registration_results if result[1]]
            
            if len(successful_registrations) == len(self.agents):
                self.is_initialized = True
                self.system_status = 'running'
                logger.info(f"🎉 All {len(self.agents)} agents initialized successfully!")
                
                # Test system connectivity
                await self._test_system_connectivity()
                
                return True
            else:
                failed_agents = [name for name, success in registration_results if not success]
                logger.error(f"Failed to initialize agents: {failed_agents}")
                self.system_status = 'error'
                return False
                
        except Exception as e:
            logger.error(f"System initialization failed: {e}")
            self.system_status = 'error'
            return False
    
    async def _test_system_connectivity(self):
        """Test connectivity between agents."""
        try:
            logger.info("Testing agent system connectivity...")
            
            # Test orchestrator to all RAG agents
            test_query = "test connectivity"
            
            for agent_type in ['local', 'global', 'drift']:
                result = await self.orchestrator._single_agent_query(test_query, agent_type, 'test_session')
                if result.get('error'):
                    logger.warning(f"Connectivity issue with {agent_type} agent: {result.get('response', 'Unknown error')}")
                else:
                    logger.info(f"✅ {agent_type} agent connectivity confirmed")
            
            logger.info("🔗 Agent connectivity test completed")
            
        except Exception as e:
            logger.error(f"Connectivity test failed: {e}")
    
    async def process_user_query(self, query: str, session_id: str = 'default', 
                                preferences: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process a user query through the agent system.
        
        This is the main interface for Streamlit integration.
        """
        if not self.is_initialized:
            return {
                'response': 'Agent system not initialized. Please check system status.',
                'error': True,
                'sources': [],
                'confidence': 0.0
            }
        
        try:
            # Create request message for orchestrator
            from .base import AgentMessage, MessageType
            
            request = AgentMessage(
                type=MessageType.REQUEST,
                sender_id='streamlit_ui',
                recipient_id=self.orchestrator.agent_id,
                content={
                    'type': 'legal_query',
                    'query': query,
                    'session_id': session_id,
                    'preferences': preferences or {}
                }
            )
            
            # Send request to orchestrator
            response = await self.protocol.send_message(request)
            
            if response and response.type != MessageType.ERROR:
                return response.content
            else:
                error_msg = response.content.get('error', 'Unknown error') if response else 'No response from orchestrator'
                return {
                    'response': f'Error processing query: {error_msg}',
                    'error': True,
                    'sources': [],
                    'confidence': 0.0
                }
                
        except Exception as e:
            logger.error(f"Error processing user query: {e}")
            return {
                'response': f'System error: {str(e)}',
                'error': True,
                'sources': [],
                'confidence': 0.0
            }
    
    async def process_multi_agent_query(self, query: str, session_id: str = 'default') -> Dict[str, Any]:
        """Process a query using all agents for comparison."""
        if not self.is_initialized:
            return {
                'response': 'Agent system not initialized.',
                'error': True
            }
        
        try:
            from .base import AgentMessage, MessageType
            
            request = AgentMessage(
                type=MessageType.REQUEST,
                sender_id='streamlit_ui',
                recipient_id=self.orchestrator.agent_id,
                content={
                    'type': 'multi_strategy_query',
                    'query': query,
                    'session_id': session_id
                }
            )
            
            response = await self.protocol.send_message(request)
            
            if response and response.type != MessageType.ERROR:
                return response.content
            else:
                error_msg = response.content.get('error', 'Unknown error') if response else 'No response'
                return {
                    'response': f'Multi-agent query failed: {error_msg}',
                    'error': True
                }
                
        except Exception as e:
            logger.error(f"Multi-agent query error: {e}")
            return {
                'response': f'Multi-agent system error: {str(e)}',
                'error': True
            }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        if not self.is_initialized:
            return {
                'status': 'not_initialized',
                'agents': {},
                'total_agents': 0,
                'active_agents': 0,
                'protocol_status': 'inactive'
            }
        
        protocol_status = self.protocol.get_system_status()
        
        return {
            'status': self.system_status,
            'agents': protocol_status['agents'],
            'total_agents': protocol_status['total_agents'],
            'active_agents': protocol_status['active_agents'],
            'protocol_status': 'active' if self.protocol else 'inactive',
            'initialization_time': datetime.now().isoformat(),
            'system_capabilities': self._get_system_capabilities()
        }
    
    def _get_system_capabilities(self) -> Dict[str, List[str]]:
        """Get capabilities of all agents in the system."""
        capabilities = {}
        
        for agent_name, agent in self.agents.items():
            if hasattr(agent, 'get_capabilities'):
                agent_caps = agent.get_capabilities()
                capabilities[agent_name] = [cap.name for cap in agent_caps]
        
        return capabilities
    
    async def get_performance_report(self) -> Dict[str, Any]:
        """Get performance report from all agents."""
        if not self.is_initialized:
            return {'error': 'System not initialized'}
        
        try:
            report = {
                'system_overview': {
                    'status': self.system_status,
                    'total_agents': len(self.agents),
                    'report_timestamp': datetime.now().isoformat()
                },
                'agent_performance': {}
            }
            
            # Get orchestrator performance
            if self.orchestrator:
                report['orchestrator_performance'] = self.orchestrator.get_performance_report()
            
            # Get individual agent reports
            for agent_name, agent in self.agents.items():
                if hasattr(agent, 'get_specialization_report'):
                    report['agent_performance'][agent_name] = agent.get_specialization_report()
                else:
                    report['agent_performance'][agent_name] = agent.get_status()
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating performance report: {e}")
            return {'error': str(e)}
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform system health check."""
        health_status = {
            'overall_health': 'unknown',
            'system_initialized': self.is_initialized,
            'agent_health': {},
            'protocol_health': 'unknown',
            'connectivity': {},
            'timestamp': datetime.now().isoformat()
        }
        
        if not self.is_initialized:
            health_status['overall_health'] = 'not_initialized'
            return health_status
        
        try:
            # Check individual agent health
            healthy_agents = 0
            for agent_name, agent in self.agents.items():
                if agent.is_active:
                    health_status['agent_health'][agent_name] = 'healthy'
                    healthy_agents += 1
                else:
                    health_status['agent_health'][agent_name] = 'inactive'
            
            # Check protocol health
            protocol_status = self.protocol.get_system_status()
            if protocol_status['active_agents'] == protocol_status['total_agents']:
                health_status['protocol_health'] = 'healthy'
            else:
                health_status['protocol_health'] = 'degraded'
            
            # Overall health assessment
            if healthy_agents == len(self.agents) and health_status['protocol_health'] == 'healthy':
                health_status['overall_health'] = 'healthy'
            elif healthy_agents > len(self.agents) // 2:
                health_status['overall_health'] = 'degraded'
            else:
                health_status['overall_health'] = 'unhealthy'
            
            return health_status
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            health_status['overall_health'] = 'error'
            health_status['error'] = str(e)
            return health_status
    
    async def shutdown(self):
        """Gracefully shutdown the agent system."""
        try:
            logger.info("Shutting down agent system...")
            
            # Shutdown all agents
            for agent_name, agent in self.agents.items():
                logger.info(f"Shutting down {agent_name} agent...")
                agent.is_active = False
            
            # Shutdown protocol
            await self.registry.shutdown()
            
            self.is_initialized = False
            self.system_status = 'stopped'
            
            logger.info("🔚 Agent system shutdown complete")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
    
    def __repr__(self):
        return f"AgentSystemManager(status={self.system_status}, agents={len(self.agents)}, initialized={self.is_initialized})"


# Global instance for Streamlit integration
_global_agent_system = None


async def get_agent_system() -> AgentSystemManager:
    """Get or create the global agent system instance."""
    global _global_agent_system
    
    if _global_agent_system is None:
        _global_agent_system = AgentSystemManager()
        
        # Initialize if not already done
        if not _global_agent_system.is_initialized:
            success = await _global_agent_system.initialize_system()
            if not success:
                logger.error("Failed to initialize agent system")
    
    return _global_agent_system


async def initialize_agents_for_streamlit() -> bool:
    """Initialize the agent system for Streamlit usage."""
    try:
        system = await get_agent_system()
        return system.is_initialized
    except Exception as e:
        logger.error(f"Failed to initialize agents for Streamlit: {e}")
        return False
