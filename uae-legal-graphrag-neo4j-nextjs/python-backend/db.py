"""Neo4j database connection and session management."""
from contextlib import contextmanager
from typing import Generator, Any
import logging
import ssl
from neo4j import GraphDatabase, Driver, Session
from src.config import settings

logger = logging.getLogger(__name__)


class Neo4jDatabase:
    """Neo4j database connection manager."""
    
    def __init__(self):
        self._driver: Driver = None
        
    def connect(self) -> None:
        """Initialize the Neo4j driver."""
        try:
            # Handle AuraDB SSL issues (demo mode)
            if "bolt+s://" in settings.neo4j_uri:
                logger.warning("Using insecure SSL mode for AuraDB demo")
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                plain_uri = settings.neo4j_uri.replace("bolt+s://", "bolt://")
                self._driver = GraphDatabase.driver(
                    plain_uri,
                    auth=(settings.neo4j_user, settings.neo4j_password),
                    encrypted=True,
                    ssl_context=ssl_context
                )
            else:
                self._driver = GraphDatabase.driver(
                    settings.neo4j_uri,
                    auth=(settings.neo4j_user, settings.neo4j_password)
                )
            
            # Test connection
            with self._driver.session(database=settings.neo4j_database) as session:
                session.run("RETURN 1")
            logger.info("Successfully connected to Neo4j")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise
    
    def close(self) -> None:
        """Close the Neo4j driver."""
        if self._driver:
            self._driver.close()
            logger.info("Neo4j connection closed")
    
    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        """Context manager for Neo4j sessions."""
        if not self._driver:
            self.connect()
        
        session = self._driver.session()
        try:
            yield session
        finally:
            session.close()
    
    def health_check(self) -> dict[str, Any]:
        """Perform health check and return status information."""
        try:
            with self.session() as session:
                # Basic connectivity
                result = session.run("RETURN 1 as status")
                status = result.single()["status"]
                
                # Count nodes
                result = session.run("MATCH (n) RETURN count(n) as node_count")
                node_count = result.single()["node_count"]
                
                # Check for vector index
                result = session.run("SHOW INDEXES YIELD name WHERE name = 'prov_embedding_index'")
                vector_index_exists = len(list(result)) > 0
                
                # Check for GDS community properties
                result = session.run(
                    "MATCH (p:Provision) WHERE p.communityId IS NOT NULL RETURN count(p) as community_nodes"
                )
                community_nodes = result.single()["community_nodes"]
                
                return {
                    "status": "healthy",
                    "connected": True,
                    "node_count": node_count,
                    "vector_index_exists": vector_index_exists,
                    "community_nodes": community_nodes
                }
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "unhealthy",
                "connected": False,
                "error": str(e)
            }


# Global database instance
db = Neo4jDatabase()
