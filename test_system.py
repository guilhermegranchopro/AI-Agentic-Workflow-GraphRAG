#!/usr/bin/env python3
"""
Comprehensive System Test Script
Tests the UAE Legal GraphRAG application to ensure all components are working properly.
"""

import asyncio
import json
import sys
import time
from pathlib import Path
import aiohttp
import requests

def test_backend_health():
    """Test backend health endpoint."""
    print("🔍 Testing Backend Health...")
    try:
        response = requests.get("http://localhost:8012/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Backend is running - Status: {data.get('status', 'unknown')}")
            print(f"  📊 Dependencies: {data.get('dependencies', {})}")
            return True
        else:
            print(f"  ❌ Backend health check failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Backend health check error: {e}")
        return False

def test_backend_api():
    """Test backend API endpoints."""
    print("\n🔍 Testing Backend API Endpoints...")
    
    # Test chat endpoint
    try:
        response = requests.post(
            "http://localhost:8012/api/chat",
            json={
                "message": "What is corporate tax in UAE?",
                "strategy": "auto",
                "max_results": 5,
                "conversation_id": "test_system"
            },
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Chat API working - Response length: {len(data.get('response', ''))}")
            print(f"  📝 Strategy used: {data.get('metadata', {}).get('strategy', 'unknown')}")
            print(f"  📚 Citations found: {len(data.get('citations', []))}")
            return True
        else:
            print(f"  ❌ Chat API failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Chat API error: {e}")
        return False

def test_backend_graph():
    """Test backend graph endpoint."""
    try:
        response = requests.get("http://localhost:8012/api/graph", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Graph API working - Nodes: {len(data.get('nodes', []))}, Edges: {len(data.get('edges', []))}")
            return True
        else:
            print(f"  ❌ Graph API failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Graph API error: {e}")
        return False

def test_backend_analysis():
    """Test backend analysis endpoint."""
    try:
        response = requests.post(
            "http://localhost:8012/api/analysis",
            json={
                "query": "UAE Court System",
                "max_results": 10
            },
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            contradictions = len(data.get('contradictions', []))
            recommendations = len(data.get('recommendations', []))
            print(f"  ✅ Analysis API working - Contradictions: {contradictions}, Recommendations: {recommendations}")
            return True
        else:
            print(f"  ❌ Analysis API failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Analysis API error: {e}")
        return False

def test_frontend():
    """Test frontend availability."""
    print("\n🔍 Testing Frontend...")
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("  ✅ Frontend is running and accessible")
            return True
        else:
            print(f"  ❌ Frontend returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Frontend error: {e}")
        return False

def test_frontend_api():
    """Test frontend API routes."""
    print("\n🔍 Testing Frontend API Routes...")
    
    # Test assistant API
    try:
        response = requests.post(
            "http://localhost:3000/api/assistant",
            json={
                "messages": [{"role": "user", "content": "What is corporate tax?"}]
            },
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Frontend Assistant API working - Response: {len(data.get('text', ''))} chars")
            return True
        else:
            print(f"  ❌ Frontend Assistant API failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Frontend Assistant API error: {e}")
        return False

def test_graph_data():
    """Test graph data endpoint."""
    try:
        response = requests.get("http://localhost:3000/api/graph", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Frontend Graph API working - Nodes: {len(data.get('nodes', []))}")
            return True
        else:
            print(f"  ❌ Frontend Graph API failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Frontend Graph API error: {e}")
        return False

def test_neo4j_connection():
    """Test Neo4j connection through backend."""
    print("\n🔍 Testing Neo4j Connection...")
    try:
        # Test through graph endpoint which uses Neo4j
        response = requests.get("http://localhost:8012/api/graph", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('nodes') and len(data['nodes']) > 0:
                print(f"  ✅ Neo4j connection working - {len(data['nodes'])} nodes found")
                return True
            else:
                print("  ⚠️  Neo4j connected but no data found")
                return False
        else:
            print(f"  ❌ Neo4j test failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Neo4j test error: {e}")
        return False

def generate_test_report(results):
    """Generate a comprehensive test report."""
    print("\n" + "="*60)
    print("📊 COMPREHENSIVE SYSTEM TEST REPORT")
    print("="*60)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    failed_tests = total_tests - passed_tests
    
    print(f"\n📈 Test Summary:")
    print(f"  Total Tests: {total_tests}")
    print(f"  ✅ Passed: {passed_tests}")
    print(f"  ❌ Failed: {failed_tests}")
    print(f"  📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    print(f"\n🔍 Detailed Results:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
    
    print(f"\n🎯 System Status:")
    if passed_tests == total_tests:
        print("  🟢 ALL SYSTEMS OPERATIONAL")
        print("  🚀 UAE Legal GraphRAG is ready for use!")
    elif passed_tests >= total_tests * 0.8:
        print("  🟡 MOSTLY OPERATIONAL - Minor issues detected")
        print("  ⚠️  Some components may need attention")
    else:
        print("  🔴 SIGNIFICANT ISSUES DETECTED")
        print("  🚨 System requires immediate attention")
    
    print("\n📋 Recommendations:")
    if failed_tests > 0:
        print("  1. Check failed components listed above")
        print("  2. Verify all services are running")
        print("  3. Check environment variables and configurations")
        print("  4. Review logs for error details")
    else:
        print("  1. System is fully operational")
        print("  2. Ready for production use")
        print("  3. Monitor system health regularly")
    
    print("="*60)

def main():
    """Run comprehensive system tests."""
    print("🚀 Starting UAE Legal GraphRAG System Tests...")
    print("="*60)
    
    results = {}
    
    # Test backend components
    results["Backend Health"] = test_backend_health()
    results["Backend Chat API"] = test_backend_api()
    results["Backend Graph API"] = test_backend_graph()
    results["Backend Analysis API"] = test_backend_analysis()
    
    # Test frontend components
    results["Frontend Availability"] = test_frontend()
    results["Frontend Assistant API"] = test_frontend_api()
    results["Frontend Graph API"] = test_graph_data()
    
    # Test database connection
    results["Neo4j Connection"] = test_neo4j_connection()
    
    # Generate comprehensive report
    generate_test_report(results)
    
    # Return appropriate exit code
    if all(results.values()):
        print("\n🎉 All tests passed! System is fully operational.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review the report above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
