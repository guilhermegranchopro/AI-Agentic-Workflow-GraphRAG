from abc import ABC, abstractmethod
from typing import List, Dict, Any
from loguru import logger
from ..schemas.rag import RAGResult, RAGNode, RAGEdge, RAGCitation
from ..schemas.a2a import RAGNode as A2ARAGNode, RAGEdge as A2ARAGEdge, RAGCitation as A2ARAGCitation
from ..adapters.neo4j_conn import Neo4jConnection


class GraphRAGBase(ABC):
    """Abstract base class for GraphRAG implementations."""
    
    def __init__(self, neo4j_conn: Neo4jConnection):
        """Initialize GraphRAG with Neo4j connection."""
        self.neo4j_conn = neo4j_conn
        
    @abstractmethod
    async def retrieve(self, query: str, max_results: int = 10) -> RAGResult:
        """Retrieve relevant nodes and edges from the knowledge graph."""
        pass
        
    def _create_rag_node(self, node_data: Dict[str, Any]) -> RAGNode:
        """Create RAG node from Neo4j data."""
        return RAGNode(
            id=str(node_data.get("id", "")),
            type=node_data.get("type", "unknown"),
            content=node_data.get("content", ""),
            metadata=node_data.get("metadata", {}),
            score=node_data.get("score", 0.0)
        )
        
    def _create_rag_edge(self, edge_data: Dict[str, Any]) -> RAGEdge:
        """Create RAG edge from Neo4j data."""
        return RAGEdge(
            source=str(edge_data.get("source", "")),
            target=str(edge_data.get("target", "")),
            type=edge_data.get("type", "unknown"),
            weight=edge_data.get("weight", 1.0),
            metadata=edge_data.get("metadata", {})
        )
        
    def _create_rag_citation(self, node_data: Dict[str, Any], score: float) -> RAGCitation:
        """Create RAG citation from node data."""
        return RAGCitation(
            node_id=str(node_data.get("id", "")),
            node_type=node_data.get("type", "unknown"),
            content=node_data.get("content", ""),
            score=score,
            metadata=node_data.get("metadata", {})
        )
        
    def _calculate_coverage(self, nodes: List[RAGNode], total_nodes: int) -> float:
        """Calculate knowledge graph coverage."""
        if total_nodes == 0:
            return 0.0
        return len(nodes) / total_nodes


class LocalGraphRAG(GraphRAGBase):
    """Local GraphRAG implementation for focused retrieval."""
    
    async def retrieve(self, query: str, max_results: int = 10) -> RAGResult:
        """Retrieve nodes and edges using local graph traversal."""
        try:
            # Cypher query for local graph traversal
            cypher_query = """
            MATCH (n)
            WHERE n.content CONTAINS $query OR n.title CONTAINS $query
            WITH n, size((n)-[]-()) as degree
            ORDER BY degree DESC, n.score DESC
            LIMIT $max_results
            OPTIONAL MATCH (n)-[r]-(related)
            WHERE related IN [(n)-[]-() | endNode(relationships())]
            RETURN DISTINCT n, r, related
            """
            
            params = {"query": query, "max_results": max_results}
            results = await self.neo4j_conn.run_cypher(cypher_query, params)
            
            nodes = []
            edges = []
            citations = []
            
            for record in results:
                if "n" in record and record["n"]:
                    node = self._create_rag_node(record["n"])
                    nodes.append(node)
                    citations.append(self._create_rag_citation(record["n"], node.score or 0.0))
                    
                if "r" in record and record["r"] and "related" in record and record["related"]:
                    edge = self._create_rag_edge({
                        "source": record["r"].get("start_node", ""),
                        "target": record["r"].get("end_node", ""),
                        "type": record["r"].get("type", ""),
                        "weight": record["r"].get("weight", 1.0),
                        "metadata": record["r"].get("properties", {})
                    })
                    edges.append(edge)
            
            # Get total node count for coverage calculation
            total_query = "MATCH (n) RETURN count(n) as total"
            total_result = await self.neo4j_conn.run_cypher(total_query)
            total_nodes = total_result[0]["total"] if total_result else 0
            
            return RAGResult(
                query=query,
                nodes=nodes,
                edges=edges,
                citations=citations,
                coverage=self._calculate_coverage(nodes, total_nodes),
                confidence=sum(node.score or 0.0 for node in nodes) / len(nodes) if nodes else 0.0
            )
            
        except Exception as e:
            logger.error(f"Local GraphRAG retrieval error: {e}")
            return RAGResult(query=query)


class GlobalGraphRAG(GraphRAGBase):
    """Global GraphRAG implementation for comprehensive retrieval."""
    
    async def retrieve(self, query: str, max_results: int = 10) -> RAGResult:
        """Retrieve nodes and edges using global graph analysis."""
        try:
            # Cypher query for global graph analysis
            cypher_query = """
            MATCH (n)
            WHERE n.content CONTAINS $query OR n.title CONTAINS $query
            WITH n, 
                 size((n)-[]-()) as degree,
                 n.score as relevance
            ORDER BY relevance DESC, degree DESC
            LIMIT $max_results
            MATCH (n)-[r*1..2]-(related)
            WHERE related <> n
            WITH n, r, related, 
                 reduce(score = 0, rel in r | score + rel.weight) as path_score
            ORDER BY path_score DESC
            RETURN DISTINCT n, r, related, path_score
            """
            
            params = {"query": query, "max_results": max_results}
            results = await self.neo4j_conn.run_cypher(cypher_query, params)
            
            nodes = []
            edges = []
            citations = []
            
            for record in results:
                if "n" in record and record["n"]:
                    node = self._create_rag_node(record["n"])
                    nodes.append(node)
                    citations.append(self._create_rag_citation(record["n"], node.score or 0.0))
                    
                if "r" in record and record["r"]:
                    # Handle path relationships
                    for rel in record["r"]:
                        edge = self._create_rag_edge({
                            "source": rel.get("start_node", ""),
                            "target": rel.get("end_node", ""),
                            "type": rel.get("type", ""),
                            "weight": rel.get("weight", 1.0),
                            "metadata": rel.get("properties", {})
                        })
                        edges.append(edge)
            
            # Get total node count for coverage calculation
            total_query = "MATCH (n) RETURN count(n) as total"
            total_result = await self.neo4j_conn.run_cypher(total_query)
            total_nodes = total_result[0]["total"] if total_result else 0
            
            return RAGResult(
                query=query,
                nodes=nodes,
                edges=edges,
                citations=citations,
                coverage=self._calculate_coverage(nodes, total_nodes),
                confidence=sum(node.score or 0.0 for node in nodes) / len(nodes) if nodes else 0.0
            )
            
        except Exception as e:
            logger.error(f"Global GraphRAG retrieval error: {e}")
            return RAGResult(query=query)


class DRIFTGraphRAG(GraphRAGBase):
    """DRIFT GraphRAG implementation for dynamic retrieval."""
    
    async def retrieve(self, query: str, max_results: int = 10) -> RAGResult:
        """Retrieve nodes and edges using DRIFT algorithm."""
        try:
            # Cypher query for DRIFT retrieval
            cypher_query = """
            MATCH (n)
            WHERE n.content CONTAINS $query OR n.title CONTAINS $query
            WITH n, 
                 size((n)-[]-()) as degree,
                 n.score as relevance,
                 n.timestamp as recency
            ORDER BY relevance DESC, recency DESC, degree DESC
            LIMIT $max_results
            MATCH (n)-[r]-(related)
            WHERE related IN [(n)-[]-() | endNode(relationships())]
            WITH n, r, related,
                 n.relevance * (1 + 0.1 * log10(degree)) as drift_score
            ORDER BY drift_score DESC
            RETURN DISTINCT n, r, related, drift_score
            """
            
            params = {"query": query, "max_results": max_results}
            results = await self.neo4j_conn.run_cypher(cypher_query, params)
            
            nodes = []
            edges = []
            citations = []
            
            for record in results:
                if "n" in record and record["n"]:
                    node = self._create_rag_node(record["n"])
                    nodes.append(node)
                    citations.append(self._create_rag_citation(record["n"], node.score or 0.0))
                    
                if "r" in record and record["r"] and "related" in record and record["related"]:
                    edge = self._create_rag_edge({
                        "source": record["r"].get("start_node", ""),
                        "target": record["r"].get("end_node", ""),
                        "type": record["r"].get("type", ""),
                        "weight": record["r"].get("weight", 1.0),
                        "metadata": record["r"].get("properties", {})
                    })
                    edges.append(edge)
            
            # Get total node count for coverage calculation
            total_query = "MATCH (n) RETURN count(n) as total"
            total_result = await self.neo4j_conn.run_cypher(total_query)
            total_nodes = total_result[0]["total"] if total_result else 0
            
            return RAGResult(
                query=query,
                nodes=nodes,
                edges=edges,
                citations=citations,
                coverage=self._calculate_coverage(nodes, total_nodes),
                confidence=sum(node.score or 0.0 for node in nodes) / len(nodes) if nodes else 0.0
            )
            
        except Exception as e:
            logger.error(f"DRIFT GraphRAG retrieval error: {e}")
            return RAGResult(query=query)
