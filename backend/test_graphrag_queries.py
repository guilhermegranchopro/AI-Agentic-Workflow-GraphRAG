import asyncio
import sys
import os

# Add the current directory to the path
sys.path.append('.')

from app.adapters.neo4j_conn import Neo4jConnection

async def test_graphrag_queries():
    print("=== Testing GraphRAG Queries ===")
    
    conn = Neo4jConnection()
    
    # Test the Local GraphRAG query
    print("Testing Local GraphRAG query...")
    local_query = """
    MATCH (n:LegalNode)
    WHERE toLower(n.content) CONTAINS toLower('Corporate Tax Law 2022') 
       OR toLower(n.title) CONTAINS toLower('Corporate Tax Law 2022')
    WITH n, 
         size([(n)-[]-() | 1]) as degree
    ORDER BY degree DESC
    LIMIT 10
    RETURN n, degree
    """
    
    local_result = await conn.run_cypher(local_query)
    print(f"Local GraphRAG found {len(local_result)} nodes")
    
    for record in local_result[:3]:  # Show first 3 results
        node = record["n"]
        degree = record["degree"]
        print(f"  - {node['title']} (degree: {degree})")
    
    # Test the Global GraphRAG query
    print("\nTesting Global GraphRAG query...")
    global_query = """
    MATCH (n:LegalNode)
    WHERE toLower(n.content) CONTAINS toLower('Corporate Tax Law 2022') 
       OR toLower(n.title) CONTAINS toLower('Corporate Tax Law 2022')
       OR toLower(n.content) CONTAINS toLower('Corporate Tax Law')
    WITH n, 
         size([(n)-[]-() | 1]) as degree
    ORDER BY degree DESC
    LIMIT 10
    MATCH (n)-[r*1..2]-(related)
    WHERE related <> n
    WITH n, r, related
    ORDER BY degree DESC
    RETURN DISTINCT n, r, related
    """
    
    global_result = await conn.run_cypher(global_query)
    print(f"Global GraphRAG found {len(global_result)} records")
    
    # Test a simple search
    print("\nTesting simple search...")
    simple_query = """
    MATCH (n:LegalNode)
    WHERE n.title CONTAINS 'Corporate Tax'
    RETURN n.title, n.id
    LIMIT 5
    """
    
    simple_result = await conn.run_cypher(simple_query)
    print(f"Simple search found {len(simple_result)} nodes")
    
    for record in simple_result:
        print(f"  - {record['n.title']} ({record['n.id']})")
    
    print("=== End Test ===")

if __name__ == "__main__":
    asyncio.run(test_graphrag_queries())
