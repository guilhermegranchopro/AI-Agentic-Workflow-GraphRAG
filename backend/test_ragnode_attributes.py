import asyncio
import sys
import os

# Add the current directory to the path
sys.path.append('.')

from app.api.routes import perform_rag_retrieval
from app.adapters.neo4j_conn import Neo4jConnection
from app.adapters.vectordb_faiss import FAISSVectorDB

async def test_ragnode_attributes():
    print("=== Testing RAGNode Attributes ===")
    
    # Initialize services
    neo4j_conn = Neo4jConnection()
    faiss_db = FAISSVectorDB()
    
    # Test with a simple query
    result = await perform_rag_retrieval(
        query="Corporate Tax",
        strategy="auto",
        max_results=3,
        neo4j_conn=neo4j_conn,
        faiss_db=faiss_db
    )
    
    if result.nodes:
        print(f"Found {len(result.nodes)} nodes")
        
        # Check the first node
        node = result.nodes[0]
        print(f"\nFirst node type: {type(node)}")
        print(f"First node attributes: {dir(node)}")
        print(f"First node dict: {node.dict()}")
        
        # Check what attributes are available
        print(f"\nAvailable attributes:")
        for attr in dir(node):
            if not attr.startswith('_'):
                try:
                    value = getattr(node, attr)
                    if not callable(value):
                        print(f"  {attr}: {value}")
                except:
                    pass
    
    print("=== End Test ===")

if __name__ == "__main__":
    asyncio.run(test_ragnode_attributes())
