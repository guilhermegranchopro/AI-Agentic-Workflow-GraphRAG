import asyncio
import sys
import os

# Add the current directory to the path
sys.path.append('.')

from app.adapters.neo4j_conn import Neo4jConnection

async def test_specific_queries():
    print("=== Testing Specific Queries ===")
    
    conn = Neo4jConnection()
    
    # Test with the exact node we found
    print("Testing with exact node...")
    exact_query = """
    MATCH (n:LegalNode {id: 'corporate_tax_amendment_2024'})
    RETURN n.title, n.content
    """
    
    exact_result = await conn.run_cypher(exact_query)
    if exact_result:
        node = exact_result[0]
        print(f"Title: {node['n.title']}")
        print(f"Content: {node['n.content'][:100]}...")
    
    # Test with different search patterns
    print("\nTesting different search patterns...")
    
    # Test 1: Simple CONTAINS
    test1_query = """
    MATCH (n:LegalNode)
    WHERE n.title CONTAINS 'Corporate Tax'
    RETURN n.title, n.id
    """
    
    test1_result = await conn.run_cypher(test1_query)
    print(f"Test 1 (CONTAINS): {len(test1_result)} nodes")
    
    # Test 2: toLower CONTAINS
    test2_query = """
    MATCH (n:LegalNode)
    WHERE toLower(n.title) CONTAINS toLower('Corporate Tax')
    RETURN n.title, n.id
    """
    
    test2_result = await conn.run_cypher(test2_query)
    print(f"Test 2 (toLower CONTAINS): {len(test2_result)} nodes")
    
    # Test 3: Content search
    test3_query = """
    MATCH (n:LegalNode)
    WHERE n.content CONTAINS 'Corporate Tax'
    RETURN n.title, n.id
    """
    
    test3_result = await conn.run_cypher(test3_query)
    print(f"Test 3 (Content CONTAINS): {len(test3_result)} nodes")
    
    # Test 4: ID search
    test4_query = """
    MATCH (n:LegalNode)
    WHERE n.id CONTAINS 'corporate_tax'
    RETURN n.title, n.id
    """
    
    test4_result = await conn.run_cypher(test4_query)
    print(f"Test 4 (ID CONTAINS): {len(test4_result)} nodes")
    
    # Show all results
    print("\nAll matching nodes:")
    for record in test4_result:
        print(f"  - {record['n.title']} ({record['n.id']})")
    
    print("=== End Test ===")

if __name__ == "__main__":
    asyncio.run(test_specific_queries())
