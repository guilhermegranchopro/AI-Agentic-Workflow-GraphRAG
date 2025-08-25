"""
Advanced Legal Analysis Service with NLP and contradiction detection
"""

import asyncio
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import logging
from sentence_transformers import SentenceTransformer
import numpy as np
from openai import AsyncOpenAI

from app.config import settings
from app.services.graphrag import AdvancedGraphRAG

logger = logging.getLogger(__name__)

class LegalAnalysisService:
    """Advanced legal analysis with NLP and sophisticated reasoning"""
    
    def __init__(self):
        self.graphrag = AdvancedGraphRAG()
        self.embedding_model = None
        self.legal_patterns = self._load_legal_patterns()
        self.openai_client = AsyncOpenAI(
            api_key=settings.azure_openai_api_key,
            base_url=f"{settings.azure_openai_endpoint}/openai/deployments/{settings.azure_openai_deployment}"
        )
    
    def _load_legal_patterns(self) -> Dict[str, List[str]]:
        """Load legal pattern recognition rules"""
        return {
            'obligation_indicators': [
                r'\b(?:shall|must|required to|obligated to|duty to)\b',
                r'\b(?:mandatory|compulsory|binding)\b'
            ],
            'prohibition_indicators': [
                r'\b(?:shall not|must not|prohibited|forbidden|banned)\b',
                r'\b(?:illegal|unlawful|invalid)\b'
            ],
            'permission_indicators': [
                r'\b(?:may|permitted|allowed|authorized|entitled)\b',
                r'\b(?:discretion|option|choice)\b'
            ],
            'temporal_indicators': [
                r'\b(?:within|before|after|during|until)\s+\d+\s+(?:days?|months?|years?)\b',
                r'\b(?:immediately|forthwith|as soon as)\b'
            ],
            'authority_indicators': [
                r'\b(?:minister|court|judge|tribunal|authority|commission)\b',
                r'\b(?:federal|state|local|municipal|government)\b'
            ]
        }
    
    async def comprehensive_analysis(
        self,
        query: str,
        scope: Optional[str] = None,
        max_findings: int = 20,
        include_contradictions: bool = True
    ) -> Dict[str, Any]:
        """Comprehensive legal analysis with multiple analytical approaches"""
        
        analysis_results = {
            'query': query,
            'scope': scope,
            'timestamp': datetime.now().isoformat(),
            'findings': {}
        }
        
        try:
            # Initialize embedding model if needed
            if not self.embedding_model:
                self.embedding_model = SentenceTransformer(settings.legal_embedding_model)
            
            # Step 1: Advanced retrieval
            retrieval_results = await self.graphrag.advanced_retrieve(
                query=query,
                mode="hybrid",
                max_results=max_findings
            )
            
            passages = retrieval_results.get('passages', [])
            if not passages:
                analysis_results['findings']['error'] = "No relevant legal passages found"
                return analysis_results
            
            # Step 2: Legal pattern analysis
            pattern_analysis = await self._analyze_legal_patterns(passages)
            analysis_results['findings']['legal_patterns'] = pattern_analysis
            
            # Step 3: Semantic concept extraction
            concept_analysis = await self._extract_legal_concepts(passages, query)
            analysis_results['findings']['legal_concepts'] = concept_analysis
            
            # Step 4: Contradiction detection
            if include_contradictions:
                contradiction_analysis = await self._detect_contradictions(passages)
                analysis_results['findings']['contradictions'] = contradiction_analysis
            
            # Step 5: Legal reasoning synthesis
            synthesis = await self._synthesize_legal_analysis(
                query, passages, pattern_analysis, concept_analysis
            )
            analysis_results['findings']['synthesis'] = synthesis
            
            # Step 6: Generate recommendations
            recommendations = await self._generate_legal_recommendations(
                query, analysis_results['findings']
            )
            analysis_results['findings']['recommendations'] = recommendations
            
            analysis_results['status'] = 'success'
            analysis_results['total_passages_analyzed'] = len(passages)
            
        except Exception as e:
            logger.error(f"Comprehensive analysis error: {e}")
            analysis_results['status'] = 'error'
            analysis_results['error'] = str(e)
        
        return analysis_results
    
    async def _analyze_legal_patterns(self, passages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze legal patterns in passages"""
        
        pattern_results = {
            'obligations': [],
            'prohibitions': [],
            'permissions': [],
            'temporal_requirements': [],
            'authorities': []
        }
        
        pattern_mapping = {
            'obligations': 'obligation_indicators',
            'prohibitions': 'prohibition_indicators', 
            'permissions': 'permission_indicators',
            'temporal_requirements': 'temporal_indicators',
            'authorities': 'authority_indicators'
        }
        
        for passage in passages:
            text = passage['text'].lower()
            
            for category, pattern_key in pattern_mapping.items():
                patterns = self.legal_patterns[pattern_key]
                
                for pattern in patterns:
                    matches = re.finditer(pattern, text, re.IGNORECASE)
                    for match in matches:
                        # Extract surrounding context
                        start = max(0, match.start() - 50)
                        end = min(len(text), match.end() + 50)
                        context = text[start:end]
                        
                        pattern_results[category].append({
                            'pattern': match.group(),
                            'context': context,
                            'node_id': passage['nodeId'],
                            'confidence': passage['score']
                        })
        
        # Calculate pattern statistics
        pattern_stats = {}
        for category, findings in pattern_results.items():
            pattern_stats[category] = {
                'count': len(findings),
                'avg_confidence': np.mean([f['confidence'] for f in findings]) if findings else 0.0
            }
        
        return {
            'patterns': pattern_results,
            'statistics': pattern_stats,
            'analysis_method': 'regex_pattern_matching'
        }
    
    async def _extract_legal_concepts(
        self, 
        passages: List[Dict[str, Any]], 
        query: str
    ) -> Dict[str, Any]:
        """Extract and analyze legal concepts using semantic similarity"""
        
        # Extract potential legal concepts using embeddings
        legal_concepts = []
        query_embedding = self.embedding_model.encode(query)
        
        for passage in passages:
            text = passage['text']
            
            # Split into sentences for concept extraction
            sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 20]
            
            for sentence in sentences:
                sentence_embedding = self.embedding_model.encode(sentence)
                similarity = np.dot(query_embedding, sentence_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(sentence_embedding)
                )
                
                if similarity > settings.semantic_similarity_threshold:
                    legal_concepts.append({
                        'concept': sentence,
                        'similarity': float(similarity),
                        'source_node': passage['nodeId'],
                        'source_confidence': passage['score']
                    })
        
        # Sort by similarity
        legal_concepts.sort(key=lambda x: x['similarity'], reverse=True)
        
        # Group similar concepts
        concept_groups = await self._group_similar_concepts(legal_concepts[:15])
        
        return {
            'individual_concepts': legal_concepts[:10],
            'concept_groups': concept_groups,
            'total_concepts_found': len(legal_concepts),
            'analysis_method': 'semantic_embedding_similarity'
        }
    
    async def _group_similar_concepts(
        self, 
        concepts: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Group semantically similar concepts"""
        
        if len(concepts) < 2:
            return [{'group_id': 0, 'concepts': concepts, 'theme': 'Single concept group'}]
        
        # Calculate pairwise similarities
        embeddings = [self.embedding_model.encode(c['concept']) for c in concepts]
        
        groups = []
        used_indices = set()
        
        for i, concept in enumerate(concepts):
            if i in used_indices:
                continue
            
            # Start new group
            group = [concept]
            used_indices.add(i)
            
            # Find similar concepts
            for j, other_concept in enumerate(concepts[i+1:], i+1):
                if j in used_indices:
                    continue
                
                similarity = np.dot(embeddings[i], embeddings[j]) / (
                    np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j])
                )
                
                if similarity > 0.8:  # High similarity threshold for grouping
                    group.append(other_concept)
                    used_indices.add(j)
            
            # Generate group theme
            group_texts = [c['concept'][:100] for c in group]
            theme = await self._generate_concept_theme(group_texts)
            
            groups.append({
                'group_id': len(groups),
                'concepts': group,
                'theme': theme,
                'size': len(group)
            })
        
        return groups
    
    async def _generate_concept_theme(self, concept_texts: List[str]) -> str:
        """Generate theme for a group of concepts using LLM"""
        
        try:
            concepts_text = "\n".join([f"- {text}" for text in concept_texts])
            
            response = await self.openai_client.chat.completions.create(
                model=settings.azure_openai_deployment,
                messages=[
                    {
                        "role": "system", 
                        "content": "Generate a brief theme or category name for these related legal concepts. Respond with just the theme name, maximum 5 words."
                    },
                    {
                        "role": "user", 
                        "content": f"Legal concepts:\n{concepts_text}"
                    }
                ],
                temperature=0.1,
                max_tokens=20
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Theme generation error: {e}")
            return "Related legal concepts"
    
    async def _detect_contradictions(
        self, 
        passages: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Detect potential contradictions between legal passages"""
        
        contradictions = []
        
        # Compare passages pairwise for potential contradictions
        for i, passage1 in enumerate(passages):
            for j, passage2 in enumerate(passages[i+1:], i+1):
                
                # Use LLM to detect contradictions
                contradiction_analysis = await self._analyze_passage_contradiction(
                    passage1, passage2
                )
                
                if contradiction_analysis['is_contradiction']:
                    contradictions.append({
                        'passage1': {
                            'node_id': passage1['nodeId'],
                            'text': passage1['text'][:200],
                            'score': passage1['score']
                        },
                        'passage2': {
                            'node_id': passage2['nodeId'], 
                            'text': passage2['text'][:200],
                            'score': passage2['score']
                        },
                        'contradiction_type': contradiction_analysis['type'],
                        'explanation': contradiction_analysis['explanation'],
                        'confidence': contradiction_analysis['confidence']
                    })
                
                # Limit contradiction analysis to prevent excessive API calls
                if len(contradictions) >= 5:
                    break
            
            if len(contradictions) >= 5:
                break
        
        return {
            'contradictions': contradictions,
            'total_contradictions_found': len(contradictions),
            'analysis_method': 'llm_pairwise_comparison'
        }
    
    async def _analyze_passage_contradiction(
        self, 
        passage1: Dict[str, Any], 
        passage2: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze if two passages contradict each other"""
        
        try:
            prompt = f"""Analyze these two legal passages for contradictions:

Passage 1: {passage1['text'][:300]}

Passage 2: {passage2['text'][:300]}

Determine if these passages contradict each other. Look for:
1. Direct contradictions (one says X, other says not X)
2. Conflicting requirements or prohibitions
3. Inconsistent interpretations of the same legal concept

Respond in JSON format:
{{
    "is_contradiction": true/false,
    "type": "direct/indirect/temporal/none",
    "explanation": "brief explanation",
    "confidence": 0.0-1.0
}}"""

            response = await self.openai_client.chat.completions.create(
                model=settings.azure_openai_deployment,
                messages=[
                    {"role": "system", "content": "You are a legal analysis expert. Analyze legal texts for contradictions and respond only in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=200
            )
            
            # Parse JSON response
            import json
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            logger.error(f"Contradiction analysis error: {e}")
            return {
                "is_contradiction": False,
                "type": "analysis_error",
                "explanation": f"Analysis failed: {str(e)}",
                "confidence": 0.0
            }
    
    async def _synthesize_legal_analysis(
        self,
        query: str,
        passages: List[Dict[str, Any]],
        pattern_analysis: Dict[str, Any],
        concept_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synthesize comprehensive legal analysis"""
        
        try:
            # Prepare synthesis context
            top_passages = passages[:5]
            passage_texts = [p['text'][:300] for p in top_passages]
            
            pattern_summary = {
                category: stats['count'] 
                for category, stats in pattern_analysis['statistics'].items()
                if stats['count'] > 0
            }
            
            concept_themes = [group['theme'] for group in concept_analysis['concept_groups']]
            
            synthesis_prompt = f"""Provide a comprehensive legal analysis synthesis for the query: "{query}"

Based on analysis of {len(passages)} legal passages, pattern analysis, and concept extraction:

Key Patterns Found:
{pattern_summary}

Legal Concept Themes:
{concept_themes}

Top Relevant Passages:
{chr(10).join([f"{i+1}. {text}" for i, text in enumerate(passage_texts)])}

Provide a structured legal analysis including:
1. Executive summary
2. Key legal findings
3. Pattern-based insights
4. Conceptual analysis
5. Legal implications
6. Recommended actions

Keep the analysis professional, precise, and actionable."""

            response = await self.openai_client.chat.completions.create(
                model=settings.azure_openai_deployment,
                messages=[
                    {"role": "system", "content": "You are a senior legal analyst providing comprehensive legal research synthesis."},
                    {"role": "user", "content": synthesis_prompt}
                ],
                temperature=0.15,
                max_tokens=1000
            )
            
            return {
                'status': 'success',
                'synthesis': response.choices[0].message.content,
                'passages_analyzed': len(passages),
                'patterns_found': sum(pattern_analysis['statistics'][cat]['count'] for cat in pattern_analysis['statistics']),
                'concepts_extracted': len(concept_analysis['individual_concepts'])
            }
            
        except Exception as e:
            logger.error(f"Synthesis error: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'fallback': 'Synthesis temporarily unavailable'
            }
    
    async def _generate_legal_recommendations(
        self,
        query: str,
        findings: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate actionable legal recommendations"""
        
        recommendations = []
        
        # Recommendation based on patterns
        patterns = findings.get('legal_patterns', {}).get('statistics', {})
        
        if patterns.get('obligations', {}).get('count', 0) > 0:
            recommendations.append({
                'type': 'compliance',
                'priority': 'high',
                'recommendation': 'Review identified legal obligations for compliance requirements',
                'basis': f"Found {patterns['obligations']['count']} obligation patterns"
            })
        
        if patterns.get('prohibitions', {}).get('count', 0) > 0:
            recommendations.append({
                'type': 'risk_management',
                'priority': 'high', 
                'recommendation': 'Assess prohibition compliance to avoid legal violations',
                'basis': f"Found {patterns['prohibitions']['count']} prohibition patterns"
            })
        
        # Recommendation based on contradictions
        contradictions = findings.get('contradictions', {})
        if contradictions.get('total_contradictions_found', 0) > 0:
            recommendations.append({
                'type': 'conflict_resolution',
                'priority': 'medium',
                'recommendation': 'Legal review required to resolve identified contradictions',
                'basis': f"Found {contradictions['total_contradictions_found']} potential contradictions"
            })
        
        # Recommendation based on concept analysis
        concepts = findings.get('legal_concepts', {})
        if concepts.get('total_concepts_found', 0) > 5:
            recommendations.append({
                'type': 'comprehensive_review',
                'priority': 'medium',
                'recommendation': 'Consider comprehensive legal review given concept complexity',
                'basis': f"Identified {concepts['total_concepts_found']} distinct legal concepts"
            })
        
        return recommendations
