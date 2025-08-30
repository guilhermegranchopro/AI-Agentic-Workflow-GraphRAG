import asyncio
import sys
import os

# Add the current directory to the path
sys.path.append('.')

from app.api.routes import perform_rag_retrieval
from app.adapters.neo4j_conn import Neo4jConnection
from app.adapters.vectordb_faiss import FAISSVectorDB

async def test_citation_creation():
    print("=== Testing Citation Creation ===")
    
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
    
    print(f"RAG Result:")
    print(f"  Query: {result.query}")
    print(f"  Nodes: {len(result.nodes)}")
    print(f"  Citations: {len(result.citations)}")
    print(f"  Edges: {len(result.edges)}")
    print(f"  Coverage: {result.coverage}")
    print(f"  Confidence: {result.confidence}")
    
    if result.citations:
        print(f"\nFirst citation:")
        citation = result.citations[0]
        print(f"  Type: {type(citation)}")
        print(f"  Attributes: {dir(citation)}")
        print(f"  Dict: {citation.dict()}")
    
    if result.nodes:
        print(f"\nFirst node:")
        node = result.nodes[0]
        print(f"  Type: {type(node)}")
        print(f"  ID: {node.id}")
        print(f"  Content: {node.content[:100]}...")
        print(f"  Metadata: {node.metadata}")
    
    # Test the condition that the AI response generation uses
    has_graphrag_data = len(result.citations) > 0 and len(result.nodes) > 0
    print(f"\nHas GraphRAG data: {has_graphrag_data}")
    
    print("=== End Test ===")

if __name__ == "__main__":
    asyncio.run(test_citation_creation())
