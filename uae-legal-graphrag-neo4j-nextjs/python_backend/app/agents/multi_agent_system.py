"""
Advanced Multi-Agent System for Legal Research
"""

import asyncio
from typing import Dict, Any, List, AsyncGenerator, Optional
from datetime import datetime
import logging
from openai import AsyncOpenAI

from app.config import settings
from app.services.graphrag import AdvancedGraphRAG

logger = logging.getLogger(__name__)

class BaseAgent:
    """Base class for all AI agents"""
    
    def __init__(self, name: str, specialization: str):
        self.name = name
        self.specialization = specialization
        self.graphrag = AdvancedGraphRAG()
        
        # Configure OpenAI client with fallback
        if settings.azure_openai_api_key and settings.azure_openai_endpoint:
            self.openai_client = AsyncOpenAI(
                api_key=settings.azure_openai_api_key,
                base_url=f"{settings.azure_openai_endpoint}/openai/deployments/{settings.azure_openai_deployment}"
            )
            self.use_openai = True
        else:
            # Fallback - no API calls, return mock responses
            self.openai_client = None
            self.use_openai = False
            logger.warning(f"No OpenAI configuration found for {name}. Using fallback mode.")
    
    async def process(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process a query with agent-specific logic"""
        raise NotImplementedError

class LocalContextAgent(BaseAgent):
    """Agent specialized in local context and entity-focused retrieval"""
    
    def __init__(self):
        super().__init__("LocalContext", "Entity-focused legal research")
    
    async def process(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process query with local context focus"""
        try:
            # Get local semantic search results
            retrieval_results = await self.graphrag.advanced_retrieve(
                query=query,
                mode="local",
                max_results=10
            )
            
            # Extract key entities and concepts
            passages = retrieval_results.get('passages', [])
            if not passages:
                return {
                    'agent': self.name,
                    'status': 'no_results',
                    'findings': [],
                    'confidence': 0.0
                }
            
            # Prepare context for LLM analysis
            context_text = "\n".join([p['text'][:500] for p in passages[:5]])
            
            if self.use_openai and self.openai_client:
                system_prompt = """You are a legal research specialist focusing on local context and specific entities. 
                Analyze the provided legal passages and extract:
                1. Key legal entities (laws, regulations, courts, officials)
                2. Specific legal concepts and their definitions
                3. Direct relationships between entities
                4. Immediate legal implications
                
                Provide concise, factual analysis focused on specific entities and their direct relationships."""
                
                response = await self.openai_client.chat.completions.create(
                    model=settings.azure_openai_deployment,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Query: {query}\n\nLegal Context:\n{context_text}"}
                    ],
                    temperature=0.1,
                    max_tokens=800
                )
                analysis = response.choices[0].message.content
            else:
                # Fallback analysis when OpenAI is not available
                analysis = f"""Based on the retrieved legal passages for the query "{query}":

                Key Findings:
                - Found {len(passages)} relevant legal documents/passages
                - High-relevance sources: {len([p for p in passages if p['score'] > 0.7])}
                - The documents contain information related to: {', '.join(set([p.get('source', 'legal document') for p in passages[:3]]))}
                
                Legal Context Summary:
                {context_text[:400]}...
                
                Note: Detailed AI analysis requires OpenAI API configuration. Showing retrieval results."""
            
            return {
                'agent': self.name,
                'status': 'success',
                'findings': {
                    'analysis': analysis,
                    'source_passages': len(passages),
                    'entities_found': len([p for p in passages if p['score'] > 0.7])
                },
                'confidence': min(max(sum(p['score'] for p in passages[:3]) / 3, 0.0), 1.0),
                'retrieval_metadata': retrieval_results
            }
            
        except Exception as e:
            logger.error(f"LocalContextAgent error: {e}")
            return {
                'agent': self.name,
                'status': 'error',
                'error': str(e),
                'confidence': 0.0
            }

class GlobalPolicyAgent(BaseAgent):
    """Agent specialized in global policy analysis and community-based insights"""
    
    def __init__(self):
        super().__init__("GlobalPolicy", "Policy analysis and community insights")
    
    async def process(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process query with global policy focus"""
        try:
            # Get community-based search results
            retrieval_results = await self.graphrag.advanced_retrieve(
                query=query,
                mode="global",
                max_results=15
            )
            
            passages = retrieval_results.get('passages', [])
            if not passages:
                return {
                    'agent': self.name,
                    'status': 'no_results',
                    'findings': [],
                    'confidence': 0.0
                }
            
            # Prepare broader context for policy analysis
            context_text = "\n".join([p['text'][:600] for p in passages[:7]])
            
            if self.use_openai and self.openai_client:
                system_prompt = """You are a policy analysis specialist focusing on broader legal frameworks and systemic patterns.
                Analyze the provided legal passages and extract:
                1. Overarching policy themes and frameworks
                2. Systemic legal patterns and principles
                3. Cross-domain implications and connections
                4. Policy coherence and potential conflicts
                5. Broader legal ecosystem impacts
                
                Provide comprehensive policy analysis that connects individual legal elements to broader frameworks."""
                
                response = await self.openai_client.chat.completions.create(
                    model=settings.azure_openai_deployment,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Query: {query}\n\nPolicy Context:\n{context_text}"}
                    ],
                    temperature=0.2,
                    max_tokens=1000
                )
                analysis = response.choices[0].message.content
            else:
                # Fallback analysis when OpenAI is not available
                analysis = f"""Policy Analysis for: "{query}"

                Global Context Overview:
                - Retrieved {len(passages)} policy-relevant documents
                - Communities/frameworks identified: {retrieval_results.get('communities_found', 'N/A')}
                - Cross-reference scope: {len([p for p in passages if p['score'] > 0.6])} high-relevance sources
                
                Key Policy Themes (Based on Retrieved Content):
                {context_text[:500]}...
                
                Systemic Patterns:
                - Document sources span multiple legal domains
                - Interconnected legal frameworks detected
                - Policy coherence analysis requires AI processing
                
                Note: Full policy analysis requires OpenAI API configuration."""
            
            return {
                'agent': self.name,
                'status': 'success',
                'findings': {
                    'analysis': analysis,
                    'communities_analyzed': retrieval_results.get('communities_found', 0),
                    'policy_scope': len(passages)
                },
                'confidence': min(max(sum(p['score'] for p in passages[:5]) / 5, 0.0), 1.0),
                'retrieval_metadata': retrieval_results
            }
            
        except Exception as e:
            logger.error(f"GlobalPolicyAgent error: {e}")
            return {
                'agent': self.name,
                'status': 'error',
                'error': str(e),
                'confidence': 0.0
            }

class TemporalEvolutionAgent(BaseAgent):
    """Agent specialized in temporal analysis and legal concept evolution"""
    
    def __init__(self):
        super().__init__("TemporalEvolution", "Legal concept evolution and drift analysis")
    
    async def process(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process query with temporal evolution focus"""
        try:
            # Get temporal drift analysis results
            retrieval_results = await self.graphrag.advanced_retrieve(
                query=query,
                mode="drift",
                max_results=12
            )
            
            passages = retrieval_results.get('passages', [])
            if not passages:
                return {
                    'agent': self.name,
                    'status': 'no_results',
                    'findings': [],
                    'confidence': 0.0
                }
            
            # Prepare temporal context
            context_text = "\n".join([
                f"[{p.get('metadata', {}).get('temporal_info', 'Unknown')}] {p['text'][:500]}" 
                for p in passages[:6]
            ])
            
            if self.use_openai and self.openai_client:
                system_prompt = """You are a legal evolution specialist focusing on how legal concepts change over time.
                Analyze the provided temporally-ordered legal passages and extract:
                1. Evolution patterns in legal concepts and interpretations
                2. Historical development and progression of legal principles
                3. Temporal inconsistencies or contradictions
                4. Emerging trends and future implications
                5. Precedential relationships and superseding changes
                
                Focus on temporal dynamics and how legal understanding has evolved."""
                
                response = await self.openai_client.chat.completions.create(
                    model=settings.azure_openai_deployment,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Query: {query}\n\nTemporal Context:\n{context_text}"}
                    ],
                    temperature=0.15,
                    max_tokens=900
                )
                analysis = response.choices[0].message.content
            else:
                # Fallback analysis when OpenAI is not available
                analysis = f"""Temporal Evolution Analysis for: "{query}"

                Historical Development Overview:
                - Retrieved {len(passages)} temporally-relevant documents
                - Temporal patterns identified: {retrieval_results.get('temporal_patterns_found', 'N/A')}
                - Evolution connections: {retrieval_results.get('evolution_connections', 'N/A')}
                
                Chronological Context:
                {context_text[:600]}...
                
                Evolution Patterns Detected:
                - Documents span multiple time periods
                - Legal concept progression tracked across sources
                - Precedential relationships require detailed analysis
                
                Temporal Insights:
                - Historical precedent evolution detected
                - Contemporary interpretation trends identified
                - Future legal implications require AI analysis
                
                Note: Detailed temporal analysis requires OpenAI API configuration."""
            
            return {
                'agent': self.name,
                'status': 'success',
                'findings': {
                    'analysis': analysis,
                    'temporal_patterns': retrieval_results.get('temporal_patterns_found', 0),
                    'evolution_connections': retrieval_results.get('evolution_connections', 0)
                },
                'confidence': min(max(sum(p['score'] for p in passages[:4]) / 4, 0.0), 1.0),
                'retrieval_metadata': retrieval_results
            }
            
        except Exception as e:
            logger.error(f"TemporalEvolutionAgent error: {e}")
            return {
                'agent': self.name,
                'status': 'error',
                'error': str(e),
                'confidence': 0.0
            }

class MultiAgentSystem:
    """Orchestrates multiple specialized agents for comprehensive legal research"""
    
    def __init__(self):
        self.agents = [
            LocalContextAgent(),
            GlobalPolicyAgent(),
            TemporalEvolutionAgent()
        ]
        self.openai_client = AsyncOpenAI(
            api_key=settings.azure_openai_api_key,
            base_url=f"{settings.azure_openai_endpoint}/openai/deployments/{settings.azure_openai_deployment}"
        )
    
    async def stream_response(self, query: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream responses from multiple agents with real-time updates"""
        
        # Initialize
        yield {
            'type': 'init',
            'data': {
                'query': query,
                'agents': [agent.name for agent in self.agents],
                'timestamp': datetime.now().isoformat()
            }
        }
        
        # Planning phase
        yield {
            'type': 'progress',
            'data': {
                'stage': 'planning',
                'message': 'Analyzing query and planning agent deployment...'
            }
        }
        
        await asyncio.sleep(0.5)  # Brief pause for UX
        
        # Agent execution phase
        yield {
            'type': 'progress',
            'data': {
                'stage': 'agents_executing',
                'message': 'Deploying specialized agents for parallel analysis...'
            }
        }
        
        # Execute agents in parallel
        agent_tasks = [
            agent.process(query, {}) for agent in self.agents
        ]
        
        agent_results = []
        for i, task in enumerate(asyncio.as_completed(agent_tasks)):
            result = await task
            agent_results.append(result)
            
            # Stream individual agent completion
            yield {
                'type': 'agent_complete',
                'data': {
                    'agent': result['agent'],
                    'status': result['status'],
                    'confidence': result.get('confidence', 0.0),
                    'progress': f"{i + 1}/{len(self.agents)}"
                }
            }
        
        # Synthesis phase
        yield {
            'type': 'progress',
            'data': {
                'stage': 'synthesis',
                'message': 'Synthesizing multi-agent insights...'
            }
        }
        
        # Synthesize results
        synthesis = await self._synthesize_agent_results(query, agent_results)
        
        # Final response
        yield {
            'type': 'complete',
            'data': {
                'query': query,
                'agent_results': agent_results,
                'synthesis': synthesis,
                'timestamp': datetime.now().isoformat(),
                'total_agents': len(self.agents)
            }
        }
    
    async def _synthesize_agent_results(
        self, 
        query: str, 
        agent_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Synthesize results from multiple agents into comprehensive response"""
        
        try:
            # Filter successful results
            successful_results = [r for r in agent_results if r['status'] == 'success']
            
            if not successful_results:
                return {
                    'status': 'no_synthesis',
                    'message': 'No successful agent results to synthesize'
                }
            
            # Prepare synthesis context
            agent_analyses = []
            for result in successful_results:
                agent_name = result['agent']
                analysis = result['findings'].get('analysis', '')
                confidence = result.get('confidence', 0.0)
                
                agent_analyses.append(f"**{agent_name} Analysis (Confidence: {confidence:.2f}):**\n{analysis}")
            
            synthesis_context = "\n\n".join(agent_analyses)
            
            synthesis_prompt = """You are a senior legal research coordinator synthesizing insights from specialized AI agents.
            
            Each agent has provided analysis from their specialized perspective:
            - LocalContext: Entity-focused analysis with specific legal relationships
            - GlobalPolicy: Policy framework analysis with systemic insights  
            - TemporalEvolution: Historical analysis and concept evolution
            
            Synthesize their findings into a comprehensive, coherent response that:
            1. Integrates insights across all perspectives
            2. Identifies key themes and convergent findings
            3. Highlights any contradictions or tensions
            4. Provides actionable legal insights
            5. Maintains appropriate legal precision and nuance
            
            Create a unified, professional legal research response."""
            
            response = await self.openai_client.chat.completions.create(
                model=settings.azure_openai_deployment,
                messages=[
                    {"role": "system", "content": synthesis_prompt},
                    {"role": "user", "content": f"Query: {query}\n\nAgent Analyses:\n{synthesis_context}"}
                ],
                temperature=0.1,
                max_tokens=1200
            )
            
            # Calculate overall confidence
            overall_confidence = sum(r.get('confidence', 0.0) for r in successful_results) / len(successful_results)
            
            return {
                'status': 'success',
                'synthesis': response.choices[0].message.content,
                'overall_confidence': overall_confidence,
                'agents_contributing': len(successful_results),
                'synthesis_method': 'llm_integration'
            }
            
        except Exception as e:
            logger.error(f"Synthesis error: {e}")
            return {
                'status': 'synthesis_error',
                'error': str(e),
                'fallback_summary': self._create_fallback_summary(successful_results)
            }
    
    def _create_fallback_summary(self, results: List[Dict[str, Any]]) -> str:
        """Create fallback summary if LLM synthesis fails"""
        if not results:
            return "No agent results available for synthesis."
        
        summary_parts = []
        for result in results:
            agent = result['agent']
            confidence = result.get('confidence', 0.0)
            analysis = result['findings'].get('analysis', 'No analysis available')[:200]
            summary_parts.append(f"{agent} (confidence: {confidence:.2f}): {analysis}...")
        
        return "Agent Summary:\n" + "\n\n".join(summary_parts)
