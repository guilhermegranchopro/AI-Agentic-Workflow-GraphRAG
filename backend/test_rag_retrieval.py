import asyncio
import sys
import os

# Add the current directory to the path
sys.path.append('.')

from app.api.routes import perform_rag_retrieval
from app.adapters.neo4j_conn import Neo4jConnection
from app.adapters.vectordb_faiss import FAISSVectorDB

async def test_rag_retrieval():
    print("=== Testing RAG Retrieval ===")
    
    # Initialize services
    neo4j_conn = Neo4jConnection()
    faiss_db = FAISSVectorDB()
    
    # Test different queries
    test_queries = [
        "Corporate Tax",
        "Corporate Tax Law 2022", 
        "UAE Court System",
        "Data Protection"
    ]
    
    for query in test_queries:
        print(f"\nTesting query: '{query}'")
        try:
            result = await perform_rag_retrieval(
                query=query,
                strategy="auto",
                max_results=10,
                neo4j_conn=neo4j_conn,
                faiss_db=faiss_db
            )
            
            print(f"  Strategy: {result.strategy}")
            print(f"  Nodes found: {len(result.nodes)}")
            print(f"  Citations found: {len(result.citations)}")
            print(f"  Coverage: {result.coverage}")
            print(f"  Confidence: {result.confidence}")
            
            if result.nodes:
                print("  Sample nodes:")
                for node in result.nodes[:3]:
                    print(f"    - {node.title}")
            
        except Exception as e:
            print(f"  Error: {e}")
    
    print("=== End Test ===")

if __name__ == "__main__":
    asyncio.run(test_rag_retrieval())
