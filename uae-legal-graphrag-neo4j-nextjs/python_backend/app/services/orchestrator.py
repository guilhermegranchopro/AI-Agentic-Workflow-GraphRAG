"""
Orchestrator service for complex workflows
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

from app.config import settings
from app.services.graphrag import AdvancedGraphRAG
from app.agents.multi_agent_system import MultiAgentSystem

logger = logging.getLogger(__name__)

class PythonOrchestrator:
    """Orchestrates complex multi-step legal research workflows"""
    
    def __init__(self):
        self.graphrag = AdvancedGraphRAG()
        self.multi_agent_system = MultiAgentSystem()
    
    async def execute_workflow(
        self,
        query: str,
        mode: str = "comprehensive",
        max_results: int = 20
    ) -> Dict[str, Any]:
        """Execute comprehensive legal research workflow"""
        
        workflow_results = {
            'query': query,
            'mode': mode,
            'timestamp': datetime.now().isoformat(),
            'stages': []
        }
        
        try:
            # Stage 1: Advanced retrieval
            stage1_start = datetime.now()
            retrieval_results = await self.graphrag.advanced_retrieve(
                query=query,
                mode="hybrid",
                max_results=max_results
            )
            
            workflow_results['stages'].append({
                'stage': 'advanced_retrieval',
                'status': 'completed',
                'duration': (datetime.now() - stage1_start).total_seconds(),
                'results_count': len(retrieval_results.get('passages', []))
            })
            
            # Stage 2: Multi-agent analysis (collect all results)
            stage2_start = datetime.now()
            agent_results = []
            
            async for chunk in self.multi_agent_system.stream_response(query):
                if chunk['type'] == 'complete':
                    agent_results = chunk['data']['agent_results']
                    synthesis = chunk['data']['synthesis']
                    break
            
            workflow_results['stages'].append({
                'stage': 'multi_agent_analysis',
                'status': 'completed',
                'duration': (datetime.now() - stage2_start).total_seconds(),
                'agents_completed': len(agent_results)
            })
            
            # Stage 3: Final integration
            stage3_start = datetime.now()
            final_results = {
                'retrieval': retrieval_results,
                'agent_analysis': agent_results,
                'synthesis': synthesis,
                'confidence_score': synthesis.get('overall_confidence', 0.0),
                'recommendation': self._generate_recommendation(retrieval_results, agent_results)
            }
            
            workflow_results['stages'].append({
                'stage': 'final_integration',
                'status': 'completed',
                'duration': (datetime.now() - stage3_start).total_seconds()
            })
            
            workflow_results['final_results'] = final_results
            workflow_results['status'] = 'success'
            
        except Exception as e:
            logger.error(f"Workflow execution error: {e}")
            workflow_results['status'] = 'error'
            workflow_results['error'] = str(e)
        
        return workflow_results
    
    def _generate_recommendation(
        self,
        retrieval_results: Dict[str, Any],
        agent_results: List[Dict[str, Any]]
    ) -> str:
        """Generate workflow recommendation based on results"""
        
        retrieval_quality = len(retrieval_results.get('passages', []))
        agent_success_count = len([r for r in agent_results if r['status'] == 'success'])
        
        if retrieval_quality >= 10 and agent_success_count >= 2:
            return "High-confidence comprehensive analysis available"
        elif retrieval_quality >= 5 and agent_success_count >= 1:
            return "Moderate-confidence analysis available, consider additional research"
        else:
            return "Limited results found, recommend query refinement or alternative search strategies"
    
    async def neo4j_health(self) -> bool:
        """Check Neo4j health"""
        return await self.graphrag.health_check()
    
    async def openai_health(self) -> bool:
        """Check OpenAI health"""
        try:
            # Simple test call
            from openai import AsyncOpenAI
            client = AsyncOpenAI(
                api_key=settings.azure_openai_api_key,
                base_url=f"{settings.azure_openai_endpoint}/openai/deployments/{settings.azure_openai_deployment}",
                api_version=settings.azure_openai_api_version
            )
            
            response = await client.chat.completions.create(
                model=settings.azure_openai_deployment,
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            logger.error(f"OpenAI health check failed: {e}")
            return False
