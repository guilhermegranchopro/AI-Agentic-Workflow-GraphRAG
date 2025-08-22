"""
Advanced GraphRAG implementation with semantic search and graph algorithms
"""

import asyncio
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from sentence_transformers import SentenceTransformer
import networkx as nx
from neo4j import AsyncGraphDatabase
import community as community_louvain
from datetime import datetime
import logging

from app.config import settings

logger = logging.getLogger(__name__)

class AdvancedGraphRAG:
    """
    Advanced GraphRAG with semantic embeddings, community detection,
    and sophisticated graph algorithms for legal research
    """
    
    def __init__(self):
        self.embedding_model = None
        self.legal_embedding_model = None
        self.driver = None
        self.graph_cache = {}
        
    async def initialize(self):
        """Initialize models and database connections"""
        try:
            # Initialize embedding models
            self.embedding_model = SentenceTransformer(settings.embedding_model)
            self.legal_embedding_model = SentenceTransformer(settings.legal_embedding_model)
            
            # Initialize Neo4j driver
            self.driver = AsyncGraphDatabase.driver(
                settings.neo4j_uri,
                auth=(settings.neo4j_user, settings.neo4j_password)
            )
            
            logger.info("AdvancedGraphRAG initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize AdvancedGraphRAG: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Check if all services are healthy"""
        try:
            if not self.driver:
                await self.initialize()
            
            async with self.driver.session(database=settings.neo4j_database) as session:
                result = await session.run("RETURN 1 as health")
                await result.single()
                return True
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    async def advanced_retrieve(
        self, 
        query: str, 
        mode: str = "hybrid",
        max_results: int = 10,
        include_metadata: bool = True
    ) -> Dict[str, Any]:
        """
        Advanced retrieval with semantic search and graph algorithms
        """
        if not self.driver:
            await self.initialize()
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query)
        
        if mode == "local":
            return await self._semantic_local_search(query, query_embedding, max_results)
        elif mode == "global":
            return await self._community_based_search(query, query_embedding, max_results)
        elif mode == "drift":
            return await self._temporal_drift_analysis(query, query_embedding, max_results)
        elif mode == "hybrid":
            return await self._hybrid_search(query, query_embedding, max_results)
        else:
            raise ValueError(f"Unsupported mode: {mode}")
    
    async def _semantic_local_search(
        self, 
        query: str, 
        query_embedding: np.ndarray, 
        max_results: int
    ) -> Dict[str, Any]:
        """
        Semantic local search using embeddings and local graph structure
        """
        cypher = """
        // Get nodes with text content
        MATCH (n)
        WHERE n.text IS NOT NULL OR n.title IS NOT NULL OR n.description IS NOT NULL
        WITH n, 
             COALESCE(n.text, n.title, n.description, '') as content,
             COALESCE(n.embedding, []) as stored_embedding
        WHERE size(content) > 10
        
        // Get local neighborhood
        OPTIONAL MATCH (n)-[r]-(neighbor)
        WHERE neighbor.text IS NOT NULL OR neighbor.title IS NOT NULL
        
        RETURN 
            elementId(n) as nodeId,
            content,
            labels(n) as labels,
            properties(n) as properties,
            stored_embedding,
            collect(DISTINCT {
                id: elementId(neighbor),
                type: type(r),
                content: COALESCE(neighbor.text, neighbor.title, neighbor.description, '')
            }) as neighbors
        LIMIT $max_results * 2
        """
        
        async with self.driver.session(database=settings.neo4j_database) as session:
            result = await session.run(cypher, max_results=max_results)
            records = await result.data()
        
        # Calculate semantic similarities
        scored_results = []
        for record in records:
            content = record['content']
            if not content:
                continue
                
            # Calculate semantic similarity
            content_embedding = self.embedding_model.encode(content)
            similarity = np.dot(query_embedding, content_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(content_embedding)
            )
            
            # Boost score based on neighborhood relevance
            neighbor_boost = 0
            for neighbor in record['neighbors']:
                if neighbor['content'] and query.lower() in neighbor['content'].lower():
                    neighbor_boost += 0.1
            
            final_score = similarity + min(neighbor_boost, 0.3)
            
            scored_results.append({
                'text': content,
                'nodeId': record['nodeId'],
                'score': float(final_score),
                'metadata': {
                    'labels': record['labels'],
                    'properties': record['properties'],
                    'neighbors_count': len(record['neighbors']),
                    'semantic_similarity': float(similarity)
                }
            })
        
        # Sort by score and return top results
        scored_results.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'passages': scored_results[:max_results],
            'retrieval_mode': 'semantic_local',
            'total_candidates': len(records),
            'query_embedding_shape': query_embedding.shape
        }
    
    async def _community_based_search(
        self, 
        query: str, 
        query_embedding: np.ndarray, 
        max_results: int
    ) -> Dict[str, Any]:
        """
        Community-based search using graph structure and semantic similarity
        """
        # First, get the full graph structure
        graph_data = await self._get_graph_structure()
        
        # Build NetworkX graph
        G = nx.Graph()
        for edge in graph_data['edges']:
            G.add_edge(edge['source'], edge['target'])
        
        # Detect communities
        communities = community_louvain.best_partition(G)
        
        # Find relevant communities based on query
        community_scores = {}
        node_content_map = {node['id']: node.get('content', '') for node in graph_data['nodes']}
        
        for node_id, community_id in communities.items():
            if community_id not in community_scores:
                community_scores[community_id] = []
            
            content = node_content_map.get(node_id, '')
            if content:
                content_embedding = self.embedding_model.encode(content)
                similarity = np.dot(query_embedding, content_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(content_embedding)
                )
                community_scores[community_id].append((node_id, content, similarity))
        
        # Get best results from top communities
        results = []
        for community_id, nodes in community_scores.items():
            if not nodes:
                continue
                
            # Sort nodes in community by similarity
            nodes.sort(key=lambda x: x[2], reverse=True)
            
            # Add top nodes from this community
            for node_id, content, similarity in nodes[:3]:  # Top 3 per community
                results.append({
                    'text': content,
                    'nodeId': node_id,
                    'score': float(similarity),
                    'metadata': {
                        'community_id': community_id,
                        'community_size': len(community_scores[community_id]),
                        'semantic_similarity': float(similarity)
                    }
                })
        
        # Sort all results by score
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'passages': results[:max_results],
            'retrieval_mode': 'community_based',
            'communities_found': len(community_scores),
            'total_nodes': len(G.nodes())
        }
    
    async def _temporal_drift_analysis(
        self, 
        query: str, 
        query_embedding: np.ndarray, 
        max_results: int
    ) -> Dict[str, Any]:
        """
        Temporal drift analysis for legal concept evolution
        """
        cypher = """
        // Find nodes with temporal information
        MATCH (n)
        WHERE (n.date IS NOT NULL OR n.year IS NOT NULL OR n.timestamp IS NOT NULL)
          AND (n.text IS NOT NULL OR n.title IS NOT NULL)
        WITH n,
             COALESCE(n.text, n.title, n.description, '') as content,
             COALESCE(n.date, n.year, n.timestamp, '') as temporal_info
        WHERE size(content) > 10
        
        // Find related concepts across time
        OPTIONAL MATCH (n)-[:SUPERSEDES|AMENDS|RELATES_TO*1..2]-(related)
        WHERE related.text IS NOT NULL
        
        RETURN 
            elementId(n) as nodeId,
            content,
            temporal_info,
            labels(n) as labels,
            properties(n) as properties,
            collect(DISTINCT {
                id: elementId(related),
                content: COALESCE(related.text, related.title, ''),
                temporal: COALESCE(related.date, related.year, related.timestamp, '')
            }) as related_concepts
        ORDER BY temporal_info DESC
        LIMIT $max_results * 3
        """
        
        async with self.driver.session(database=settings.neo4j_database) as session:
            result = await session.run(cypher, max_results=max_results)
            records = await result.data()
        
        # Analyze temporal evolution patterns
        scored_results = []
        for record in records:
            content = record['content']
            if not content:
                continue
            
            # Calculate semantic similarity
            content_embedding = self.embedding_model.encode(content)
            similarity = np.dot(query_embedding, content_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(content_embedding)
            )
            
            # Analyze evolution patterns
            evolution_score = 0
            for related in record['related_concepts']:
                if related['content'] and query.lower() in related['content'].lower():
                    evolution_score += 0.1
            
            # Temporal relevance (newer gets slight boost)
            temporal_boost = 0
            if record['temporal_info']:
                try:
                    # Simple year extraction for demonstration
                    year_str = str(record['temporal_info'])
                    if any(char.isdigit() for char in year_str):
                        # Boost recent documents slightly
                        temporal_boost = 0.05
                except:
                    pass
            
            final_score = similarity + evolution_score + temporal_boost
            
            scored_results.append({
                'text': content,
                'nodeId': record['nodeId'],
                'score': float(final_score),
                'metadata': {
                    'labels': record['labels'],
                    'properties': record['properties'],
                    'temporal_info': record['temporal_info'],
                    'evolution_connections': len(record['related_concepts']),
                    'semantic_similarity': float(similarity)
                }
            })
        
        # Sort by score
        scored_results.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'passages': scored_results[:max_results],
            'retrieval_mode': 'temporal_drift',
            'temporal_patterns_found': len([r for r in records if r['temporal_info']]),
            'evolution_connections': sum(len(r['related_concepts']) for r in records)
        }
    
    async def _hybrid_search(
        self, 
        query: str, 
        query_embedding: np.ndarray, 
        max_results: int
    ) -> Dict[str, Any]:
        """
        Hybrid search combining all methods
        """
        # Run all search methods in parallel
        local_task = self._semantic_local_search(query, query_embedding, max_results // 3)
        community_task = self._community_based_search(query, query_embedding, max_results // 3)
        drift_task = self._temporal_drift_analysis(query, query_embedding, max_results // 3)
        
        local_results, community_results, drift_results = await asyncio.gather(
            local_task, community_task, drift_task
        )
        
        # Combine and deduplicate results
        all_passages = []
        seen_node_ids = set()
        
        # Add results from each method with method-specific boosts
        for passages, boost in [
            (local_results['passages'], 1.0),
            (community_results['passages'], 0.9),
            (drift_results['passages'], 0.8)
        ]:
            for passage in passages:
                if passage['nodeId'] not in seen_node_ids:
                    passage['score'] *= boost
                    all_passages.append(passage)
                    seen_node_ids.add(passage['nodeId'])
        
        # Sort combined results
        all_passages.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'passages': all_passages[:max_results],
            'retrieval_mode': 'hybrid',
            'methods_used': ['semantic_local', 'community_based', 'temporal_drift'],
            'total_unique_results': len(all_passages)
        }
    
    async def _get_graph_structure(self) -> Dict[str, Any]:
        """Get graph structure for community detection"""
        if 'graph_structure' in self.graph_cache:
            return self.graph_cache['graph_structure']
        
        cypher = """
        MATCH (n)-[r]->(m)
        WHERE n.text IS NOT NULL OR n.title IS NOT NULL
        RETURN 
            elementId(n) as source,
            elementId(m) as target,
            type(r) as relationship_type,
            COALESCE(n.text, n.title, n.description, '') as source_content,
            COALESCE(m.text, m.title, m.description, '') as target_content
        LIMIT 1000
        """
        
        async with self.driver.session(database=settings.neo4j_database) as session:
            result = await session.run(cypher)
            records = await result.data()
        
        nodes = {}
        edges = []
        
        for record in records:
            source_id = record['source']
            target_id = record['target']
            
            # Add nodes
            nodes[source_id] = {
                'id': source_id,
                'content': record['source_content']
            }
            nodes[target_id] = {
                'id': target_id,
                'content': record['target_content']
            }
            
            # Add edge
            edges.append({
                'source': source_id,
                'target': target_id,
                'type': record['relationship_type']
            })
        
        graph_data = {
            'nodes': list(nodes.values()),
            'edges': edges
        }
        
        # Cache for 5 minutes
        self.graph_cache['graph_structure'] = graph_data
        
        return graph_data
    
    async def get_advanced_graph_data(
        self,
        query: Optional[str] = None,
        node_types: Optional[List[str]] = None,
        max_nodes: int = 100
    ) -> Dict[str, Any]:
        """
        Get graph data with community detection and semantic clustering
        """
        graph_data = await self._get_graph_structure()
        
        # Build NetworkX graph for analysis
        G = nx.Graph()
        for edge in graph_data['edges'][:max_nodes]:
            G.add_edge(edge['source'], edge['target'])
        
        # Community detection
        communities = community_louvain.best_partition(G)
        
        # Add community information to nodes
        enhanced_nodes = []
        for node in graph_data['nodes'][:max_nodes]:
            node_id = node['id']
            enhanced_node = {
                **node,
                'community': communities.get(node_id, 0),
                'degree': G.degree(node_id) if node_id in G else 0
            }
            enhanced_nodes.append(enhanced_node)
        
        return {
            'nodes': enhanced_nodes,
            'edges': graph_data['edges'][:max_nodes],
            'communities': len(set(communities.values())),
            'graph_metrics': {
                'total_nodes': len(G.nodes()),
                'total_edges': len(G.edges()),
                'average_clustering': nx.average_clustering(G) if len(G) > 0 else 0,
                'density': nx.density(G) if len(G) > 0 else 0
            }
        }
    
    async def close(self):
        """Close database connections"""
        if self.driver:
            await self.driver.close()
