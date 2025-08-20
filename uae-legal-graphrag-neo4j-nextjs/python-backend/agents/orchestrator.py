"""Orchestrator Agent - Main coordinator for the UAE Legal GraphRAG system.

The orchestrator manages user interactions, coordinates with specialized RAG agents,
and synthesizes responses using the A2A protocol.
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

from .base import BaseAgent, AgentMessage, AgentCapability, MessageType
from src.embeddings.azure_openai import get_azure_openai_client
from src.config import settings

logger = logging.getLogger(__name__)


class OrchestratorAgent(BaseAgent):
    """
    Main orchestrator agent that:
    1. Handles user interactions via the Streamlit UI
    2. Analyzes queries and determines optimal RAG strategy
    3. Coordinates with specialized RAG agents via A2A protocol
    4. Synthesizes final responses using Azure OpenAI
    5. Manages conversation context and agent coordination
    """
    
    def __init__(self):
        super().__init__(
            agent_id="orchestrator_001",
            name="Legal Assistant Orchestrator", 
            description="Main coordinator for UAE Legal GraphRAG system with A2A protocol"
        )
        self.protocol = None
        self.conversation_context = {}
        self.agent_performance_history = {}
        
    async def initialize(self) -> bool:
        """Initialize the orchestrator agent."""
        try:
            # Test Azure OpenAI connection
            client = get_azure_openai_client()
            
            # Initialize conversation tracking
            self.conversation_context = {}
            self.agent_performance_history = {
                'local_rag': {'total_queries': 0, 'avg_confidence': 0.0, 'avg_response_time': 0.0},
                'global_rag': {'total_queries': 0, 'avg_confidence': 0.0, 'avg_response_time': 0.0},
                'drift_rag': {'total_queries': 0, 'avg_confidence': 0.0, 'avg_response_time': 0.0}
            }
            
            logger.info("Orchestrator agent initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize orchestrator: {e}")
            return False
    
    def set_protocol(self, protocol):
        """Set the A2A protocol instance."""
        self.protocol = protocol
    
    def get_capabilities(self) -> List[AgentCapability]:
        """Define orchestrator capabilities."""
        return [
            AgentCapability(
                name="query_coordination",
                description="Coordinate complex legal queries across multiple RAG agents",
                input_schema={
                    "query": {"type": "string", "description": "Legal question"},
                    "context": {"type": "object", "description": "Conversation context"},
                    "preferences": {"type": "object", "description": "User preferences"}
                },
                output_schema={
                    "response": {"type": "string", "description": "Synthesized legal response"},
                    "sources": {"type": "array", "description": "Source citations"},
                    "confidence": {"type": "number", "description": "Response confidence"},
                    "strategy_used": {"type": "string", "description": "RAG strategy employed"}
                },
                confidence_threshold=0.8
            ),
            AgentCapability(
                name="multi_agent_synthesis",
                description="Synthesize responses from multiple specialized agents",
                input_schema={
                    "agent_responses": {"type": "array", "description": "Responses from RAG agents"},
                    "original_query": {"type": "string", "description": "Original user query"}
                },
                output_schema={
                    "synthesized_response": {"type": "string", "description": "Combined response"},
                    "confidence_scores": {"type": "object", "description": "Agent confidence scores"}
                },
                confidence_threshold=0.75
            ),
            AgentCapability(
                name="conversation_management",
                description="Manage ongoing legal conversations and context",
                input_schema={
                    "session_id": {"type": "string", "description": "Conversation session ID"},
                    "message_history": {"type": "array", "description": "Previous messages"}
                },
                output_schema={
                    "updated_context": {"type": "object", "description": "Updated conversation context"}
                },
                confidence_threshold=0.9
            )
        ]
    
    async def process_request(self, request: AgentMessage) -> AgentMessage:
        """Process incoming requests from the UI or other agents."""
        try:
            request_type = request.content.get('type', 'unknown')
            
            if request_type == 'legal_query':
                return await self._handle_legal_query(request)
            elif request_type == 'multi_strategy_query':
                return await self._handle_multi_strategy_query(request)
            elif request_type == 'conversation_update':
                return await self._handle_conversation_update(request)
            else:
                return self._create_error_response(request, f"Unknown request type: {request_type}")
                
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            return self._create_error_response(request, str(e))
    
    async def _handle_legal_query(self, request: AgentMessage) -> AgentMessage:
        """Handle a legal query with intelligent agent coordination."""
        query = request.content.get('query', '')
        session_id = request.content.get('session_id', 'default')
        preferences = request.content.get('preferences', {})
        
        # Analyze query to determine strategy
        query_analysis = await self._analyze_query(query)
        
        # Determine which agents to consult
        strategy = preferences.get('rag_strategy', 'smart_auto')
        
        if strategy == 'smart_auto':
            # Use intelligent coordination
            response = await self._smart_coordination(query, query_analysis, session_id)
        elif strategy == 'multi_agent':
            # Query all agents and synthesize
            response = await self._multi_agent_coordination(query, session_id)
        else:
            # Single agent strategy
            response = await self._single_agent_query(query, strategy, session_id)
        
        return AgentMessage(
            type=MessageType.RESPONSE,
            sender_id=self.agent_id,
            recipient_id=request.sender_id,
            correlation_id=request.id,
            content=response
        )
    
    async def _analyze_query(self, query: str) -> Dict[str, Any]:
        """Analyze query using Azure OpenAI to determine optimal strategy."""
        try:
            client = get_azure_openai_client()
            
            analysis_prompt = f"""
            Analyze this legal query and provide a JSON response with the following structure:
            {{
                "query_type": "specific_provision|definition|procedural|comparative|penalty|rights_obligations|general",
                "complexity": "low|medium|high",
                "temporal_aspects": true/false,
                "specific_entities": ["list", "of", "legal", "entities"],
                "recommended_strategy": "local|global|drift",
                "confidence": 0.0-1.0,
                "reasoning": "explanation of the analysis"
            }}
            
            Query: "{query}"
            """
            
            response = await asyncio.to_thread(
                client.chat.completions.create,
                model=settings.azure_openai_chat_deployment,
                messages=[
                    {"role": "system", "content": "You are an expert legal query analyzer. Respond only with valid JSON."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            import json
            analysis = json.loads(response.choices[0].message.content)
            return analysis
            
        except Exception as e:
            logger.error(f"Query analysis failed: {e}")
            # Fallback analysis
            return {
                "query_type": "general",
                "complexity": "medium",
                "temporal_aspects": "recent" in query.lower() or "latest" in query.lower(),
                "recommended_strategy": "local",
                "confidence": 0.5,
                "reasoning": "Fallback analysis due to processing error"
            }
    
    async def _smart_coordination(self, query: str, analysis: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Intelligent coordination based on query analysis."""
        recommended_strategy = analysis.get('recommended_strategy', 'local')
        confidence = analysis.get('confidence', 0.5)
        
        # If confidence is low, try multiple strategies
        if confidence < 0.7:
            return await self._multi_agent_coordination(query, session_id)
        
        # High confidence - use recommended strategy
        return await self._single_agent_query(query, recommended_strategy, session_id)
    
    async def _single_agent_query(self, query: str, strategy: str, session_id: str) -> Dict[str, Any]:
        """Query a single specialized agent."""
        if not self.protocol:
            raise Exception("A2A Protocol not initialized")
        
        # Map strategy to agent ID
        agent_mapping = {
            'local': 'local_rag_001',
            'global': 'global_rag_001', 
            'drift': 'drift_rag_001'
        }
        
        target_agent_id = agent_mapping.get(strategy)
        if not target_agent_id:
            raise Exception(f"Unknown strategy: {strategy}")
        
        # Create task message
        task_message = AgentMessage(
            type=MessageType.TASK_ASSIGNMENT,
            sender_id=self.agent_id,
            recipient_id=target_agent_id,
            content={
                'task': {
                    'id': f"{session_id}_{datetime.now().timestamp()}",
                    'type': f'{strategy}_rag_query',
                    'query': query,
                    'session_id': session_id,
                    'metadata': {
                        'timestamp': datetime.now().isoformat(),
                        'priority': 'normal'
                    }
                }
            }
        )
        
        # Send to agent
        start_time = datetime.now()
        response = await self.protocol.send_message(task_message)
        response_time = (datetime.now() - start_time).total_seconds()
        
        if not response or response.type == MessageType.ERROR:
            return {
                'response': f"Error querying {strategy} agent: {response.content.get('error', 'Unknown error') if response else 'No response'}",
                'sources': [],
                'confidence': 0.0,
                'strategy_used': strategy,
                'error': True
            }
        
        # Update performance tracking
        self._update_agent_performance(strategy, response_time, response.content.get('confidence', 0.5))
        
        result = response.content.get('result', {})
        return {
            'response': result.get('response', 'No response generated'),
            'sources': result.get('sources', []),
            'confidence': result.get('confidence', 0.5),
            'strategy_used': strategy,
            'response_time': response_time,
            'agent_id': target_agent_id
        }
    
    async def _multi_agent_coordination(self, query: str, session_id: str) -> Dict[str, Any]:
        """Query multiple agents and synthesize the best response."""
        strategies = ['local', 'global', 'drift']
        
        # Query all agents in parallel
        tasks = []
        for strategy in strategies:
            task = self._single_agent_query(query, strategy, session_id)
            tasks.append(task)
        
        # Wait for all responses
        try:
            responses = await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            logger.error(f"Error in multi-agent coordination: {e}")
            return {
                'response': f"Error in multi-agent coordination: {str(e)}",
                'sources': [],
                'confidence': 0.0,
                'strategy_used': 'multi_agent_error'
            }
        
        # Filter successful responses
        valid_responses = []
        for i, response in enumerate(responses):
            if isinstance(response, dict) and not response.get('error', False):
                response['strategy'] = strategies[i]
                valid_responses.append(response)
        
        if not valid_responses:
            return {
                'response': "All agents failed to provide valid responses",
                'sources': [],
                'confidence': 0.0,
                'strategy_used': 'multi_agent_failed'
            }
        
        # Synthesize the best response
        return await self._synthesize_responses(query, valid_responses)
    
    async def _synthesize_responses(self, query: str, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Synthesize multiple agent responses into a coherent answer."""
        try:
            client = get_azure_openai_client()
            
            # Prepare synthesis prompt
            response_summaries = []
            all_sources = []
            
            for resp in responses:
                response_summaries.append({
                    'strategy': resp['strategy'],
                    'response': resp['response'],
                    'confidence': resp['confidence'],
                    'sources': resp['sources']
                })
                all_sources.extend(resp['sources'])
            
            synthesis_prompt = f"""
            You are synthesizing multiple legal research responses for this query: "{query}"
            
            Agent Responses:
            {chr(10).join([f"**{r['strategy'].upper()} RAG** (confidence: {r['confidence']:.1%}): {r['response']}" for r in response_summaries])}
            
            Create a comprehensive, accurate legal response that:
            1. Combines the best insights from all agents
            2. Prioritizes higher-confidence responses
            3. Maintains legal accuracy and proper citations
            4. Provides a clear, coherent answer
            5. Notes any conflicting information
            
            Format as a professional legal response.
            """
            
            response = await asyncio.to_thread(
                client.chat.completions.create,
                model=settings.azure_openai_chat_deployment,
                messages=[
                    {"role": "system", "content": "You are an expert legal assistant synthesizing multiple research sources."},
                    {"role": "user", "content": synthesis_prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            synthesized_response = response.choices[0].message.content
            
            # Calculate overall confidence (weighted average)
            total_confidence = sum(r['confidence'] for r in responses)
            avg_confidence = total_confidence / len(responses) if responses else 0.0
            
            # Remove duplicate sources
            unique_sources = []
            seen_sources = set()
            for source in all_sources:
                source_key = source.get('title', '') + source.get('content', '')
                if source_key not in seen_sources:
                    unique_sources.append(source)
                    seen_sources.add(source_key)
            
            return {
                'response': synthesized_response,
                'sources': unique_sources[:10],  # Limit to top 10 sources
                'confidence': avg_confidence,
                'strategy_used': 'multi_agent_synthesis',
                'agent_responses': len(responses),
                'synthesis_method': 'azure_openai_gpt4o'
            }
            
        except Exception as e:
            logger.error(f"Response synthesis failed: {e}")
            # Fallback: return highest confidence response
            best_response = max(responses, key=lambda x: x['confidence'])
            best_response['strategy_used'] = f"{best_response['strategy']}_fallback"
            return best_response
    
    async def _handle_multi_strategy_query(self, request: AgentMessage) -> AgentMessage:
        """Handle requests for multi-strategy responses."""
        query = request.content.get('query', '')
        session_id = request.content.get('session_id', 'default')
        
        response = await self._multi_agent_coordination(query, session_id)
        
        return AgentMessage(
            type=MessageType.RESPONSE,
            sender_id=self.agent_id,
            recipient_id=request.sender_id,
            correlation_id=request.id,
            content=response
        )
    
    async def _handle_conversation_update(self, request: AgentMessage) -> AgentMessage:
        """Handle conversation context updates."""
        session_id = request.content.get('session_id', 'default')
        update_data = request.content.get('update_data', {})
        
        # Update conversation context
        if session_id not in self.conversation_context:
            self.conversation_context[session_id] = {
                'messages': [],
                'preferences': {},
                'legal_entities': set(),
                'session_start': datetime.now().isoformat()
            }
        
        self.conversation_context[session_id].update(update_data)
        
        return AgentMessage(
            type=MessageType.RESPONSE,
            sender_id=self.agent_id,
            recipient_id=request.sender_id,
            correlation_id=request.id,
            content={'status': 'updated', 'session_id': session_id}
        )
    
    def _update_agent_performance(self, strategy: str, response_time: float, confidence: float):
        """Update performance tracking for agents."""
        if strategy in self.agent_performance_history:
            perf = self.agent_performance_history[strategy]
            perf['total_queries'] += 1
            
            # Update running averages
            total = perf['total_queries']
            perf['avg_response_time'] = ((perf['avg_response_time'] * (total - 1)) + response_time) / total
            perf['avg_confidence'] = ((perf['avg_confidence'] * (total - 1)) + confidence) / total
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get performance report for all agents."""
        return {
            'orchestrator_metrics': self.performance_metrics,
            'agent_performance': self.agent_performance_history,
            'active_sessions': len(self.conversation_context),
            'system_uptime': datetime.now().isoformat()
        }
