"""Grounding validation to ensure answers cite retrieved nodes."""
import logging
from typing import List, Dict, Any, Set
import re

logger = logging.getLogger(__name__)


def extract_node_ids_from_results(results: List[Dict[str, Any]]) -> Set[str]:
    """
    Extract all node IDs from query results for grounding validation.
    
    Args:
        results: List of query results containing nodes
        
    Returns:
        Set of node IDs found in results
    """
    node_ids = set()
    
    for result in results:
        # Handle different result structures
        if "provision" in result:
            provision = result["provision"]
            if isinstance(provision, dict) and "id" in provision:
                node_ids.add(provision["id"])
        
        if "neighbors" in result:
            for neighbor in result["neighbors"]:
                if "neighbor" in neighbor:
                    neighbor_node = neighbor["neighbor"]
                    if isinstance(neighbor_node, dict) and "id" in neighbor_node:
                        node_ids.add(neighbor_node["id"])
        
        if "node" in result:
            node = result["node"]
            if isinstance(node, dict) and "id" in node:
                node_ids.add(node["id"])
    
    return node_ids


def extract_citations_from_text(text: str) -> Set[str]:
    """
    Extract node ID citations from generated text.
    
    Args:
        text: Generated text that should contain citations
        
    Returns:
        Set of cited node IDs
    """
    # Look for patterns like [node-id], (node-id), or node-id references
    citation_patterns = [
        r'\[([a-zA-Z0-9\-_]+)\]',  # [node-id]
        r'\(([a-zA-Z0-9\-_]+)\)',  # (node-id)
        r'(?:Article|Art\.?\s+)([0-9]+)',  # Article 12, Art. 12
        r'(?:provision|section)\s+([a-zA-Z0-9\-_]+)',  # provision civil-art-106
    ]
    
    citations = set()
    for pattern in citation_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        citations.update(matches)
    
    return citations


def calculate_grounding_score(
    generated_text: str,
    query_results: List[Dict[str, Any]],
    min_citations: int = 1
) -> Dict[str, Any]:
    """
    Calculate grounding score for generated text against query results.
    
    Args:
        generated_text: Text that should be grounded in results
        query_results: Results from graph queries
        min_citations: Minimum number of citations required
        
    Returns:
        Dictionary with grounding metrics
    """
    # Extract available node IDs from results
    available_nodes = extract_node_ids_from_results(query_results)
    
    # Extract citations from generated text
    cited_nodes = extract_citations_from_text(generated_text)
    
    # Calculate metrics
    valid_citations = cited_nodes.intersection(available_nodes)
    invalid_citations = cited_nodes - available_nodes
    
    citation_count = len(valid_citations)
    grounding_ratio = len(valid_citations) / max(len(cited_nodes), 1)
    coverage_ratio = len(valid_citations) / max(len(available_nodes), 1)
    
    is_grounded = (
        citation_count >= min_citations and
        grounding_ratio >= 0.7 and  # At least 70% of citations are valid
        len(invalid_citations) == 0  # No invalid citations
    )
    
    return {
        "is_grounded": is_grounded,
        "citation_count": citation_count,
        "valid_citations": list(valid_citations),
        "invalid_citations": list(invalid_citations),
        "grounding_ratio": grounding_ratio,
        "coverage_ratio": coverage_ratio,
        "available_nodes": list(available_nodes),
        "min_citations_met": citation_count >= min_citations
    }


def validate_answer_grounding(
    answer: str,
    sources: List[Dict[str, Any]],
    strict: bool = False
) -> bool:
    """
    Validate if an answer is properly grounded in its sources.
    
    Args:
        answer: Generated answer text
        sources: Source materials/query results
        strict: Whether to use strict grounding requirements
        
    Returns:
        True if answer is sufficiently grounded
    """
    try:
        grounding_metrics = calculate_grounding_score(answer, sources)
        
        if strict:
            # Strict mode: require high citation rate and coverage
            return (
                grounding_metrics["is_grounded"] and
                grounding_metrics["coverage_ratio"] >= 0.5
            )
        else:
            # Lenient mode: just check basic grounding
            return grounding_metrics["is_grounded"]
            
    except Exception as e:
        logger.error(f"Error validating grounding: {e}")
        return False


def create_grounded_summary(
    query_results: List[Dict[str, Any]],
    include_ids: bool = True
) -> str:
    """
    Create a summary that explicitly cites source node IDs.
    
    Args:
        query_results: Results from graph queries
        include_ids: Whether to include node IDs in citations
        
    Returns:
        Grounded summary text with explicit citations
    """
    if not query_results:
        return "No relevant sources found."
    
    summary_parts = []
    cited_nodes = set()
    
    for i, result in enumerate(query_results[:5]):  # Limit to top 5
        if "provision" in result:
            provision = result["provision"]
            node_id = provision.get("id", f"item-{i}")
            text = provision.get("text", "")
            article_title = provision.get("article_title", "")
            
            if node_id not in cited_nodes:
                citation = f"[{node_id}]" if include_ids else f"Article {provision.get('number', i+1)}"
                summary_part = f"According to {citation}"
                if article_title:
                    summary_part += f" ({article_title})"
                summary_part += f": {text[:200]}..."
                
                summary_parts.append(summary_part)
                cited_nodes.add(node_id)
    
    if summary_parts:
        return "\n\n".join(summary_parts)
    else:
        return "Sources available but could not extract citable content."


def get_fallback_sources_only(query_results: List[Dict[str, Any]]) -> str:
    """
    Return a sources-only view when grounding fails.
    
    Args:
        query_results: Results from graph queries
        
    Returns:
        Formatted list of sources without interpretation
    """
    if not query_results:
        return "No sources found for this query."
    
    sources_list = []
    for i, result in enumerate(query_results[:10]):
        if "provision" in result:
            provision = result["provision"]
            context = result.get("context", {})
            
            source_info = f"**Source {i+1}:** {provision.get('id', 'Unknown')}"
            if provision.get("number"):
                source_info += f" (Article {provision['number']})"
            
            if context.get("instrument"):
                instrument = context["instrument"]
                source_info += f"\n- From: {instrument.get('title', 'Unknown Instrument')}"
                if instrument.get("year"):
                    source_info += f" ({instrument['year']})"
            
            if provision.get("text"):
                source_info += f"\n- Text: {provision['text'][:300]}..."
            
            if "score" in result:
                source_info += f"\n- Relevance: {result['score']:.3f}"
            
            sources_list.append(source_info)
    
    return "\n\n".join(sources_list)
