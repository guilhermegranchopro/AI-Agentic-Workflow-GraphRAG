import asyncio
from typing import List, Dict, Any, Optional
from neo4j import AsyncGraphDatabase
from tenacity import retry, stop_after_attempt, wait_exponential
from loguru import logger
from ..schemas.config import settings


class Neo4jConnection:
    """Async Neo4j connection manager with retry logic."""
    
    def __init__(self):
        """Initialize Neo4j connection."""
        if not all([settings.neo4j_uri, settings.neo4j_username, settings.neo4j_password]):
            logger.warning("Neo4j credentials not configured")
            self.driver = None
            return
            
        self.driver = AsyncGraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_username, settings.neo4j_password)
        )
        
    async def verify_connectivity(self) -> bool:
        """Verify Neo4j connection."""
        if not self.driver:
            return False
            
        try:
            await self.driver.verify_connectivity()
            return True
        except Exception as e:
            logger.error(f"Neo4j connectivity check failed: {e}")
            return False
            
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    async def run_cypher(
        self,
        query: str,
        parameters: Optional[Dict[str, Any]] = None,
        timeout: int = 30
    ) -> List[Dict[str, Any]]:
        """Execute Cypher query with retry logic."""
        if not self.driver:
            raise ValueError("Neo4j driver not configured")
            
        try:
            async with self.driver.session() as session:
                result = await asyncio.wait_for(
                    session.run(query, parameters or {}),
                    timeout=timeout
                )
                records = await result.data()
                return records
        except Exception as e:
            logger.error(f"Neo4j query error: {e}")
            raise
            
    async def get_graph_stats(self) -> Dict[str, Any]:
        """Get Neo4j graph statistics."""
        if not self.driver:
            return {"error": "Neo4j not configured"}
            
        try:
            # Get node counts by type
            node_query = """
            MATCH (n)
            RETURN labels(n) as labels, count(n) as count
            """
            node_stats = await self.run_cypher(node_query)
            
            # Get relationship counts by type
            rel_query = """
            MATCH ()-[r]->()
            RETURN type(r) as type, count(r) as count
            """
            rel_stats = await self.run_cypher(rel_query)
            
            # Get total counts
            total_nodes = sum(stat["count"] for stat in node_stats)
            total_rels = sum(stat["count"] for stat in rel_stats)
            
            return {
                "total_nodes": total_nodes,
                "total_relationships": total_rels,
                "node_types": {stat["labels"][0] if stat["labels"] else "unlabeled": stat["count"] for stat in node_stats},
                "relationship_types": {stat["type"]: stat["count"] for stat in rel_stats}
            }
        except Exception as e:
            logger.error(f"Failed to get graph stats: {e}")
            return {"error": str(e)}
            
    async def health_check(self) -> Dict[str, Any]:
        """Check Neo4j service health."""
        if not self.driver:
            return {"status": "not_configured", "error": "Credentials missing"}
            
        try:
            is_connected = await self.verify_connectivity()
            if is_connected:
                stats = await self.get_graph_stats()
                return {"status": "healthy", "stats": stats}
            else:
                return {"status": "unhealthy", "error": "Connection failed"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
            
    async def close(self):
        """Close Neo4j connection."""
        if self.driver:
            await self.driver.close()
