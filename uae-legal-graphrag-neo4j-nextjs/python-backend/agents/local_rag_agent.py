"""Local RAG Agent - Specialized agent for specific provision retrieval.

This agent excels at:
- Finding specific articles, sections, and clauses
- Retrieving exact legal text and provisions
- Handling precise legal citations
- Processing targeted queries about specific laws
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

from .base import BaseAgent, AgentMessage, AgentCapability, MessageType
from src.graph.tools import local_rag_query_simplified as local_rag_query

logger = logging.getLogger(__name__)


class LocalRAGAgent(BaseAgent):
    """
    Specialized agent for Local RAG queries focusing on:
    - Specific legal provisions and articles
    - Exact text retrieval from legal documents
    - Precise citation and reference handling
    - High-accuracy specific legal questions
    """
    
    def __init__(self):
        super().__init__(
            agent_id="local_rag_001",
            name="Local RAG Specialist",
            description="Expert in specific provision retrieval and exact legal text queries"
        )
        self.specialization_areas = [
            "specific_provisions", 
            "article_lookup", 
            "exact_citations",
            "legal_definitions",
            "penalty_clauses"
        ]
        self.query_patterns = {
            'article_pattern': r'article\s+(\d+)',
            'section_pattern': r'section\s+(\d+)',
            'clause_pattern': r'clause\s+(\d+)',
            'paragraph_pattern': r'paragraph\s+(\d+)'
        }
        
    async def initialize(self) -> bool:
        """Initialize the Local RAG agent."""
        try:
            # Test the local RAG functionality
            test_result = local_rag_query("test query")
            
            logger.info("Local RAG agent initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Local RAG agent: {e}")
            return False
    
    def get_capabilities(self) -> List[AgentCapability]:
        """Define Local RAG agent capabilities."""
        return [
            AgentCapability(
                name="local_rag_query",
                description="Retrieve specific legal provisions using local vector similarity search",
                input_schema={
                    "query": {"type": "string", "description": "Specific legal question"},
                    "max_results": {"type": "integer", "description": "Maximum results to return", "default": 5},
                    "similarity_threshold": {"type": "number", "description": "Minimum similarity score", "default": 0.7}
                },
                output_schema={
                    "response": {"type": "string", "description": "Retrieved legal text and analysis"},
                    "sources": {"type": "array", "description": "Source provisions with citations"},
                    "confidence": {"type": "number", "description": "Retrieval confidence score"},
                    "matched_entities": {"type": "array", "description": "Legal entities found"}
                },
                confidence_threshold=0.8,
                performance_metrics={
                    "avg_response_time": 0.0,
                    "accuracy_score": 0.0,
                    "total_queries": 0
                }
            ),
            AgentCapability(
                name="article_extraction",
                description="Extract and analyze specific articles from legal documents",
                input_schema={
                    "article_number": {"type": "string", "description": "Article number to retrieve"},
                    "document_type": {"type": "string", "description": "Type of legal document"}
                },
                output_schema={
                    "article_text": {"type": "string", "description": "Complete article text"},
                    "cross_references": {"type": "array", "description": "Related articles"},
                    "amendments": {"type": "array", "description": "Article amendments"}
                },
                confidence_threshold=0.9
            ),
            AgentCapability(
                name="penalty_analysis",
                description="Analyze penalty clauses and legal consequences",
                input_schema={
                    "violation_type": {"type": "string", "description": "Type of legal violation"},
                    "jurisdiction": {"type": "string", "description": "Legal jurisdiction"}
                },
                output_schema={
                    "penalties": {"type": "array", "description": "Applicable penalties"},
                    "severity": {"type": "string", "description": "Penalty severity level"},
                    "legal_basis": {"type": "array", "description": "Legal provisions supporting penalties"}
                },
                confidence_threshold=0.85
            )
        ]
    
    async def process_request(self, request: AgentMessage) -> AgentMessage:
        """Process incoming requests for Local RAG operations."""
        try:
            content = request.content
            task = content.get('task', {})
            task_type = task.get('type', '')
            
            if task_type == 'local_rag_query':
                result = await self._handle_local_rag_query(task)
            elif task_type == 'article_extraction':
                result = await self._handle_article_extraction(task)
            elif task_type == 'penalty_analysis':
                result = await self._handle_penalty_analysis(task)
            else:
                return self._create_error_response(request, f"Unsupported task type: {task_type}")
            
            return AgentMessage(
                type=MessageType.TASK_RESULT,
                sender_id=self.agent_id,
                recipient_id=request.sender_id,
                correlation_id=request.id,
                content={
                    'task_id': task.get('id'),
                    'result': result,
                    'status': 'completed',
                    'agent_id': self.agent_id,
                    'processing_time': result.get('processing_time', 0.0)
                }
            )
            
        except Exception as e:
            logger.error(f"Error processing Local RAG request: {e}")
            return self._create_error_response(request, str(e))
    
    async def _handle_local_rag_query(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle local RAG query with enhanced analysis."""
        start_time = datetime.now()
        
        query = task.get('query', '')
        max_results = task.get('max_results', 5)
        
        try:
            # Enhanced query preprocessing
            processed_query = await self._preprocess_query(query)
            
            # Execute local RAG query - this returns a dictionary
            rag_result = await asyncio.to_thread(local_rag_query, processed_query)
            
            # Check for errors in the RAG result
            if isinstance(rag_result, dict) and 'error' in rag_result:
                return {
                    'response': f"Local RAG query failed: {rag_result['error']}",
                    'sources': [],
                    'confidence': 0.0,
                    'error': True,
                    'processing_time': (datetime.now() - start_time).total_seconds()
                }
            
            # Generate response from RAG result
            response_text = await self._generate_response_from_rag_result(query, rag_result)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Extract sources and confidence
            sources = self._extract_sources_from_dict(rag_result, max_results)
            confidence = self._calculate_confidence(query, rag_result, sources)
            
            # Update performance metrics
            self._update_performance_metrics(processing_time, confidence)
            
            return {
                'response': response_text,
                'sources': sources,
                'confidence': confidence,
                'matched_entities': self._extract_legal_entities(query),
                'processing_time': processing_time,
                'query_type': 'local_rag',
                'specialization_applied': self._get_applied_specialization(query)
            }
            
        except Exception as e:
            logger.error(f"Local RAG query failed: {e}")
            return {
                'response': f"Local RAG query failed: {str(e)}",
                'sources': [],
                'confidence': 0.0,
                'error': True,
                'processing_time': (datetime.now() - start_time).total_seconds()
            }
    
    async def _process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process tasks for Local RAG agent."""
        task_type = task.get('type', '')
        
        try:
            if task_type == 'local_rag_query':
                result = await self._handle_local_rag_query(task)
                return result
            elif task_type == 'article_extraction':
                result = await self._handle_article_extraction(task)
                return result
            elif task_type == 'penalty_analysis':
                result = await self._handle_penalty_analysis(task)
                return result
            else:
                return {
                    'response': f"Unknown task type: {task_type}",
                    'sources': [],
                    'confidence': 0.0,
                    'error': True
                }
        except Exception as e:
            logger.error(f"Task processing failed: {e}")
            return {
                'response': f"Task processing failed: {str(e)}",
                'sources': [],
                'confidence': 0.0,
                'error': True
            }

    async def _preprocess_query(self, query: str) -> str:
        """Preprocess query to optimize for local RAG retrieval."""
        # Convert to lowercase for pattern matching
        query_lower = query.lower()
        
        # Enhance queries with specific legal patterns
        enhancements = []
        
        # Check for article references
        import re
        for pattern_name, pattern in self.query_patterns.items():
            matches = re.findall(pattern, query_lower)
            if matches:
                enhancements.append(f"Focus on {pattern_name.replace('_', ' ')} {matches[0]}")
        
        # Add context for better retrieval
        if 'penalty' in query_lower or 'fine' in query_lower:
            enhancements.append("penalty clauses and legal consequences")
        
        if 'definition' in query_lower or 'what is' in query_lower:
            enhancements.append("legal definitions and explanations")
        
        # Combine original query with enhancements
        if enhancements:
            enhanced_query = f"{query}. Additional context: {'; '.join(enhancements)}"
            return enhanced_query
        
        return query
    
    async def _generate_response_from_rag_result(self, query: str, rag_result: Dict[str, Any]) -> str:
        """Generate a comprehensive response from the RAG result dictionary."""
        try:
            response_parts = []
            
            # Add main provision information
            if 'provision' in rag_result:
                provision = rag_result['provision']
                if provision:
                    response_parts.append("**Primary Legal Provision:**")
                    if 'title' in provision and provision['title']:
                        response_parts.append(f"Title: {provision['title']}")
                    if 'content' in provision and provision['content']:
                        content = provision['content'][:500] + "..." if len(provision['content']) > 500 else provision['content']
                        response_parts.append(f"Content: {content}")
            
            # Add semantic seeds for context
            if 'semantic_seeds' in rag_result and rag_result['semantic_seeds']:
                response_parts.append("\\n**Related Legal Context:**")
                for i, seed in enumerate(rag_result['semantic_seeds'][:3], 1):
                    if 'provision' in seed:
                        seed_provision = seed['provision']
                        title = seed_provision.get('title', f'Related Provision {i}')
                        content = seed_provision.get('content', '')[:200] + "..." if len(seed_provision.get('content', '')) > 200 else seed_provision.get('content', '')
                        response_parts.append(f"{i}. {title}: {content}")
            
            # Add neighbors information
            if 'neighbors' in rag_result and rag_result['neighbors']:
                neighbors_count = len(rag_result['neighbors'])
                response_parts.append(f"\\n**Connected Legal Elements:** {neighbors_count} related provisions found")
            
            # Add amendments information
            if 'amendments' in rag_result and rag_result['amendments']:
                amendments_count = len(rag_result['amendments'])
                response_parts.append(f"\\n**Legal Evolution:** {amendments_count} amendments or updates identified")
            
            # Add query-specific analysis
            query_lower = query.lower()
            if any(term in query_lower for term in ['liability', 'responsible', 'accountable']):
                response_parts.append("\\n**Liability Analysis:**")
                response_parts.append("The above provisions outline the legal framework for determining liability and responsibility in the specified context.")
            
            if any(term in query_lower for term in ['commercial', 'company', 'business']):
                response_parts.append("\\n**Commercial Law Application:**")
                response_parts.append("These provisions apply specifically to commercial entities and business operations under UAE law.")
            
            if any(term in query_lower for term in ['court', 'interpret', 'judicial']):
                response_parts.append("\\n**Judicial Interpretation:**")
                response_parts.append("Courts typically interpret these provisions based on established legal precedents and the specific circumstances of each case.")
            
            # Combine all parts
            if response_parts:
                return "\\n".join(response_parts)
            else:
                return "No specific legal provisions found for your query. Please try rephrasing your question or using more specific legal terms."
            
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            return f"Error generating response: {str(e)}"

    def _extract_sources_from_dict(self, rag_result: Dict[str, Any], max_results: int = 5) -> List[Dict[str, Any]]:
        """Extract sources from the RAG result dictionary."""
        sources = []
        
        try:
            # Extract primary provision as a source
            if 'provision' in rag_result and rag_result['provision']:
                provision = rag_result['provision']
                sources.append({
                    'title': provision.get('title', 'Legal Provision'),
                    'content': provision.get('content', 'No content available')[:300] + "..." if len(provision.get('content', '')) > 300 else provision.get('content', ''),
                    'source_agent': 'Local RAG',
                    'confidence': 0.9,
                    'type': 'Primary Provision'
                })
            
            # Extract semantic seeds as sources
            if 'semantic_seeds' in rag_result:
                for i, seed in enumerate(rag_result['semantic_seeds'][:max_results-1]):
                    if 'provision' in seed:
                        seed_provision = seed['provision']
                        sources.append({
                            'title': seed_provision.get('title', f'Related Provision {i+1}'),
                            'content': seed_provision.get('content', 'No content available')[:300] + "..." if len(seed_provision.get('content', '')) > 300 else seed_provision.get('content', ''),
                            'source_agent': 'Local RAG',
                            'confidence': seed.get('similarity', 0.7),
                            'type': 'Semantic Match'
                        })
            
            return sources[:max_results]
            
        except Exception as e:
            logger.error(f"Source extraction failed: {e}")
            return []

    async def _enhance_local_result(self, original_query: str, rag_result: str) -> str:
        """Enhance the local RAG result with specialized analysis."""
        try:
            # Add specialized insights based on query type
            query_lower = original_query.lower()
            
            enhancements = []
            
            # Add article-specific analysis
            if any(term in query_lower for term in ['article', 'section', 'clause']):
                enhancements.append("**Specific Provision Analysis:**")
                enhancements.append("This query targets specific legal provisions requiring exact text retrieval.")
            
            # Add penalty analysis
            if any(term in query_lower for term in ['penalty', 'fine', 'punishment', 'consequence']):
                enhancements.append("**Penalty Assessment:**")
                enhancements.append("Legal consequences and penalty structures are analyzed below.")
            
            # Add cross-reference suggestions
            if rag_result and len(rag_result) > 100:
                enhancements.append("**Related Provisions:**")
                enhancements.append("Consider reviewing related articles for comprehensive understanding.")
            
            # Combine original result with enhancements
            if enhancements:
                enhanced_result = f"{rag_result}\\n\\n{chr(10).join(enhancements)}"
                return enhanced_result
            
            return rag_result
            
        except Exception as e:
            logger.error(f"Result enhancement failed: {e}")
            return rag_result
    
    async def _handle_article_extraction(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle specific article extraction requests."""
        article_number = task.get('article_number', '')
        document_type = task.get('document_type', 'UAE Constitution')
        
        try:
            # Construct targeted query for article extraction
            query = f"Article {article_number} {document_type} complete text provisions"
            
            # Use local RAG for retrieval
            result = await asyncio.to_thread(local_rag_query, query)
            
            return {
                'article_text': result,
                'article_number': article_number,
                'document_type': document_type,
                'cross_references': self._find_cross_references(result),
                'confidence': 0.9 if result else 0.1
            }
            
        except Exception as e:
            return {
                'article_text': f"Error retrieving Article {article_number}: {str(e)}",
                'error': True
            }
    
    async def _handle_penalty_analysis(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle penalty analysis requests."""
        violation_type = task.get('violation_type', '')
        jurisdiction = task.get('jurisdiction', 'UAE')
        
        try:
            # Construct penalty-focused query
            query = f"penalties fines consequences {violation_type} {jurisdiction} legal punishment"
            
            # Use local RAG for penalty retrieval
            result = await asyncio.to_thread(local_rag_query, query)
            
            # Analyze penalty severity
            severity = self._assess_penalty_severity(result)
            
            return {
                'penalties': self._extract_penalties(result),
                'severity': severity,
                'legal_basis': self._extract_legal_basis(result),
                'violation_type': violation_type,
                'jurisdiction': jurisdiction,
                'confidence': 0.8 if result else 0.2
            }
            
        except Exception as e:
            return {
                'penalties': [f"Error analyzing penalties for {violation_type}: {str(e)}"],
                'error': True
            }
    
    def _extract_sources(self, rag_result: str, max_results: int) -> List[Dict[str, Any]]:
        """Extract source information from RAG result."""
        sources = []
        
        try:
            # Simple extraction - in a real implementation, this would be more sophisticated
            if rag_result:
                # Extract potential article references
                import re
                article_matches = re.findall(r'Article\s+(\d+)', rag_result, re.IGNORECASE)
                
                for i, article_num in enumerate(article_matches[:max_results]):
                    sources.append({
                        'title': f"Article {article_num}",
                        'content': f"Legal provision from Article {article_num}",
                        'type': 'legal_article',
                        'confidence': 0.9 - (i * 0.1),  # Decrease confidence for later matches
                        'source_agent': 'local_rag'
                    })
                
                # If no specific articles found, create generic source
                if not sources:
                    sources.append({
                        'title': 'UAE Legal Provisions',
                        'content': rag_result[:200] + "..." if len(rag_result) > 200 else rag_result,
                        'type': 'legal_text',
                        'confidence': 0.7,
                        'source_agent': 'local_rag'
                    })
        
        except Exception as e:
            logger.error(f"Source extraction failed: {e}")
        
        return sources[:max_results]
    
    def _calculate_confidence(self, query: str, rag_result: Any, sources: List[Dict]) -> float:
        """Calculate confidence score for the local RAG result."""
        base_confidence = 0.5
        
        # Handle both string and dictionary rag_result
        has_meaningful_result = False
        if isinstance(rag_result, dict):
            # Check if we have provision data
            if 'provision' in rag_result and rag_result['provision']:
                has_meaningful_result = True
                base_confidence += 0.2
            # Check semantic seeds
            if 'semantic_seeds' in rag_result and rag_result['semantic_seeds']:
                base_confidence += 0.1 * min(len(rag_result['semantic_seeds']), 3)
        elif isinstance(rag_result, str) and len(rag_result) > 50:
            has_meaningful_result = True
            base_confidence += 0.2
        
        # Boost confidence if we found specific legal entities
        legal_entities = self._extract_legal_entities(query)
        if legal_entities:
            base_confidence += 0.1 * len(legal_entities)
        
        # Boost confidence based on sources
        if sources:
            avg_source_confidence = sum(s.get('confidence', 0.5) for s in sources) / len(sources)
            base_confidence += (avg_source_confidence * 0.2)
        
        # Boost confidence for this agent's specialization areas
        query_lower = query.lower()
        if any(spec in query_lower for spec in ['article', 'section', 'penalty', 'specific']):
            base_confidence += 0.1
        
        return min(base_confidence, 1.0)
    
    def _extract_legal_entities(self, query: str) -> List[str]:
        """Extract legal entities from the query."""
        entities = []
        query_lower = query.lower()
        
        import re
        
        # Extract article numbers
        articles = re.findall(r'article\s+(\d+)', query_lower)
        entities.extend([f"Article {num}" for num in articles])
        
        # Extract law numbers
        laws = re.findall(r'law\s+(?:no\.?\s*)?(\d+)', query_lower)
        entities.extend([f"Law {num}" for num in laws])
        
        # Extract section numbers
        sections = re.findall(r'section\s+(\d+)', query_lower)
        entities.extend([f"Section {num}" for num in sections])
        
        return entities
    
    def _get_applied_specialization(self, query: str) -> List[str]:
        """Determine which specializations were applied."""
        applied = []
        query_lower = query.lower()
        
        if any(term in query_lower for term in ['article', 'section', 'clause']):
            applied.append('specific_provisions')
        
        if 'penalty' in query_lower or 'fine' in query_lower:
            applied.append('penalty_clauses')
        
        if 'definition' in query_lower or 'what is' in query_lower:
            applied.append('legal_definitions')
        
        if not applied:
            applied.append('general_local_rag')
        
        return applied
    
    def _find_cross_references(self, text: str) -> List[str]:
        """Find cross-references in legal text."""
        cross_refs = []
        
        import re
        # Find references to other articles
        refs = re.findall(r'(?:see|refer to|pursuant to|according to).*?Article\s+(\d+)', text, re.IGNORECASE)
        cross_refs.extend([f"Article {ref}" for ref in refs])
        
        return list(set(cross_refs))  # Remove duplicates
    
    def _assess_penalty_severity(self, penalty_text: str) -> str:
        """Assess the severity of penalties mentioned in text."""
        text_lower = penalty_text.lower()
        
        if any(term in text_lower for term in ['imprisonment', 'jail', 'prison', 'detention']):
            return 'severe'
        elif any(term in text_lower for term in ['fine', 'monetary', 'payment']):
            return 'moderate'
        elif any(term in text_lower for term in ['warning', 'caution', 'notice']):
            return 'minor'
        else:
            return 'unspecified'
    
    def _extract_penalties(self, penalty_text: str) -> List[str]:
        """Extract specific penalties from text."""
        penalties = []
        
        import re
        # Extract monetary penalties
        monetary = re.findall(r'fine[s]?.*?(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:AED|dirham)', penalty_text, re.IGNORECASE)
        penalties.extend([f"Fine of {amount} AED" for amount in monetary])
        
        # Extract imprisonment terms
        imprisonment = re.findall(r'imprisonment.*?(\d+)\s*(?:year|month|day)', penalty_text, re.IGNORECASE)
        penalties.extend([f"Imprisonment of {term}" for term in imprisonment])
        
        if not penalties:
            penalties.append("Penalties as specified in applicable law")
        
        return penalties
    
    def _extract_legal_basis(self, penalty_text: str) -> List[str]:
        """Extract legal basis for penalties."""
        basis = []
        
        import re
        # Extract article references
        articles = re.findall(r'Article\s+(\d+)', penalty_text, re.IGNORECASE)
        basis.extend([f"Article {num}" for num in articles])
        
        if not basis:
            basis.append("UAE Legal Framework")
        
        return basis
    
    def _update_performance_metrics(self, processing_time: float, confidence: float):
        """Update agent performance metrics."""
        # Update the first capability's performance metrics
        if self.capabilities:
            cap = self.capabilities[0]
            cap.performance_metrics['total_queries'] = cap.performance_metrics.get('total_queries', 0) + 1
            
            # Update running averages
            total = cap.performance_metrics['total_queries']
            old_avg_time = cap.performance_metrics.get('avg_response_time', 0.0)
            cap.performance_metrics['avg_response_time'] = ((old_avg_time * (total - 1)) + processing_time) / total
            
            old_avg_accuracy = cap.performance_metrics.get('accuracy_score', 0.0)
            cap.performance_metrics['accuracy_score'] = ((old_avg_accuracy * (total - 1)) + confidence) / total
    
    def get_specialization_report(self) -> Dict[str, Any]:
        """Get detailed report on Local RAG specialization performance."""
        return {
            'agent_id': self.agent_id,
            'specialization_areas': self.specialization_areas,
            'capabilities': [cap.name for cap in self.get_capabilities()],
            'performance_metrics': self.performance_metrics,
            'query_patterns_supported': list(self.query_patterns.keys()),
            'optimization_status': 'active'
        }
