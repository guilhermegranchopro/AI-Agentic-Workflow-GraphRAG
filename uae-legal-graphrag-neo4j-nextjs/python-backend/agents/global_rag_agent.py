"""Global RAG Agent - Specialized agent for conceptual understanding and broad queries.

This agent excels at:
- Broad legal concepts and principles
- Comparative legal analysis
- Legal framework overviews
- Conceptual understanding and definitions
- Cross-domain legal relationships
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

from .base import BaseAgent, AgentMessage, AgentCapability, MessageType
from src.graph.tools import global_rag_query

logger = logging.getLogger(__name__)


class GlobalRAGAgent(BaseAgent):
    """
    Specialized agent for Global RAG queries focusing on:
    - Broad legal concepts and principles
    - Legal framework understanding
    - Comparative analysis across legal domains
    - Conceptual questions and definitions
    - Legal system overviews
    """
    
    def __init__(self):
        super().__init__(
            agent_id="global_rag_001",
            name="Global RAG Specialist",
            description="Expert in conceptual understanding and broad legal framework analysis"
        )
        self.specialization_areas = [
            "legal_concepts",
            "framework_analysis", 
            "comparative_law",
            "legal_principles",
            "system_overviews",
            "cross_domain_analysis"
        ]
        self.concept_categories = {
            'constitutional': ['constitution', 'fundamental rights', 'government structure'],
            'civil': ['contracts', 'obligations', 'property rights', 'liability'],
            'commercial': ['business law', 'corporate governance', 'commercial transactions'],
            'criminal': ['criminal procedure', 'criminal offenses', 'criminal justice'],
            'administrative': ['public administration', 'regulatory framework', 'government agencies']
        }
        
    async def initialize(self) -> bool:
        """Initialize the Global RAG agent."""
        try:
            # Test the global RAG functionality
            test_result = global_rag_query("test conceptual query")
            
            logger.info("Global RAG agent initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Global RAG agent: {e}")
            return False
    
    def get_capabilities(self) -> List[AgentCapability]:
        """Define Global RAG agent capabilities."""
        return [
            AgentCapability(
                name="global_rag_query",
                description="Analyze broad legal concepts using global knowledge synthesis",
                input_schema={
                    "query": {"type": "string", "description": "Conceptual legal question"},
                    "scope": {"type": "string", "description": "Analysis scope", "default": "comprehensive"},
                    "include_comparisons": {"type": "boolean", "description": "Include comparative analysis", "default": False}
                },
                output_schema={
                    "response": {"type": "string", "description": "Comprehensive conceptual analysis"},
                    "concepts": {"type": "array", "description": "Related legal concepts"},
                    "frameworks": {"type": "array", "description": "Applicable legal frameworks"},
                    "confidence": {"type": "number", "description": "Analysis confidence score"}
                },
                confidence_threshold=0.75,
                performance_metrics={
                    "conceptual_accuracy": 0.0,
                    "framework_coverage": 0.0,
                    "synthesis_quality": 0.0
                }
            ),
            AgentCapability(
                name="framework_analysis",
                description="Analyze legal frameworks and their relationships",
                input_schema={
                    "domain": {"type": "string", "description": "Legal domain to analyze"},
                    "depth": {"type": "string", "description": "Analysis depth", "enum": ["overview", "detailed", "comprehensive"]}
                },
                output_schema={
                    "framework_structure": {"type": "object", "description": "Framework organization"},
                    "key_principles": {"type": "array", "description": "Fundamental principles"},
                    "relationships": {"type": "array", "description": "Inter-framework relationships"}
                },
                confidence_threshold=0.8
            ),
            AgentCapability(
                name="comparative_analysis",
                description="Compare legal concepts across different domains or jurisdictions",
                input_schema={
                    "concepts": {"type": "array", "description": "Concepts to compare"},
                    "comparison_criteria": {"type": "array", "description": "Criteria for comparison"}
                },
                output_schema={
                    "similarities": {"type": "array", "description": "Common elements"},
                    "differences": {"type": "array", "description": "Distinct characteristics"},
                    "analysis_summary": {"type": "string", "description": "Comparative analysis summary"}
                },
                confidence_threshold=0.7
            ),
            AgentCapability(
                name="concept_synthesis",
                description="Synthesize complex legal concepts from multiple sources",
                input_schema={
                    "topic": {"type": "string", "description": "Legal topic for synthesis"},
                    "sources": {"type": "array", "description": "Source materials for synthesis"}
                },
                output_schema={
                    "synthesized_concept": {"type": "string", "description": "Unified concept explanation"},
                    "source_integration": {"type": "object", "description": "How sources were integrated"},
                    "confidence_factors": {"type": "array", "description": "Factors affecting confidence"}
                },
                confidence_threshold=0.8
            )
        ]
    
    async def _process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process tasks for Global RAG agent."""
        task_type = task.get('type', '')
        
        try:
            if task_type == 'global_rag_query':
                result = await self._handle_global_rag_query(task)
                return result
            elif task_type == 'framework_analysis':
                result = await self._handle_framework_analysis(task)
                return result
            elif task_type == 'comparative_analysis':
                result = await self._handle_comparative_analysis(task)
                return result
            elif task_type == 'concept_synthesis':
                result = await self._handle_concept_synthesis(task)
                return result
            else:
                return {
                    'response': f"Unknown task type: {task_type}",
                    'sources': [],
                    'confidence': 0.0,
                    'error': True
                }
        except Exception as e:
            logger.error(f"Global RAG task processing failed: {e}")
            return {
                'response': f"Task processing failed: {str(e)}",
                'sources': [],
                'confidence': 0.0,
                'error': True
            }

    async def process_request(self, request: AgentMessage) -> AgentMessage:
        """Process incoming requests for Global RAG operations."""
        try:
            content = request.content
            task = content.get('task', {})
            task_type = task.get('type', '')
            
            if task_type == 'global_rag_query':
                result = await self._handle_global_rag_query(task)
            elif task_type == 'framework_analysis':
                result = await self._handle_framework_analysis(task)
            elif task_type == 'comparative_analysis':
                result = await self._handle_comparative_analysis(task)
            elif task_type == 'concept_synthesis':
                result = await self._handle_concept_synthesis(task)
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
            logger.error(f"Error processing Global RAG request: {e}")
            return self._create_error_response(request, str(e))
    
    async def _handle_global_rag_query(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle global RAG query with conceptual enhancement."""
        start_time = datetime.now()
        
        query = task.get('query', '')
        scope = task.get('scope', 'comprehensive')
        include_comparisons = task.get('include_comparisons', False)
        
        try:
            # Enhance query for conceptual understanding
            enhanced_query = await self._enhance_conceptual_query(query, scope)
            
            # Execute global RAG query - this returns a dictionary
            rag_result = await asyncio.to_thread(global_rag_query, enhanced_query)
            
            # Check for errors in the RAG result
            if isinstance(rag_result, dict) and 'error' in rag_result:
                return {
                    'response': f"Global RAG query failed: {rag_result['error']}",
                    'sources': [],
                    'confidence': 0.0,
                    'error': True,
                    'processing_time': (datetime.now() - start_time).total_seconds()
                }
            
            # Generate response from RAG result dictionary
            response_text = await self._generate_response_from_global_rag_result(query, rag_result)
            
            # Extract sources and confidence
            sources = self._extract_sources_from_global_result(rag_result)
            confidence = self._calculate_global_confidence(query, rag_result, sources)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Update performance metrics
            concept_count = len(rag_result.get('semantic_results', []))
            framework_count = len(rag_result.get('community_analysis', []))
            self._update_performance_metrics(processing_time, confidence, concept_count, framework_count)
            
            return {
                'response': response_text,
                'sources': sources,
                'confidence': confidence,
                'conceptual_framework': self._extract_conceptual_framework(rag_result),
                'processing_time': processing_time,
                'query_type': 'global_rag',
                'scope': scope
            }
            
        except Exception as e:
            logger.error(f"Global RAG query failed: {e}")
            return {
                'response': f"Global RAG query failed: {str(e)}",
                'sources': [],
                'confidence': 0.0,
                'error': True,
                'processing_time': (datetime.now() - start_time).total_seconds()
            }
            
            # Add comparative analysis if requested
            if include_comparisons:
                comparative_insights = await self._add_comparative_insights(query, rag_result)
                conceptual_analysis['comparative_insights'] = comparative_insights
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Extract concepts and frameworks
            concepts = self._extract_legal_concepts(query, rag_result)
            frameworks = self._identify_legal_frameworks(query, rag_result)
            confidence = self._calculate_conceptual_confidence(query, rag_result, concepts)
            
            # Update performance metrics
            self._update_performance_metrics(processing_time, confidence, len(concepts), len(frameworks))
            
            return {
                'response': conceptual_analysis['enhanced_response'],
                'concepts': concepts,
                'frameworks': frameworks,
                'confidence': confidence,
                'conceptual_depth': conceptual_analysis['depth_score'],
                'processing_time': processing_time,
                'query_type': 'global_rag',
                'analysis_scope': scope,
                'specialization_applied': self._get_applied_specialization(query)
            }
            
        except Exception as e:
            logger.error(f"Global RAG query failed: {e}")
            return {
                'response': f"Global RAG query failed: {str(e)}",
                'concepts': [],
                'frameworks': [],
                'confidence': 0.0,
                'error': True,
                'processing_time': (datetime.now() - start_time).total_seconds()
            }
    
    async def _generate_response_from_global_rag_result(self, query: str, rag_result: Dict[str, Any]) -> str:
        """Generate a comprehensive response from the Global RAG result dictionary."""
        try:
            response_parts = []
            
            # Add conceptual overview
            response_parts.append("**Legal Framework Overview:**")
            
            # Add semantic results context
            if 'semantic_results' in rag_result and rag_result['semantic_results']:
                response_parts.append("\\n**Relevant Legal Provisions:**")
                for i, result in enumerate(rag_result['semantic_results'][:3], 1):
                    if 'provision' in result:
                        provision = result['provision']
                        title = provision.get('title', f'Legal Provision {i}')
                        content = provision.get('content', '')[:300] + "..." if len(provision.get('content', '')) > 300 else provision.get('content', '')
                        response_parts.append(f"{i}. {title}: {content}")
            
            # Add community analysis
            if 'community_analysis' in rag_result and rag_result['community_analysis']:
                response_parts.append("\\n**Cross-Domain Legal Analysis:**")
                for i, community in enumerate(rag_result['community_analysis'][:3], 1):
                    community_id = community.get('community_id', f'Domain {i}')
                    summary = community.get('summary', 'Legal domain analysis')
                    size = community.get('size', 0)
                    response_parts.append(f"**Domain {i}** ({size} interconnected provisions): {summary}")
                    
                    # Add provisions from this community
                    provisions = community.get('relevant_provisions', [])
                    for j, provision in enumerate(provisions[:2]):
                        title = provision.get('title', 'Legal Provision')
                        content = provision.get('content', 'No content available')[:200] + "..." if len(provision.get('content', '')) > 200 else provision.get('content', '')
                        response_parts.append(f"  - {title}: {content}")
            
            # Add cross-community patterns
            if 'cross_community_patterns' in rag_result and rag_result['cross_community_patterns']:
                response_parts.append("\\n**Cross-Domain Implications:**")
                for pattern in rag_result['cross_community_patterns']:
                    response_parts.append(f"• {pattern}")
            
            # Add query-specific conceptual analysis
            query_lower = query.lower()
            if any(term in query_lower for term in ['constitutional', 'constitution']):
                response_parts.append("\\n**Constitutional Framework Analysis:**")
                response_parts.append("Constitutional law establishes the fundamental legal principles and governmental structure. The provisions above represent key constitutional concepts that form the foundation of the legal system.")
            
            if any(term in query_lower for term in ['principle', 'concept', 'framework']):
                response_parts.append("\\n**Conceptual Analysis:**")
                response_parts.append("The legal concepts identified demonstrate the interconnected nature of legal principles across different domains of law.")
            
            if any(term in query_lower for term in ['rights', 'duties', 'obligations']):
                response_parts.append("\\n**Rights and Obligations Framework:**")
                response_parts.append("The legal framework establishes a comprehensive system of rights and corresponding obligations across multiple legal domains.")
            
            # Combine all parts
            if response_parts:
                return "\\n".join(response_parts)
            else:
                return "No comprehensive legal framework found for your query. Please try expanding your search terms or using more general legal concepts."
            
        except Exception as e:
            logger.error(f"Global response generation failed: {e}")
            return f"Error generating response: {str(e)}"

    def _extract_sources_from_global_result(self, rag_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract sources from the Global RAG result dictionary."""
        sources = []
        
        try:
            # Extract semantic results as sources
            if 'semantic_results' in rag_result:
                for i, result in enumerate(rag_result['semantic_results'][:3]):
                    if 'provision' in result:
                        provision = result['provision']
                        sources.append({
                            'title': provision.get('title', f'Legal Framework {i+1}'),
                            'content': provision.get('content', 'No content available')[:300] + "..." if len(provision.get('content', '')) > 300 else provision.get('content', ''),
                            'source_agent': 'Global RAG',
                            'confidence': result.get('similarity', 0.8),
                            'type': 'Conceptual Framework'
                        })
            
            # Extract community provisions as sources
            if 'community_analysis' in rag_result:
                for community in rag_result['community_analysis'][:2]:
                    provisions = community.get('relevant_provisions', [])
                    for provision in provisions[:1]:  # One per community
                        sources.append({
                            'title': provision.get('title', 'Cross-Domain Provision'),
                            'content': provision.get('content', 'No content available')[:300] + "..." if len(provision.get('content', '')) > 300 else provision.get('content', ''),
                            'source_agent': 'Global RAG',
                            'confidence': 0.7,
                            'type': 'Cross-Domain Analysis'
                        })
            
            return sources[:5]  # Limit to 5 sources
            
        except Exception as e:
            logger.error(f"Global source extraction failed: {e}")
            return []

    def _calculate_global_confidence(self, query: str, rag_result: Dict[str, Any], sources: List[Dict]) -> float:
        """Calculate confidence score for Global RAG results."""
        base_confidence = 0.6  # Higher base for global conceptual queries
        
        # Check if we have meaningful community analysis
        if 'community_analysis' in rag_result and rag_result['community_analysis']:
            communities_count = len(rag_result['community_analysis'])
            base_confidence += 0.1 * min(communities_count, 3)
        
        # Check semantic results quality
        if 'semantic_results' in rag_result and rag_result['semantic_results']:
            base_confidence += 0.15
        
        # Boost for cross-community patterns
        if 'cross_community_patterns' in rag_result and rag_result['cross_community_patterns']:
            base_confidence += 0.1
        
        # Boost for global/conceptual query terms
        query_lower = query.lower()
        if any(term in query_lower for term in ['concept', 'principle', 'framework', 'constitutional', 'general']):
            base_confidence += 0.1
        
        # Source quality boost
        if sources:
            avg_source_confidence = sum(s.get('confidence', 0.7) for s in sources) / len(sources)
            base_confidence += (avg_source_confidence * 0.15)
        
        return min(base_confidence, 1.0)

    def _extract_conceptual_framework(self, rag_result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract conceptual framework information from the result."""
        try:
            framework = {
                'domains_analyzed': len(rag_result.get('community_analysis', [])),
                'cross_domain_patterns': rag_result.get('cross_community_patterns', []),
                'semantic_matches': len(rag_result.get('semantic_results', [])),
                'framework_type': 'comprehensive' if len(rag_result.get('community_analysis', [])) > 1 else 'focused'
            }
            return framework
        except:
            return {'framework_type': 'basic'}

    async def _enhance_conceptual_query(self, query: str, scope: str) -> str:
        """Enhance query for better conceptual understanding."""
        query_lower = query.lower()
        
        # Identify query category
        category = self._identify_legal_category(query_lower)
        
        # Add conceptual context
        enhancements = []
        
        if 'definition' in query_lower or 'what is' in query_lower:
            enhancements.append("provide comprehensive legal definition and conceptual framework")
        
        if 'compare' in query_lower or 'difference' in query_lower:
            enhancements.append("include comparative analysis and distinguishing features")
        
        if 'principle' in query_lower or 'concept' in query_lower:
            enhancements.append("explain underlying legal principles and theoretical foundations")
        
        if scope == 'comprehensive':
            enhancements.append("provide broad context and related legal frameworks")
        
        # Add category-specific enhancements
        if category and category in self.concept_categories:
            related_concepts = self.concept_categories[category]
            enhancements.append(f"consider related {category} law concepts: {', '.join(related_concepts[:3])}")
        
        # Combine original query with enhancements
        if enhancements:
            enhanced_query = f"{query}. Analysis requirements: {'; '.join(enhancements)}"
            return enhanced_query
        
        return query
    
    async def _perform_conceptual_analysis(self, original_query: str, rag_result: str) -> Dict[str, Any]:
        """Perform deep conceptual analysis of the RAG result."""
        try:
            # Analyze conceptual depth
            depth_indicators = [
                'principle', 'concept', 'framework', 'theory', 'doctrine',
                'interpretation', 'application', 'scope', 'purpose', 'rationale'
            ]
            
            depth_score = sum(1 for indicator in depth_indicators if indicator in rag_result.lower()) / len(depth_indicators)
            
            # Enhance the response with conceptual insights
            query_lower = original_query.lower()
            enhancements = []
            
            # Add conceptual framework explanation
            if any(term in query_lower for term in ['what is', 'define', 'explain']):
                enhancements.append("**Conceptual Framework:**")
                enhancements.append("This concept operates within the broader UAE legal system framework.")
            
            # Add principle analysis
            if 'principle' in query_lower or depth_score > 0.3:
                enhancements.append("**Underlying Principles:**")
                enhancements.append("The legal principles governing this area ensure consistency with UAE constitutional values.")
            
            # Add practical implications
            if len(rag_result) > 200:
                enhancements.append("**Practical Applications:**")
                enhancements.append("These legal concepts have practical implications for legal practice and compliance.")
            
            # Add interconnections
            if depth_score > 0.5:
                enhancements.append("**Legal Interconnections:**")
                enhancements.append("This area connects with other legal domains within the UAE legal system.")
            
            # Combine original result with conceptual enhancements
            if enhancements:
                enhanced_response = f"{rag_result}\\n\\n{chr(10).join(enhancements)}"
            else:
                enhanced_response = rag_result
            
            return {
                'enhanced_response': enhanced_response,
                'depth_score': depth_score,
                'conceptual_indicators': depth_indicators
            }
            
        except Exception as e:
            logger.error(f"Conceptual analysis failed: {e}")
            return {
                'enhanced_response': rag_result,
                'depth_score': 0.0,
                'error': str(e)
            }
    
    async def _add_comparative_insights(self, query: str, rag_result: str) -> Dict[str, Any]:
        """Add comparative analysis insights."""
        try:
            # Identify comparison opportunities
            query_lower = query.lower()
            
            comparative_insights = {
                'comparison_type': 'none',
                'insights': []
            }
            
            if 'compare' in query_lower or 'difference' in query_lower:
                comparative_insights['comparison_type'] = 'explicit'
                comparative_insights['insights'].append("Direct comparison requested by user")
            
            elif any(term in query_lower for term in ['versus', 'vs', 'between']):
                comparative_insights['comparison_type'] = 'implicit'
                comparative_insights['insights'].append("Comparative analysis inferred from query structure")
            
            else:
                # Look for opportunities for conceptual comparison
                category = self._identify_legal_category(query_lower)
                if category:
                    comparative_insights['comparison_type'] = 'conceptual'
                    comparative_insights['insights'].append(f"Comparison available with other {category} law concepts")
            
            return comparative_insights
            
        except Exception as e:
            logger.error(f"Comparative insights failed: {e}")
            return {'comparison_type': 'error', 'insights': []}
    
    async def _handle_framework_analysis(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle legal framework analysis requests."""
        domain = task.get('domain', 'general')
        depth = task.get('depth', 'overview')
        
        try:
            # Construct framework-focused query
            query = f"{domain} legal framework structure principles organization {depth} analysis"
            
            # Use global RAG for framework retrieval
            result = await asyncio.to_thread(global_rag_query, query)
            
            # Analyze framework structure
            framework_structure = self._analyze_framework_structure(result)
            key_principles = self._extract_key_principles(result)
            relationships = self._identify_framework_relationships(result, domain)
            
            return {
                'framework_structure': framework_structure,
                'key_principles': key_principles,
                'relationships': relationships,
                'domain': domain,
                'analysis_depth': depth,
                'confidence': 0.8 if result else 0.2
            }
            
        except Exception as e:
            return {
                'framework_structure': {'error': f"Framework analysis failed: {str(e)}"},
                'error': True
            }
    
    async def _handle_comparative_analysis(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle comparative analysis requests."""
        concepts = task.get('concepts', [])
        criteria = task.get('comparison_criteria', ['scope', 'application', 'enforcement'])
        
        try:
            # Construct comparative query
            concept_list = ', '.join(concepts)
            criteria_list = ', '.join(criteria)
            query = f"compare {concept_list} legal concepts differences similarities {criteria_list}"
            
            # Use global RAG for comparative analysis
            result = await asyncio.to_thread(global_rag_query, query)
            
            # Extract comparison elements
            similarities = self._extract_similarities(result, concepts)
            differences = self._extract_differences(result, concepts)
            
            return {
                'similarities': similarities,
                'differences': differences,
                'analysis_summary': f"Comparative analysis of {len(concepts)} legal concepts across {len(criteria)} criteria",
                'concepts_analyzed': concepts,
                'criteria_used': criteria,
                'confidence': 0.75 if result else 0.25
            }
            
        except Exception as e:
            return {
                'analysis_summary': f"Comparative analysis failed: {str(e)}",
                'error': True
            }
    
    async def _handle_concept_synthesis(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle concept synthesis requests."""
        topic = task.get('topic', '')
        sources = task.get('sources', [])
        
        try:
            # Construct synthesis query
            source_context = ', '.join(sources) if sources else 'multiple legal sources'
            query = f"synthesize {topic} legal concept from {source_context} unified explanation"
            
            # Use global RAG for synthesis
            result = await asyncio.to_thread(global_rag_query, query)
            
            # Analyze synthesis quality
            synthesis_analysis = self._analyze_synthesis_quality(result, topic, sources)
            
            return {
                'synthesized_concept': result,
                'source_integration': synthesis_analysis['integration_score'],
                'confidence_factors': synthesis_analysis['confidence_factors'],
                'topic': topic,
                'sources_used': len(sources),
                'confidence': synthesis_analysis['overall_confidence']
            }
            
        except Exception as e:
            return {
                'synthesized_concept': f"Concept synthesis failed: {str(e)}",
                'error': True
            }
    
    def _identify_legal_category(self, query: str) -> Optional[str]:
        """Identify the legal category of a query."""
        for category, keywords in self.concept_categories.items():
            if any(keyword in query for keyword in keywords):
                return category
        return None
    
    def _extract_legal_concepts(self, query: str, rag_result: str) -> List[Dict[str, Any]]:
        """Extract legal concepts from the query and result."""
        concepts = []
        
        # Common legal concepts
        concept_terms = [
            'contract', 'obligation', 'liability', 'right', 'duty', 'procedure',
            'jurisdiction', 'authority', 'penalty', 'compliance', 'governance',
            'constitutional', 'statutory', 'regulatory', 'administrative'
        ]
        
        text_to_analyze = f"{query} {rag_result}".lower()
        
        for term in concept_terms:
            if term in text_to_analyze:
                concepts.append({
                    'concept': term.title(),
                    'relevance': 'high' if term in query.lower() else 'medium',
                    'category': self._get_concept_category(term),
                    'confidence': 0.8 if term in query.lower() else 0.6
                })
        
        return concepts[:10]  # Limit to top 10 concepts
    
    def _identify_legal_frameworks(self, query: str, rag_result: str) -> List[Dict[str, Any]]:
        """Identify applicable legal frameworks."""
        frameworks = []
        
        framework_indicators = [
            'UAE Constitution', 'Civil Code', 'Commercial Code', 'Criminal Code',
            'Administrative Law', 'Labor Law', 'Federal Law', 'Local Law'
        ]
        
        text_to_analyze = f"{query} {rag_result}".lower()
        
        for framework in framework_indicators:
            if framework.lower() in text_to_analyze:
                frameworks.append({
                    'framework': framework,
                    'relevance': 'direct' if framework.lower() in query.lower() else 'related',
                    'scope': self._determine_framework_scope(framework),
                    'confidence': 0.9 if framework.lower() in query.lower() else 0.7
                })
        
        return frameworks
    
    def _calculate_conceptual_confidence(self, query: str, rag_result: str, concepts: List[Dict]) -> float:
        """Calculate confidence for conceptual analysis."""
        base_confidence = 0.5
        
        # Boost for comprehensive result
        if rag_result and len(rag_result) > 100:
            base_confidence += 0.2
        
        # Boost for identified concepts
        if concepts:
            concept_boost = min(len(concepts) * 0.05, 0.2)
            base_confidence += concept_boost
        
        # Boost for conceptual keywords
        conceptual_keywords = ['principle', 'framework', 'concept', 'theory', 'doctrine']
        conceptual_score = sum(1 for keyword in conceptual_keywords if keyword in rag_result.lower())
        base_confidence += min(conceptual_score * 0.05, 0.15)
        
        # This agent's specialty boost
        if any(term in query.lower() for term in ['concept', 'principle', 'framework', 'general', 'broad']):
            base_confidence += 0.1
        
        return min(base_confidence, 1.0)
    
    def _get_applied_specialization(self, query: str) -> List[str]:
        """Determine which specializations were applied."""
        applied = []
        query_lower = query.lower()
        
        if any(term in query_lower for term in ['concept', 'principle', 'theory']):
            applied.append('legal_concepts')
        
        if any(term in query_lower for term in ['framework', 'system', 'structure']):
            applied.append('framework_analysis')
        
        if any(term in query_lower for term in ['compare', 'versus', 'difference']):
            applied.append('comparative_law')
        
        if any(term in query_lower for term in ['overview', 'general', 'broad']):
            applied.append('system_overviews')
        
        if not applied:
            applied.append('general_global_rag')
        
        return applied
    
    def _get_concept_category(self, concept: str) -> str:
        """Get category for a legal concept."""
        concept_mapping = {
            'contract': 'civil',
            'obligation': 'civil',
            'liability': 'civil',
            'penalty': 'criminal',
            'procedure': 'procedural',
            'constitutional': 'constitutional',
            'administrative': 'administrative'
        }
        return concept_mapping.get(concept, 'general')
    
    def _determine_framework_scope(self, framework: str) -> str:
        """Determine the scope of a legal framework."""
        scope_mapping = {
            'UAE Constitution': 'foundational',
            'Civil Code': 'comprehensive',
            'Commercial Code': 'specialized',
            'Criminal Code': 'specialized',
            'Administrative Law': 'regulatory',
            'Labor Law': 'specialized'
        }
        return scope_mapping.get(framework, 'general')
    
    def _analyze_framework_structure(self, result: str) -> Dict[str, Any]:
        """Analyze the structure of a legal framework."""
        return {
            'hierarchical_levels': self._count_hierarchical_references(result),
            'organizational_patterns': self._identify_organizational_patterns(result),
            'structural_clarity': 'high' if len(result) > 200 else 'medium'
        }
    
    def _extract_key_principles(self, result: str) -> List[str]:
        """Extract key legal principles from analysis."""
        principles = []
        
        principle_indicators = [
            'fundamental principle', 'key principle', 'basic principle',
            'core concept', 'essential element', 'foundational aspect'
        ]
        
        for indicator in principle_indicators:
            if indicator in result.lower():
                principles.append(f"Principle identified: {indicator}")
        
        if not principles:
            principles.append("General legal principles apply")
        
        return principles[:5]
    
    def _identify_framework_relationships(self, result: str, domain: str) -> List[Dict[str, str]]:
        """Identify relationships between frameworks."""
        relationships = []
        
        relationship_patterns = [
            'governed by', 'regulated under', 'pursuant to', 'in accordance with',
            'subject to', 'derived from', 'consistent with'
        ]
        
        for pattern in relationship_patterns:
            if pattern in result.lower():
                relationships.append({
                    'type': 'hierarchical',
                    'description': f"Framework relationship indicated by '{pattern}'"
                })
        
        return relationships[:3]
    
    def _extract_similarities(self, result: str, concepts: List[str]) -> List[str]:
        """Extract similarities from comparative analysis."""
        similarities = []
        
        similarity_indicators = [
            'similar', 'alike', 'common', 'shared', 'both', 'equivalent'
        ]
        
        for indicator in similarity_indicators:
            if indicator in result.lower():
                similarities.append(f"Similarity: {indicator} characteristics identified")
        
        if not similarities:
            similarities.append("Common legal foundation in UAE law")
        
        return similarities[:3]
    
    def _extract_differences(self, result: str, concepts: List[str]) -> List[str]:
        """Extract differences from comparative analysis."""
        differences = []
        
        difference_indicators = [
            'different', 'distinct', 'unlike', 'whereas', 'however', 'contrast'
        ]
        
        for indicator in difference_indicators:
            if indicator in result.lower():
                differences.append(f"Difference: {indicator} characteristics noted")
        
        if not differences:
            differences.append("Distinct application and scope")
        
        return differences[:3]
    
    def _analyze_synthesis_quality(self, result: str, topic: str, sources: List[str]) -> Dict[str, Any]:
        """Analyze the quality of concept synthesis."""
        confidence_factors = []
        
        # Check for integration indicators
        integration_indicators = ['combines', 'integrates', 'synthesizes', 'unifies']
        integration_score = sum(1 for indicator in integration_indicators if indicator in result.lower())
        
        if integration_score > 0:
            confidence_factors.append(f"Integration indicators found: {integration_score}")
        
        # Check for comprehensive coverage
        if len(result) > 300:
            confidence_factors.append("Comprehensive synthesis provided")
        
        # Calculate overall confidence
        overall_confidence = min(0.6 + (integration_score * 0.1) + (len(result) / 1000), 1.0)
        
        return {
            'integration_score': integration_score,
            'confidence_factors': confidence_factors,
            'overall_confidence': overall_confidence
        }
    
    def _count_hierarchical_references(self, result: str) -> int:
        """Count references to hierarchical legal structures."""
        hierarchical_terms = ['article', 'section', 'chapter', 'part', 'title', 'subsection']
        return sum(1 for term in hierarchical_terms if term in result.lower())
    
    def _identify_organizational_patterns(self, result: str) -> List[str]:
        """Identify organizational patterns in legal frameworks."""
        patterns = []
        
        if 'hierarchical' in result.lower():
            patterns.append('hierarchical structure')
        
        if 'systematic' in result.lower():
            patterns.append('systematic organization')
        
        if 'categorical' in result.lower():
            patterns.append('categorical classification')
        
        if not patterns:
            patterns.append('standard legal organization')
        
        return patterns
    
    def _update_performance_metrics(self, processing_time: float, confidence: float, concept_count: int, framework_count: int):
        """Update Global RAG agent performance metrics."""
        if self.capabilities:
            cap = self.capabilities[0]  # Update first capability metrics
            
            # Track conceptual accuracy (approximated by confidence)
            old_accuracy = cap.performance_metrics.get('conceptual_accuracy', 0.0)
            cap.performance_metrics['conceptual_accuracy'] = (old_accuracy + confidence) / 2
            
            # Track framework coverage (based on identified frameworks)
            old_coverage = cap.performance_metrics.get('framework_coverage', 0.0)
            new_coverage = min(framework_count / 3.0, 1.0)  # Normalize to 0-1
            cap.performance_metrics['framework_coverage'] = (old_coverage + new_coverage) / 2
            
            # Track synthesis quality (based on concept extraction)
            old_quality = cap.performance_metrics.get('synthesis_quality', 0.0)
            new_quality = min(concept_count / 5.0, 1.0)  # Normalize to 0-1
            cap.performance_metrics['synthesis_quality'] = (old_quality + new_quality) / 2
    
    def get_specialization_report(self) -> Dict[str, Any]:
        """Get detailed report on Global RAG specialization performance."""
        return {
            'agent_id': self.agent_id,
            'specialization_areas': self.specialization_areas,
            'concept_categories': list(self.concept_categories.keys()),
            'capabilities': [cap.name for cap in self.get_capabilities()],
            'performance_metrics': self.performance_metrics,
            'conceptual_focus': 'broad legal frameworks and principles',
            'optimization_status': 'active'
        }
