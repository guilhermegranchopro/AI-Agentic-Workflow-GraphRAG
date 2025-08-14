"""Parameterized read-only graph queries for GraphRAG operations."""
import logging
from typing import List, Dict, Any, Optional
from datetime import date
import pandas as pd
from neo4j import Session
from src.db import db

logger = logging.getLogger(__name__)


def knn_provisions(qvec: List[float], k: int = 5) -> List[Dict[str, Any]]:
    """
    Find k nearest neighbor provisions using vector similarity.
    
    Args:
        qvec: Query vector embedding
        k: Number of neighbors to return
        
    Returns:
        List of dictionaries with provision data and similarity scores
    """
    query = """
    CALL db.index.vector.queryNodes('prov_embedding_index', $k, $qvec)
    YIELD node, score
    RETURN node { .id, .number, .text, .article_title, .instrument_id } AS provision, score
    ORDER BY score DESC
    """
    
    with db.session() as session:
        result = session.run(query, k=k, qvec=qvec)
        return [{"provision": record["provision"], "score": record["score"]} 
                for record in result]


def asof_amendments(provision_id: str, as_of: date) -> List[Dict[str, Any]]:
    """
    Find amendment events affecting a provision as of a specific date.
    
    Args:
        provision_id: ID of the provision
        as_of: Date for temporal filtering
        
    Returns:
        List of amendment events
    """
    query = """
    MATCH (p:Provision {id: $provision_id})<-[:AFFECTS]-(e:Event)
    WHERE date($as_of) >= e.valid_from 
      AND (e.valid_to IS NULL OR date($as_of) <= e.valid_to)
    RETURN e {
        .id, .kind, .description, .valid_from, .valid_to, .gazette_ref
    } AS event
    ORDER BY e.valid_from DESC
    """
    
    with db.session() as session:
        result = session.run(query, provision_id=provision_id, as_of=as_of.isoformat())
        return [record["event"] for record in result]


def asof_neighbors(provision_id: str, as_of: date, 
                   rel_types: List[str] = None) -> List[Dict[str, Any]]:
    """
    Find neighboring nodes connected to a provision via specified relationships,
    with temporal filtering for events.
    
    Args:
        provision_id: ID of the provision
        as_of: Date for temporal filtering  
        rel_types: List of relationship types to traverse
        
    Returns:
        List of paths with relationship details
    """
    if rel_types is None:
        rel_types = ['CITES', 'INTERPRETED_BY', 'AMENDED_BY', 'AFFECTS']
    
    # Build dynamic relationship pattern
    rel_pattern = '|'.join(rel_types)
    
    query = f"""
    MATCH path = (p:Provision {{id: $provision_id}})-[r:{rel_pattern}]-(n)
    WHERE NOT EXISTS {{
        MATCH (p)-[:AFFECTS|AMENDED_BY]-(e:Event)
        WHERE date($as_of) < e.valid_from 
           OR (e.valid_to IS NOT NULL AND date($as_of) > e.valid_to)
    }}
    RETURN path,
           type(r) as relationship_type,
           n {{ .id, .number, .text, .case_number, .date, .title }} as neighbor,
           r {{ .* }} as relationship_props
    LIMIT 20
    """
    
    with db.session() as session:
        result = session.run(query, provision_id=provision_id, as_of=as_of.isoformat())
        return [{
            "path": record["path"],
            "relationship_type": record["relationship_type"], 
            "neighbor": record["neighbor"],
            "relationship_props": record["relationship_props"]
        } for record in result]


def communities_top(n: int = 10) -> pd.DataFrame:
    """
    Get top N communities by size with basic statistics.
    
    Args:
        n: Number of top communities to return
        
    Returns:
        DataFrame with community statistics
    """
    query = """
    MATCH (node)
    WHERE node.communityId IS NOT NULL
    WITH node.communityId as communityId, count(node) as size,
         collect(DISTINCT labels(node)[0]) as node_types
    ORDER BY size DESC
    LIMIT $n
    RETURN communityId, size, node_types
    """
    
    with db.session() as session:
        result = session.run(query, n=n)
        data = [{
            "community_id": record["communityId"],
            "size": record["size"],
            "node_types": record["node_types"]
        } for record in result]
        return pd.DataFrame(data)


def nodes_in_community(community_id: int, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get nodes belonging to a specific community.
    
    Args:
        community_id: ID of the community
        limit: Maximum number of nodes to return
        
    Returns:
        List of nodes in the community
    """
    query = """
    MATCH (node {communityId: $community_id})
    RETURN node {
        .id, .number, .text, .title, .case_number, .date
    } as node,
    labels(node)[0] as node_type
    LIMIT $limit
    """
    
    with db.session() as session:
        result = session.run(query, community_id=community_id, limit=limit)
        return [{
            "node": record["node"],
            "node_type": record["node_type"]
        } for record in result]


def provision_by_community(community_ids: List[int], limit: int = 5) -> List[Dict[str, Any]]:
    """
    Get provisions from specific communities for DRIFT queries.
    
    Args:
        community_ids: List of community IDs to search
        limit: Maximum provisions per community
        
    Returns:
        List of provisions grouped by community
    """
    query = """
    UNWIND $community_ids as communityId
    MATCH (p:Provision {communityId: communityId})
    WITH communityId, collect(p {
        .id, .number, .text, .article_title, .instrument_id
    })[0..$limit] as provisions
    RETURN communityId, provisions
    """
    
    with db.session() as session:
        result = session.run(query, community_ids=community_ids, limit=limit)
        return [{
            "community_id": record["communityId"],
            "provisions": record["provisions"]
        } for record in result]


def search_provisions_by_text(search_text: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Search provisions using fulltext index.
    
    Args:
        search_text: Text to search for
        limit: Maximum number of results
        
    Returns:
        List of matching provisions with scores
    """
    query = """
    CALL db.index.fulltext.queryNodes('provision_text_index', $search_text)
    YIELD node, score
    RETURN node {
        .id, .number, .text, .article_title, .instrument_id
    } as provision, score
    ORDER BY score DESC
    LIMIT $limit
    """
    
    with db.session() as session:
        result = session.run(query, search_text=search_text, limit=limit)
        return [{
            "provision": record["provision"],
            "score": record["score"]
        } for record in result]


def get_provision_context(provision_id: str) -> Dict[str, Any]:
    """
    Get full context for a provision including instrument and gazette info.
    
    Args:
        provision_id: ID of the provision
        
    Returns:
        Dictionary with provision context
    """
    query = """
    MATCH (p:Provision {id: $provision_id})
    OPTIONAL MATCH (i:Instrument)-[:HAS_PROVISION]->(p)
    OPTIONAL MATCH (i)-[:PUBLISHED_IN]->(g:GazetteIssue)
    RETURN p {
        .id, .number, .text, .article_title
    } as provision,
    i {
        .id, .title, .type, .number, .year, .jurisdiction
    } as instrument,
    g {
        .id, .number, .date, .year
    } as gazette
    """
    
    with db.session() as session:
        result = session.run(query, provision_id=provision_id)
        record = result.single()
        if record:
            return {
                "provision": record["provision"],
                "instrument": record["instrument"],
                "gazette": record["gazette"]
            }
        return None
