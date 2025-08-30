import asyncio
import sys
import os

# Add the current directory to the path
sys.path.append('.')

from app.adapters.neo4j_conn import Neo4jConnection

async def test_node_properties():
    print("=== Testing Node Properties ===")
    
    conn = Neo4jConnection()
    
    # Get a sample node to see its properties
    query = "MATCH (n:LegalNode) RETURN n LIMIT 1"
    result = await conn.run_cypher(query)
    
    if result:
        node = result[0]["n"]
        print(f"Sample node: {node}")
        print(f"Node properties: {node.keys()}")
        
        # Check if nodes have content and title properties
        content_query = "MATCH (n:LegalNode) WHERE n.content IS NOT NULL RETURN count(n) as count"
        title_query = "MATCH (n:LegalNode) WHERE n.title IS NOT NULL RETURN count(n) as count"
        
        content_result = await conn.run_cypher(content_query)
        title_result = await conn.run_cypher(title_query)
        
        print(f"Nodes with content: {content_result[0]['count'] if content_result else 0}")
        print(f"Nodes with title: {title_result[0]['count'] if title_result else 0}")
        
        # Get all unique property keys
        props_query = "MATCH (n:LegalNode) RETURN keys(n) as keys LIMIT 5"
        props_result = await conn.run_cypher(props_query)
        
        print("Sample property keys:")
        for record in props_result:
            print(f"  {record['keys']}")
    
    print("=== End Test ===")

if __name__ == "__main__":
    asyncio.run(test_node_properties())
