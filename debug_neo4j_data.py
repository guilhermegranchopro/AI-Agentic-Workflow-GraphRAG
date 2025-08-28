#!/usr/bin/env python3
"""
Debug script to check Neo4j data and queries
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def debug_neo4j_data():
    """Debug Neo4j data and queries."""
    print("🔍 Debugging Neo4j Data and Queries")
    print("=" * 40)
    
    try:
        from backend.app.adapters.neo4j_conn import Neo4jConnection
        neo4j_conn = Neo4jConnection()
        
        # Check what nodes exist
        print("📋 Checking all nodes in database:")
        all_nodes_query = "MATCH (n) RETURN n.title, n.type, n.content LIMIT 10"
        all_nodes = await neo4j_conn.run_cypher(all_nodes_query)
        
        for i, record in enumerate(all_nodes):
            print(f"   {i+1}. Title: {record['n.title']}")
            print(f"      Type: {record['n.type']}")
            print(f"      Content: {record['n.content'][:100]}...")
            print()
        
        # Check node labels
        print("🏷️  Checking node labels:")
        labels_query = "CALL db.labels() YIELD label RETURN label"
        labels = await neo4j_conn.run_cypher(labels_query)
        for record in labels:
            print(f"   - {record['label']}")
        
        # Check node properties
        print("\n📊 Checking node properties:")
        props_query = "MATCH (n) RETURN keys(n) as properties LIMIT 1"
        props = await neo4j_conn.run_cypher(props_query)
        if props:
            print(f"   Properties: {props[0]['properties']}")
        
        # Test a simple search query
        print("\n🔍 Testing simple search query:")
        test_query = "MATCH (n) WHERE n.content CONTAINS 'business' RETURN n.title, n.type LIMIT 5"
        test_results = await neo4j_conn.run_cypher(test_query)
        print(f"   Found {len(test_results)} nodes containing 'business'")
        for record in test_results:
            print(f"   - {record['n.title']} ({record['n.type']})")
        
        # Test title search
        print("\n🔍 Testing title search:")
        title_query = "MATCH (n) WHERE n.title CONTAINS 'business' RETURN n.title, n.type LIMIT 5"
        title_results = await neo4j_conn.run_cypher(title_query)
        print(f"   Found {len(title_results)} nodes with 'business' in title")
        for record in title_results:
            print(f"   - {record['n.title']} ({record['n.type']})")
        
        # Test content search
        print("\n🔍 Testing content search:")
        content_query = "MATCH (n) WHERE n.content CONTAINS 'UAE' RETURN n.title, n.type LIMIT 5"
        content_results = await neo4j_conn.run_cypher(content_query)
        print(f"   Found {len(content_results)} nodes containing 'UAE'")
        for record in content_results:
            print(f"   - {record['n.title']} ({record['n.type']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(debug_neo4j_data())
    sys.exit(0 if success else 1)
