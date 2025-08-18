"""Enhanced GraphRAG utilities for the Legal Assistant chatbot."""

from typing import List, Dict, Optional, Tuple
import re
from datetime import datetime, date
from src.db import db


def analyze_legal_query(query: str) -> Dict[str, any]:
    """
    Analyze a legal query to determine the best RAG strategy and extract key entities.
    
    Args:
        query: The user's legal question
        
    Returns:
        Dictionary with analysis results
    """
    query_lower = query.lower()
    
    # Legal entity patterns
    article_pattern = r'article\s+(\d+)'
    law_pattern = r'law\s+(?:no\.?\s*)?(\d+)(?:\s+of\s+(\d{4}))?'
    decree_pattern = r'decree\s+(?:no\.?\s*)?(\d+)(?:\s+of\s+(\d{4}))?'
    
    # Extract entities
    entities = {
        'articles': re.findall(article_pattern, query_lower),
        'laws': re.findall(law_pattern, query_lower),
        'decrees': re.findall(decree_pattern, query_lower),
    }
    
    # Categorize query type
    query_type = categorize_query(query_lower)
    
    # Determine urgency/temporal aspects
    temporal_indicators = ['recent', 'latest', 'current', 'new', 'updated', 'changed']
    is_temporal = any(indicator in query_lower for indicator in temporal_indicators)
    
    # Determine complexity
    complexity_indicators = ['compare', 'difference', 'versus', 'relationship', 'how', 'why']
    is_complex = any(indicator in query_lower for indicator in complexity_indicators)
    
    return {
        'entities': entities,
        'query_type': query_type,
        'is_temporal': is_temporal,
        'is_complex': is_complex,
        'suggested_strategy': suggest_rag_strategy(query_type, is_temporal, is_complex),
        'confidence': calculate_confidence(entities, query_type)
    }


def categorize_query(query: str) -> str:
    """Categorize the type of legal query."""
    
    # Definition queries
    if any(word in query for word in ['what is', 'define', 'definition', 'meaning']):
        return 'definition'
    
    # Procedural queries  
    elif any(word in query for word in ['how to', 'process', 'procedure', 'steps']):
        return 'procedural'
    
    # Specific article/law queries
    elif any(word in query for word in ['article', 'section', 'paragraph', 'clause']):
        return 'specific_provision'
    
    # Comparative queries
    elif any(word in query for word in ['compare', 'difference', 'versus', 'vs']):
        return 'comparative'
    
    # Penalty/consequence queries
    elif any(word in query for word in ['penalty', 'punishment', 'fine', 'consequence']):
        return 'penalty'
    
    # Rights and obligations
    elif any(word in query for word in ['rights', 'obligations', 'duties', 'responsibilities']):
        return 'rights_obligations'
    
    # General concept
    else:
        return 'general'


def suggest_rag_strategy(query_type: str, is_temporal: bool, is_complex: bool) -> str:
    """Suggest the best RAG strategy based on query analysis."""
    
    if is_temporal:
        return 'drift'
    elif query_type in ['specific_provision', 'penalty']:
        return 'local'
    elif query_type in ['definition', 'general', 'rights_obligations'] or is_complex:
        return 'global'
    else:
        return 'local'


def calculate_confidence(entities: Dict, query_type: str) -> float:
    """Calculate confidence score for the query analysis."""
    
    base_confidence = 0.7
    
    # Boost confidence if specific entities found
    if entities['articles'] or entities['laws'] or entities['decrees']:
        base_confidence += 0.2
    
    # Adjust based on query type clarity
    if query_type in ['specific_provision', 'definition']:
        base_confidence += 0.1
    
    return min(base_confidence, 1.0)


def enhanced_source_extraction(rag_result: str, query_analysis: Dict, max_sources: int = 5) -> List[Dict]:
    """
    Enhanced source extraction that considers query analysis.
    
    Args:
        rag_result: RAG query result
        query_analysis: Analysis of the original query
        max_sources: Maximum sources to extract
        
    Returns:
        List of enhanced source dictionaries
    """
    sources = []
    
    try:
        # Extract from RAG result text
        sources.extend(_extract_from_text(rag_result, max_sources // 2))
        
        # Get additional sources from knowledge graph
        if len(sources) < max_sources:
            remaining = max_sources - len(sources)
            kg_sources = _get_kg_sources(query_analysis, remaining)
            sources.extend(kg_sources)
        
        # Enhance sources with additional metadata
        for source in sources:
            source['extraction_method'] = 'enhanced'
            source['query_type'] = query_analysis['query_type']
            source['timestamp'] = datetime.now().isoformat()
    
    except Exception as e:
        print(f"Source extraction error: {e}")
    
    return sources[:max_sources]


def _extract_from_text(text: str, max_sources: int) -> List[Dict]:
    """Extract sources from RAG result text."""
    sources = []
    lines = text.split('\n')
    
    source_indicators = [
        'article', 'section', 'law', 'decree', 'constitution',
        'federal law', 'civil code', 'penal code', 'commercial code'
    ]
    
    for line in lines:
        line_lower = line.lower().strip()
        if any(indicator in line_lower for indicator in source_indicators) and len(line.strip()) > 10:
            
            # Extract article/law numbers if present
            article_match = re.search(r'article\s+(\d+)', line_lower)
            law_match = re.search(r'law\s+(?:no\.?\s*)?(\d+)', line_lower)
            
            source = {
                'text': line.strip(),
                'type': 'Legal Provision',
                'relevance_score': 0.8,
                'article_number': article_match.group(1) if article_match else None,
                'law_number': law_match.group(1) if law_match else None,
            }
            
            sources.append(source)
            
            if len(sources) >= max_sources:
                break
    
    return sources


def _get_kg_sources(query_analysis: Dict, max_sources: int) -> List[Dict]:
    """Get additional sources from the knowledge graph."""
    sources = []
    
    try:
        with db.session() as session:
            # Build query based on extracted entities
            kg_query = _build_kg_query(query_analysis)
            
            result = session.run(kg_query, limit=max_sources)
            
            for record in result:
                source = {
                    'text': record.get('text', 'No text available'),
                    'type': 'Knowledge Graph',
                    'id': record.get('id'),
                    'instrument': record.get('instrument'),
                    'article_number': record.get('number'),
                    'relevance_score': 0.7,
                }
                sources.append(source)
    
    except Exception as e:
        print(f"KG source extraction error: {e}")
    
    return sources


def _build_kg_query(query_analysis: Dict) -> str:
    """Build a Cypher query based on query analysis."""
    
    entities = query_analysis['entities']
    query_type = query_analysis['query_type']
    
    # Base query
    base_query = """
    MATCH (p:Provision)
    OPTIONAL MATCH (p)<-[:HAS_PROVISION]-(i:Instrument)
    """
    
    # Add conditions based on entities
    conditions = []
    
    if entities['articles']:
        article_nums = [int(num) for num in entities['articles']]
        conditions.append(f"p.number IN {article_nums}")
    
    if entities['laws']:
        law_nums = [int(match[0]) for match in entities['laws']]
        conditions.append(f"i.number IN {law_nums}")
    
    # Add WHERE clause if conditions exist
    if conditions:
        where_clause = "WHERE " + " OR ".join(conditions)
    else:
        where_clause = ""
    
    # Return clause
    return_clause = """
    RETURN p.id as id, p.text as text, p.number as number, 
           i.id as instrument
    LIMIT $limit
    """
    
    return base_query + where_clause + return_clause


def format_legal_response(response: str, sources: List[Dict], citation_style: str) -> str:
    """
    Format the legal response with proper citations.
    
    Args:
        response: Raw response from Azure OpenAI
        sources: List of source dictionaries
        citation_style: Citation formatting style
        
    Returns:
        Formatted response with citations
    """
    if not sources:
        return response
    
    # Add citations based on style
    if citation_style == "Academic":
        return _add_academic_citations(response, sources)
    elif citation_style == "Brief":
        return _add_brief_citations(response, sources)
    else:  # Detailed
        return _add_detailed_citations(response, sources)


def _add_academic_citations(response: str, sources: List[Dict]) -> str:
    """Add academic-style citations."""
    citation_text = "\n\n**References:**\n"
    
    for i, source in enumerate(sources, 1):
        if source.get('instrument') and source.get('article_number'):
            citation = f"{i}. {source['instrument']}, Article {source['article_number']}"
        elif source.get('instrument'):
            citation = f"{i}. {source['instrument']}"
        else:
            citation = f"{i}. {source.get('type', 'Legal Source')}"
        
        citation_text += f"{citation}\n"
    
    return response + citation_text


def _add_brief_citations(response: str, sources: List[Dict]) -> str:
    """Add brief citations."""
    if sources:
        citation_text = "\n\n*Sources: "
        source_refs = []
        
        for source in sources:
            if source.get('article_number'):
                source_refs.append(f"Art. {source['article_number']}")
            elif source.get('instrument'):
                source_refs.append(source['instrument'][:20] + "...")
        
        citation_text += ", ".join(source_refs[:3]) + "*"
        return response + citation_text
    
    return response


def _add_detailed_citations(response: str, sources: List[Dict]) -> str:
    """Add detailed citations."""
    if not sources:
        return response
    
    citation_text = "\n\n---\n**📚 Legal Sources:**\n\n"
    
    for i, source in enumerate(sources, 1):
        citation_text += f"**[{i}]** "
        
        if source.get('instrument'):
            citation_text += f"{source['instrument']}"
            
        if source.get('article_number'):
            citation_text += f", Article {source['article_number']}"
            
        if source.get('law_number'):
            citation_text += f", Law No. {source['law_number']}"
        
        citation_text += "\n\n"
    
    return response + citation_text


def get_related_provisions(provision_id: str, max_related: int = 3) -> List[Dict]:
    """
    Get provisions related to a specific provision through graph relationships.
    
    Args:
        provision_id: ID of the source provision
        max_related: Maximum related provisions to return
        
    Returns:
        List of related provision dictionaries
    """
    try:
        with db.session() as session:
            query = """
            MATCH (p:Provision {id: $provision_id})
            MATCH (p)-[r]-(related:Provision)
            OPTIONAL MATCH (related)<-[:HAS_PROVISION]-(i:Instrument)
            RETURN related.id as id, related.text as text, 
                   related.number as number, i.id as instrument,
                   type(r) as relationship_type
            LIMIT $max_related
            """
            
            result = session.run(query, provision_id=provision_id, max_related=max_related)
            
            return [dict(record) for record in result]
            
    except Exception as e:
        print(f"Related provisions error: {e}")
        return []
