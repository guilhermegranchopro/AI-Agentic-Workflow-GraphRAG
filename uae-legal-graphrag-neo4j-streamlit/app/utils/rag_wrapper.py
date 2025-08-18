"""GraphRAG compatibility layer for the Legal Assistant chatbot."""

from typing import List, Dict, Any
from datetime import date, datetime
from src.graph.tools import (
    semantic_search_provisions, 
    local_rag_query as _local_rag_query,
    global_rag_communities,
    drift_rag_query as _drift_rag_query
)


def local_rag_query(query_text: str) -> str:
    """
    Local RAG query wrapper that takes a text query and returns formatted text.
    
    Args:
        query_text: Natural language query
        
    Returns:
        Formatted text response with provisions and context
    """
    try:
        # First find relevant provisions using semantic search
        semantic_results = semantic_search_provisions(query_text, 5)
        
        if not semantic_results:
            return "No relevant provisions found for your query."
        
        # Format the response
        response_parts = []
        response_parts.append(f"Local RAG Query Results for: '{query_text}'\n")
        
        for i, result in enumerate(semantic_results, 1):
            provision = result.get("provision", {})
            score = result.get("score", 0)
            
            response_parts.append(f"\n[{i}] Provision ID: {provision.get('id', 'Unknown')}")
            response_parts.append(f"Relevance Score: {score:.3f}")
            
            if "text" in provision:
                text = provision["text"]
                if len(text) > 300:
                    text = text[:300] + "..."
                response_parts.append(f"Text: {text}")
            
            # Add context if available
            context = result.get("context", {})
            if context:
                instrument = context.get("instrument", {})
                if instrument:
                    response_parts.append(f"Source: {instrument.get('id', 'Unknown')}")
        
        return "\n".join(response_parts)
        
    except Exception as e:
        return f"Error in local RAG query: {str(e)}"


def global_rag_query(query_text: str) -> str:
    """
    Global RAG query wrapper that uses community structure.
    
    Args:
        query_text: Natural language query
        
    Returns:
        Formatted text response with community-based analysis
    """
    try:
        # Get community structure
        communities_data = global_rag_communities(10)
        
        if "error" in communities_data:
            return f"Error in global RAG: {communities_data['error']}"
        
        # Also get semantic search results for context
        semantic_results = semantic_search_provisions(query_text, 3)
        
        response_parts = []
        response_parts.append(f"Global RAG Query Results for: '{query_text}'\n")
        
        # Add community information
        communities = communities_data.get("communities", [])
        if communities:
            response_parts.append("📊 Relevant Legal Communities:")
            for i, community in enumerate(communities[:5], 1):
                community_id = community.get("community_id", "Unknown")
                size = community.get("size", 0)
                response_parts.append(f"[{i}] Community {community_id}: {size} provisions")
                
                # Add sample provisions from community
                nodes = community.get("nodes", [])[:3]  # Top 3 nodes
                for node in nodes:
                    if "text" in node:
                        text = node["text"][:150] + "..." if len(node["text"]) > 150 else node["text"]
                        response_parts.append(f"   • {text}")
        
        # Add semantic search context
        if semantic_results:
            response_parts.append("\n🔍 Most Relevant Provisions:")
            for i, result in enumerate(semantic_results, 1):
                provision = result.get("provision", {})
                score = result.get("score", 0)
                response_parts.append(f"[{i}] Score: {score:.3f}")
                
                if "text" in provision:
                    text = provision["text"][:200] + "..." if len(provision["text"]) > 200 else provision["text"]
                    response_parts.append(f"   {text}")
        
        return "\n".join(response_parts)
        
    except Exception as e:
        return f"Error in global RAG query: {str(e)}"


def drift_rag_query(query_text: str, as_of_date: date) -> str:
    """
    DRIFT RAG query wrapper with temporal filtering.
    
    Args:
        query_text: Natural language query
        as_of_date: Date for temporal filtering
        
    Returns:
        Formatted text response with temporal context
    """
    try:
        # Use the actual DRIFT RAG function
        drift_results = _drift_rag_query(query_text, as_of_date, top_communities=3)
        
        if "error" in drift_results:
            return f"DRIFT RAG Error: {drift_results['error']}"
        
        response_parts = []
        response_parts.append(f"DRIFT RAG Query Results for: '{query_text}' (as of {as_of_date})\n")
        
        # Format the DRIFT results
        if "communities" in drift_results:
            communities = drift_results["communities"]
            response_parts.append("⏱️ Temporal Community Analysis:")
            
            for i, community in enumerate(communities, 1):
                community_id = community.get("community_id", "Unknown")
                relevance = community.get("relevance_score", 0)
                response_parts.append(f"[{i}] Community {community_id} (Relevance: {relevance:.3f})")
                
                # Add provisions from this community
                provisions = community.get("provisions", [])[:3]
                for provision in provisions:
                    if "text" in provision:
                        text = provision["text"][:150] + "..." if len(provision["text"]) > 150 else provision["text"]
                        response_parts.append(f"   • {text}")
        
        # Add semantic fallback
        if not response_parts or len(response_parts) <= 2:
            semantic_results = semantic_search_provisions(query_text, 3)
            if semantic_results:
                response_parts.append("\n🔍 Fallback Semantic Results:")
                for i, result in enumerate(semantic_results, 1):
                    provision = result.get("provision", {})
                    score = result.get("score", 0)
                    response_parts.append(f"[{i}] Relevance: {score:.3f}")
                    
                    if "text" in provision:
                        text = provision["text"][:200] + "..." if len(provision["text"]) > 200 else provision["text"]
                        response_parts.append(f"   {text}")
        
        return "\n".join(response_parts)
        
    except Exception as e:
        return f"Error in DRIFT RAG query: {str(e)}"


def hybrid_rag_query(query_text: str, strategy: str = "auto") -> str:
    """
    Hybrid RAG query that combines multiple strategies.
    
    Args:
        query_text: Natural language query
        strategy: Strategy to use ("local", "global", "drift", "auto")
        
    Returns:
        Formatted text response
    """
    if strategy == "local":
        return local_rag_query(query_text)
    elif strategy == "global":
        return global_rag_query(query_text)
    elif strategy == "drift":
        return drift_rag_query(query_text, datetime.now().date())
    else:  # auto
        # Simple auto-selection logic
        query_lower = query_text.lower()
        
        if any(word in query_lower for word in ['recent', 'current', 'latest', 'new']):
            return drift_rag_query(query_text, datetime.now().date())
        elif any(word in query_lower for word in ['overview', 'explain', 'what is']):
            return global_rag_query(query_text)
        else:
            return local_rag_query(query_text)
