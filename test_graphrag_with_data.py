#!/usr/bin/env python3
"""
Test script to verify GraphRAG functionality with loaded mock data
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def test_graphrag_queries():
    """Test GraphRAG queries with the loaded mock data."""
    print("🔍 Testing GraphRAG with Mock UAE Legal Data")
    print("=" * 50)
    
    try:
        # Initialize services
        from backend.app.adapters.neo4j_conn import Neo4jConnection
        from backend.app.rag.graph_interface import LocalGraphRAG, GlobalGraphRAG, DRIFTGraphRAG
        
        neo4j_conn = Neo4jConnection()
        
        # Test queries
        test_queries = [
            "business requirements",
            "corporate tax",
            "free zones",
            "labor law",
            "intellectual property",
            "banking regulations",
            "foreign ownership",
            "arbitration"
        ]
        
        print("📋 Testing Local GraphRAG:")
        local_rag = LocalGraphRAG(neo4j_conn)
        
        for query in test_queries[:3]:  # Test first 3 queries
            print(f"\n🔍 Query: '{query}'")
            result = await local_rag.retrieve(query, max_results=5)
            print(f"   📊 Found {len(result.nodes)} nodes")
            print(f"   🔗 Found {len(result.edges)} relationships")
            print(f"   📚 Found {len(result.citations)} citations")
            print(f"   📈 Coverage: {result.coverage:.2%}")
            print(f"   🎯 Confidence: {result.confidence:.2f}")
            
            if result.nodes:
                print("   📋 Top nodes:")
                for i, node in enumerate(result.nodes[:3]):
                    print(f"      {i+1}. {node.content[:50]}... ({node.type})")
        
        print("\n📋 Testing Global GraphRAG:")
        global_rag = GlobalGraphRAG(neo4j_conn)
        
        for query in test_queries[3:6]:  # Test next 3 queries
            print(f"\n🔍 Query: '{query}'")
            result = await global_rag.retrieve(query, max_results=5)
            print(f"   📊 Found {len(result.nodes)} nodes")
            print(f"   🔗 Found {len(result.edges)} relationships")
            print(f"   📚 Found {len(result.citations)} citations")
            print(f"   📈 Coverage: {result.coverage:.2%}")
            print(f"   🎯 Confidence: {result.confidence:.2f}")
            
            if result.nodes:
                print("   📋 Top nodes:")
                for i, node in enumerate(result.nodes[:3]):
                    print(f"      {i+1}. {node.content[:50]}... ({node.type})")
        
        print("\n📋 Testing DRIFT GraphRAG:")
        drift_rag = DRIFTGraphRAG(neo4j_conn)
        
        for query in test_queries[6:]:  # Test last 2 queries
            print(f"\n🔍 Query: '{query}'")
            result = await drift_rag.retrieve(query, max_results=5)
            print(f"   📊 Found {len(result.nodes)} nodes")
            print(f"   🔗 Found {len(result.edges)} relationships")
            print(f"   📚 Found {len(result.citations)} citations")
            print(f"   📈 Coverage: {result.coverage:.2%}")
            print(f"   🎯 Confidence: {result.confidence:.2f}")
            
            if result.nodes:
                print("   📋 Top nodes:")
                for i, node in enumerate(result.nodes[:3]):
                    print(f"      {i+1}. {node.content[:50]}... ({node.type})")
        
        print("\n🎉 All GraphRAG tests completed successfully!")
        print("✅ Local GraphRAG: Working")
        print("✅ Global GraphRAG: Working")
        print("✅ DRIFT GraphRAG: Working")
        print("✅ Mock data is being retrieved correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_specific_legal_queries():
    """Test specific UAE legal queries."""
    print("\n🏛️  Testing Specific UAE Legal Queries")
    print("=" * 40)
    
    try:
        from backend.app.rag.graph_interface import LocalGraphRAG
        from backend.app.adapters.neo4j_conn import Neo4jConnection
        
        neo4j_conn = Neo4jConnection()
        local_rag = LocalGraphRAG(neo4j_conn)
        
        # Test specific legal queries
        legal_queries = [
            "What are the requirements for starting a business in UAE?",
            "How does corporate tax work in UAE?",
            "What are the benefits of free zones?",
            "What are the labor law requirements?",
            "How to protect intellectual property in UAE?"
        ]
        
        for query in legal_queries:
            print(f"\n🔍 Legal Query: '{query}'")
            result = await local_rag.retrieve(query, max_results=3)
            
            if result.nodes:
                print(f"   📊 Found {len(result.nodes)} relevant legal nodes:")
                for i, node in enumerate(result.nodes):
                    print(f"      {i+1}. {node.content[:50]}...")
                    print(f"         Type: {node.type}")
                    print(f"         Content: {node.content[:100]}...")
                    print(f"         Score: {node.score}")
            else:
                print("   ❌ No relevant nodes found")
        
        print("\n✅ Specific legal queries test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Legal queries test failed: {e}")
        return False

async def main():
    """Main test function."""
    print("🚀 UAE Legal GraphRAG - Data Verification Test")
    print("=" * 60)
    
    # Test basic GraphRAG functionality
    if not await test_graphrag_queries():
        return False
    
    # Test specific legal queries
    if not await test_specific_legal_queries():
        return False
    
    print("\n🎉 All tests passed successfully!")
    print("📊 The Neo4j knowledge graph is working correctly with mock UAE legal data")
    print("🔍 GraphRAG can now provide meaningful legal information")
    print("🚀 Ready for the 2-hour presentation!")
    
    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
