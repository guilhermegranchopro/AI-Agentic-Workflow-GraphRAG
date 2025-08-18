"""High-level graph tools used by the Streamlit app."""
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import date, datetime
from src.graph.queries import (
    knn_provisions, asof_neighbors, asof_amendments, 
    communities_top, nodes_in_community, provision_by_community,
    search_provisions_by_text, get_provision_context
)
from src.embeddings.azure_openai import embeddings_client

logger = logging.getLogger(__name__)


def semantic_search_provisions(query_text: str, k: int = 5) -> List[Dict[str, Any]]:
    """
    Perform semantic search on provisions using embeddings.
    
    Args:
        query_text: Natural language query
        k: Number of results to return
        
    Returns:
        List of provisions with similarity scores
    """
    try:
        # Generate embedding for query
        query_embedding = embeddings_client.get_embeddings(query_text)
        
        # Find similar provisions
        results = knn_provisions(query_embedding, k)
        
        # Enrich with context
        enriched_results = []
        for result in results:
            provision_id = result["provision"]["id"]
            context = get_provision_context(provision_id)
            if context:
                result["context"] = context
            enriched_results.append(result)
            
        return enriched_results
        
    except Exception as e:
        logger.error(f"Error in semantic search: {e}")
        return []


def local_rag_query(provision_id: str, as_of_date: date, 
                   rel_types: List[str] = None) -> Dict[str, Any]:
    """
    Perform Local RAG query starting from a specific provision.
    
    Args:
        provision_id: Starting provision ID
        as_of_date: Date for temporal filtering
        rel_types: Relationship types to traverse
        
    Returns:
        Dictionary with paths and context
    """
    try:
        # Get provision context
        context = get_provision_context(provision_id)
        if not context:
            return {"error": f"Provision {provision_id} not found"}
        
        # Get neighbors with temporal filtering
        neighbors = asof_neighbors(provision_id, as_of_date, rel_types)
        
        # Get amendments
        amendments = asof_amendments(provision_id, as_of_date)
        
        return {
            "provision": context,
            "neighbors": neighbors,
            "amendments": amendments,
            "as_of_date": as_of_date.isoformat(),
            "path_count": len(neighbors)
        }
        
    except Exception as e:
        logger.error(f"Error in local RAG query: {e}")
        return {"error": str(e)}


def local_rag_query_simplified(query_text: str) -> Dict[str, Any]:
    """
    Simplified Local RAG query that takes just a query text (for agent compatibility).
    
    Args:
        query_text: Natural language query
        
    Returns:
        Dictionary with local RAG results
    """
    try:
        # First do semantic search to find relevant provisions
        semantic_results = semantic_search_provisions(query_text, 5)
        
        if not semantic_results:
            return {"error": "No relevant provisions found"}
        
        # Use current date as default
        from datetime import date
        as_of_date = date.today()
        
        # Take the most relevant provision and do local RAG
        top_provision = semantic_results[0]["provision"]
        provision_id = top_provision["id"]
        
        # Run full local RAG query
        local_result = local_rag_query(provision_id, as_of_date)
        
        # Add semantic context
        local_result["semantic_seeds"] = semantic_results[:3]
        local_result["query"] = query_text
        
        return local_result
        
    except Exception as e:
        logger.error(f"Error in simplified local RAG query: {e}")
        return {"error": str(e)}


def global_rag_query(query_text: str, top_communities: int = 5) -> Dict[str, Any]:
    """
    Perform Global RAG query across multiple communities for broad conceptual understanding.
    
    Args:
        query_text: Natural language query
        top_communities: Number of top communities to explore
        
    Returns:
        Dictionary with global analysis across communities
    """
    try:
        # First, do semantic search to get relevant provisions
        semantic_results = semantic_search_provisions(query_text, 10)
        
        if not semantic_results:
            return {"error": "No relevant provisions found"}
        
        # Get top communities globally
        communities_df = communities_top(top_communities)
        
        # Get provisions from these communities
        top_community_ids = communities_df['community_id'].tolist()
        community_provisions = provision_by_community(top_community_ids, 3)
        
        # Analyze each community for relevance to query
        global_analysis = {
            "query": query_text,
            "semantic_results": semantic_results[:5],
            "community_analysis": [],
            "cross_community_patterns": []
        }
        
        for community_data in community_provisions:
            community_id = community_data["community_id"]
            provisions = community_data["provisions"]
            
            # Get community info
            community_size = communities_df[communities_df['community_id'] == community_id]['size'].iloc[0]
            
            community_analysis = {
                "community_id": community_id,
                "size": community_size,
                "relevant_provisions": [],
                "summary": generate_community_summary(provisions)
            }
            
            # Add top provisions from this community
            for provision in provisions[:2]:
                community_analysis["relevant_provisions"].append({
                    "id": provision["id"],
                    "title": provision.get("title", "Unknown"),
                    "content": provision.get("content", "")[:200] + "..." if len(provision.get("content", "")) > 200 else provision.get("content", "")
                })
            
            global_analysis["community_analysis"].append(community_analysis)
        
        # Identify cross-community patterns (simplified)
        if len(global_analysis["community_analysis"]) > 1:
            global_analysis["cross_community_patterns"] = [
                "Multiple legal domains affected",
                "Broad conceptual implications",
                "Cross-jurisdictional relevance"
            ]
        
        return global_analysis
        
    except Exception as e:
        logger.error(f"Error in global RAG query: {e}")
        return {"error": str(e)}


def global_rag_communities(limit: int = 10) -> Dict[str, Any]:
    """
    Get global community structure for Global RAG.
    
    Args:
        limit: Number of top communities to return
        
    Returns:
        Dictionary with community information
    """
    try:
        communities_df = communities_top(limit)
        
        communities_with_nodes = []
        for _, row in communities_df.iterrows():
            community_id = row['community_id']
            nodes = nodes_in_community(community_id, 5)
            
            community_info = {
                "id": community_id,
                "size": row['size'],
                "node_types": row['node_types'],
                "sample_nodes": nodes,
                "summary": generate_community_summary(nodes)
            }
            communities_with_nodes.append(community_info)
        
        return {
            "communities": communities_with_nodes,
            "total_communities": len(communities_with_nodes)
        }
        
    except Exception as e:
        logger.error(f"Error in global RAG communities: {e}")
        return {"error": str(e)}


def drift_rag_query(query_text: str, as_of_date: date, 
                   top_communities: int = 3) -> Dict[str, Any]:
    """
    Perform DRIFT RAG query using community signals to guide local search.
    
    Args:
        query_text: Natural language query
        as_of_date: Date for temporal filtering
        top_communities: Number of top communities to explore
        
    Returns:
        Dictionary with fused results from multiple communities
    """
    try:
        # First, do semantic search to identify relevant provisions
        semantic_results = semantic_search_provisions(query_text, 10)
        
        if not semantic_results:
            return {"error": "No relevant provisions found"}
        
        # Extract community IDs from top semantic results
        community_ids = []
        for result in semantic_results[:5]:  # Top 5 semantic results
            provision = result.get("provision", {})
            # In practice, you'd get community ID from the provision
            # For now, we'll simulate by getting communities
            pass
        
        # Get top communities globally
        communities_df = communities_top(top_communities)
        top_community_ids = communities_df['community_id'].tolist()
        
        # Get provisions from these communities
        community_provisions = provision_by_community(top_community_ids, 2)
        
        # Run local RAG on central provisions from each community
        fused_results = {
            "query": query_text,
            "as_of_date": as_of_date.isoformat(),
            "semantic_seeds": semantic_results[:3],
            "community_results": []
        }
        
        for community_data in community_provisions:
            community_id = community_data["community_id"]
            provisions = community_data["provisions"]
            
            community_paths = []
            for provision in provisions[:1]:  # Take top provision from community
                local_result = local_rag_query(provision["id"], as_of_date)
                if "error" not in local_result:
                    community_paths.append(local_result)
            
            fused_results["community_results"].append({
                "community_id": community_id,
                "provisions_explored": len(provisions),
                "paths": community_paths
            })
        
        return fused_results
        
    except Exception as e:
        logger.error(f"Error in DRIFT RAG query: {e}")
        return {"error": str(e)}


def generate_community_summary(nodes: List[Dict[str, Any]]) -> str:
    """
    Generate a simple summary for a community based on its nodes.
    
    Args:
        nodes: List of nodes in the community
        
    Returns:
        String summary of the community
    """
    if not nodes:
        return "Empty community"
    
    # Handle different node structures - some might have 'node_type', others might have 'type'
    node_types = set()
    for node in nodes:
        if "node_type" in node:
            node_types.add(node["node_type"])
        elif "type" in node:
            node_types.add(node["type"])
        else:
            # Default to Provision if no type specified
            node_types.add("Provision")
    
    if "Provision" in node_types and "Judgment" in node_types:
        return "Legal provisions with judicial interpretations"
    elif "Provision" in node_types:
        return "Related legal provisions"
    elif "Judgment" in node_types:
        return "Related court judgments"
    else:
        return f"Mixed legal entities ({', '.join(node_types)})"


def combine_text_and_vector_search(query_text: str, k: int = 5) -> List[Dict[str, Any]]:
    """
    Combine fulltext and vector search for better recall.
    
    Args:
        query_text: Search query
        k: Number of results from each method
        
    Returns:
        Combined and deduplicated results
    """
    try:
        # Get vector search results
        vector_results = semantic_search_provisions(query_text, k)
        
        # Get fulltext search results
        text_results = search_provisions_by_text(query_text, k)
        
        # Combine and deduplicate by provision ID
        seen_ids = set()
        combined_results = []
        
        # Add vector results first (higher quality)
        for result in vector_results:
            provision_id = result["provision"]["id"]
            if provision_id not in seen_ids:
                result["search_type"] = "vector"
                combined_results.append(result)
                seen_ids.add(provision_id)
        
        # Add text results that aren't already included
        for result in text_results:
            provision_id = result["provision"]["id"]
            if provision_id not in seen_ids:
                result["search_type"] = "fulltext"
                combined_results.append(result)
                seen_ids.add(provision_id)
        
        return combined_results[:k*2]  # Return up to 2*k combined results
        
    except Exception as e:
        logger.error(f"Error in combined search: {e}")
        return []
