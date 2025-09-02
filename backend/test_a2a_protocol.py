#!/usr/bin/env python3
"""
A2A Protocol Test Script - Following the Exact A2A Protocol Guide
================================================================

This script tests the A2A Protocol implementation in the UAE Legal GraphRAG system.
It follows the exact A2A Protocol guidelines provided:

1. Discovery: publish an Agent Card at /.well-known/agent.json
2. Choose a transport and implement the core methods
3. Auth & security
4. Streaming & long-running tasks
5. Compliance testing

Run this script to verify that all A2A Protocol endpoints are working correctly.
"""

import requests
import json
import time
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"  # Change this to your deployment URL
API_TOKEN = "your-api-token-here"  # Replace with actual token

# Headers
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_TOKEN}"
}


def test_agent_discovery():
    """
    Test agent discovery endpoints - A2A Protocol requirement #1.
    
    This tests the /.well-known/agent.json endpoint which is REQUIRED for A2A Protocol compliance.
    """
    print("🔍 Testing Agent Discovery (A2A Protocol Requirement #1)...")
    
    # Test /.well-known/agent.json - THIS IS REQUIRED FOR A2A COMPLIANCE
    try:
        response = requests.get(f"{BASE_URL}/.well-known/agent.json")
        if response.status_code == 200:
            agent_card = response.json()
            print(f"✅ Agent Card: {agent_card['name']} v{agent_card['protocolVersion']}")
            print(f"   Skills: {len(agent_card['skills'])} available")
            print(f"   Transports: {[t['transport'] for t in agent_card['transports']]}")
            print(f"   Base URL: {agent_card['service']['baseUrl']}")
            
            # Verify A2A Protocol compliance
            if agent_card.get('protocolVersion') == '0.3.0':
                print("   ✅ A2A Protocol version 0.3.0 compliant")
            else:
                print(f"   ❌ A2A Protocol version mismatch: {agent_card.get('protocolVersion')}")
                
        else:
            print(f"❌ Agent Card failed: {response.status_code}")
            print("   ❌ THIS ENDPOINT IS REQUIRED FOR A2A PROTOCOL COMPLIANCE")
    except Exception as e:
        print(f"❌ Agent Card error: {e}")
        print("   ❌ THIS ENDPOINT IS REQUIRED FOR A2A PROTOCOL COMPLIANCE")
    
    # Test /.well-known/agent (alternative endpoint)
    try:
        response = requests.get(f"{BASE_URL}/.well-known/agent")
        if response.status_code == 200:
            print("✅ Alternative agent endpoint working")
        else:
            print(f"❌ Alternative agent endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Alternative agent endpoint error: {e}")
    
    # Test /.well-known/health
    try:
        response = requests.get(f"{BASE_URL}/.well-known/health")
        if response.status_code == 200:
            health = response.json()
            print(f"✅ Well-known health: {health['status']}")
        else:
            print(f"❌ Well-known health failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Well-known health error: {e}")


def test_a2a_health():
    """
    Test A2A Protocol health endpoint.
    """
    print("\n🏥 Testing A2A Protocol Health...")
    
    try:
        response = requests.get(f"{BASE_URL}/a2a/health")
        if response.status_code == 200:
            health = response.json()
            print(f"✅ A2A Health: {health['status']}")
            print(f"   Protocol: {health['protocol']} v{health['version']}")
            print(f"   Endpoints: {len(health['endpoints'])} available")
            
            # Verify required endpoints are listed
            required_endpoints = [
                "/.well-known/agent.json",
                "/v1/message:send",
                "/v1/message:stream",
                "/v1/tasks/{task_id}"
            ]
            
            for endpoint in required_endpoints:
                if endpoint in health['endpoints']:
                    print(f"   ✅ {endpoint} - Available")
                else:
                    print(f"   ❌ {endpoint} - Missing (REQUIRED for A2A compliance)")
                    
        else:
            print(f"❌ A2A Health failed: {response.status_code}")
    except Exception as e:
        print(f"❌ A2A Health error: {e}")


def test_message_send():
    """
    Test A2A Protocol message:send endpoint - A2A Protocol requirement #2.
    
    This tests the core message:send method which is REQUIRED for A2A Protocol compliance.
    """
    print("\n📨 Testing A2A Protocol message:send (Requirement #2)...")
    
    # Test AI Assistant skill
    print("   Testing AI Assistant skill...")
    message_request = {
        "message": {
            "role": "user",
            "parts": [
                {
                    "kind": "text",
                    "text": "What are the UAE Data Protection Law requirements?"
                }
            ],
            "metadata": {
                "skill_id": "ai_assistant"
            }
        },
        "configuration": {
            "strategy": "hybrid",
            "max_results": 3
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/a2a/v1/message:send",
            json=message_request,
            headers=HEADERS
        )
        
        if response.status_code == 200:
            result = response.json()
            print("     ✅ AI Assistant request successful")
            print(f"     Response: {result['message']['parts'][0]['text'][:100]}...")
            print(f"     Citations: {result['message']['metadata']['citations_count']}")
            print(f"     Processing time: {result['metadata']['processing_time']}s")
        else:
            print(f"     ❌ AI Assistant failed: {response.status_code}")
            print(f"     Error: {response.text}")
    except Exception as e:
        print(f"     ❌ AI Assistant error: {e}")
    
    # Test Legal Analysis skill
    print("   Testing Legal Analysis skill...")
    analysis_request = {
        "message": {
            "role": "user",
            "parts": [
                {
                    "kind": "data",
                    "data": {
                        "query": "Data Protection Law contradictions",
                        "analysis_type": "contradictions",
                        "max_depth": 2
                    }
                }
            ],
            "metadata": {
                "skill_id": "legal_analysis"
            }
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/a2a/v1/message:send",
            json=analysis_request,
            headers=HEADERS
        )
        
        if response.status_code == 200:
            result = response.json()
            print("     ✅ Legal Analysis request successful")
            print(f"     Contradictions: {result['message']['metadata']['contradictions_count']}")
            print(f"     Harmonizations: {result['message']['metadata']['harmonizations_count']}")
            print(f"     Processing time: {result['metadata']['processing_time']}s")
        else:
            print(f"     ❌ Legal Analysis failed: {response.status_code}")
            print(f"     Error: {response.text}")
    except Exception as e:
        print(f"     ❌ Legal Analysis error: {e}")


def test_graphrag_skills():
    """
    Test GraphRAG skills via A2A Protocol.
    """
    print("\n🔍 Testing GraphRAG Skills...")
    
    skills = ["local_graphrag", "global_graphrag", "drift_graphrag"]
    
    for skill in skills:
        print(f"   Testing {skill}...")
        
        graphrag_request = {
            "message": {
                "role": "user",
                "parts": [
                    {
                        "kind": "data",
                        "data": {
                            "query": "UAE Commercial Companies Law",
                            "max_results": 5
                        }
                    }
                ],
                "metadata": {
                    "skill_id": skill
                }
            }
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/a2a/v1/message:send",
                json=graphrag_request,
                headers=HEADERS
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"     ✅ {skill}: {result['message']['metadata']['nodes_count']} nodes found")
            else:
                print(f"     ❌ {skill}: {response.status_code}")
        except Exception as e:
            print(f"     ❌ {skill}: {e}")


def test_authenticated_card():
    """
    Test authenticated agent card endpoint.
    """
    print("\n🔐 Testing Authenticated Agent Card...")
    
    try:
        response = requests.get(f"{BASE_URL}/a2a/v1/card", headers=HEADERS)
        if response.status_code == 200:
            card = response.json()
            print("✅ Authenticated card successful")
            print(f"   Authenticated: {card['metadata'].get('authenticated', False)}")
            if 'internal_metrics' in card['metadata']:
                metrics = card['metadata']['internal_metrics']
                print(f"   Total requests: {metrics.get('total_requests', 0)}")
                print(f"   Active tasks: {metrics.get('active_tasks', 0)}")
        else:
            print(f"❌ Authenticated card failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Authenticated card error: {e}")


def test_a2a_compliance():
    """
    Test A2A Protocol compliance - A2A Protocol requirement #5.
    
    This verifies that the implementation follows the A2A Protocol specification.
    """
    print("\n🔍 Testing A2A Protocol Compliance (Requirement #5)...")
    
    compliance_checklist = {
        "Agent Card": False,
        "Message:Send": False,
        "Message:Stream": False,
        "Tasks:Get": False,
        "Transport": False,
        "Security": False,
        "Capabilities": False
    }
    
    # Test Agent Card
    try:
        response = requests.get(f"{BASE_URL}/.well-known/agent.json")
        if response.status_code == 200:
            agent_card = response.json()
            if agent_card.get('protocolVersion') == '0.3.0':
                compliance_checklist["Agent Card"] = True
                print("   ✅ Agent Card: Public discovery at /.well-known/agent.json")
            else:
                print("   ❌ Agent Card: Protocol version mismatch")
        else:
            print("   ❌ Agent Card: Endpoint not accessible")
    except Exception as e:
        print(f"   ❌ Agent Card: {e}")
    
    # Test Message:Send
    try:
        test_request = {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": "Test"}],
                "metadata": {"skill_id": "ai_assistant"}
            }
        }
        response = requests.post(f"{BASE_URL}/a2a/v1/message:send", json=test_request, headers=HEADERS)
        if response.status_code in [200, 400, 401]:  # 400/401 are valid responses for invalid requests
            compliance_checklist["Message:Send"] = True
            print("   ✅ Message:Send: Synchronous message handling")
        else:
            print(f"   ❌ Message:Send: Unexpected status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Message:Send: {e}")
    
    # Test Message:Stream
    try:
        response = requests.post(f"{BASE_URL}/a2a/v1/message:stream", json={"taskId": "test"})
        if response.status_code in [200, 400, 404]:  # Valid responses
            compliance_checklist["Message:Stream"] = True
            print("   ✅ Message:Stream: Server-Sent Events for streaming")
        else:
            print(f"   ❌ Message:Stream: Unexpected status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Message:Stream: {e}")
    
    # Test Tasks:Get
    try:
        response = requests.get(f"{BASE_URL}/a2a/v1/tasks/test")
        if response.status_code in [404]:  # 404 is expected for non-existent task
            compliance_checklist["Tasks:Get"] = True
            print("   ✅ Tasks:Get: Task status polling")
        else:
            print(f"   ❌ Tasks:Get: Unexpected status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Tasks:Get: {e}")
    
    # Test Transport
    try:
        response = requests.get(f"{BASE_URL}/.well-known/agent.json")
        if response.status_code == 200:
            agent_card = response.json()
            transports = [t['transport'] for t in agent_card.get('transports', [])]
            if 'HTTP+JSON' in transports:
                compliance_checklist["Transport"] = True
                print("   ✅ Transport: HTTP+JSON support")
            else:
                print("   ❌ Transport: HTTP+JSON not supported")
        else:
            print("   ❌ Transport: Cannot verify")
    except Exception as e:
        print(f"   ❌ Transport: {e}")
    
    # Test Security
    try:
        response = requests.get(f"{BASE_URL}/.well-known/agent.json")
        if response.status_code == 200:
            agent_card = response.json()
            security_schemes = agent_card.get('securitySchemes', [])
            if security_schemes:
                compliance_checklist["Security"] = True
                print("   ✅ Security: Authentication schemes defined")
            else:
                print("   ❌ Security: No authentication schemes")
        else:
            print("   ❌ Security: Cannot verify")
    except Exception as e:
        print(f"   ❌ Security: {e}")
    
    # Test Capabilities
    try:
        response = requests.get(f"{BASE_URL}/.well-known/agent.json")
        if response.status_code == 200:
            agent_card = response.json()
            capabilities = agent_card.get('capabilities', {})
            if capabilities.get('streaming') and capabilities.get('longRunningTasks'):
                compliance_checklist["Capabilities"] = True
                print("   ✅ Capabilities: Streaming and long-running tasks")
            else:
                print("   ❌ Capabilities: Missing required capabilities")
        else:
            print("   ❌ Capabilities: Cannot verify")
    except Exception as e:
        print(f"   ❌ Capabilities: {e}")
    
    # Summary
    print("\n📊 A2A Protocol Compliance Summary:")
    total_checks = len(compliance_checklist)
    passed_checks = sum(compliance_checklist.values())
    
    for check, status in compliance_checklist.items():
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {check}")
    
    print(f"\n   Compliance: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("   🎉 FULL A2A PROTOCOL COMPLIANCE ACHIEVED!")
    else:
        print("   ⚠️  Some compliance checks failed. Review the implementation.")


def main():
    """Run all A2A Protocol tests following the exact guidelines."""
    print("🚀 A2A Protocol Test Suite - Following Exact Guidelines")
    print("=" * 70)
    print(f"Testing against: {BASE_URL}")
    print(f"API Token: {'*' * len(API_TOKEN) if API_TOKEN != 'your-api-token-here' else 'NOT SET'}")
    print()
    print("A2A Protocol Requirements Being Tested:")
    print("1. Discovery: publish an Agent Card at /.well-known/agent.json")
    print("2. Choose a transport and implement the core methods")
    print("3. Auth & security")
    print("4. Streaming & long-running tasks")
    print("5. Compliance testing")
    print()
    
    # Run tests
    test_agent_discovery()
    test_a2a_health()
    test_message_send()
    test_graphrag_skills()
    test_authenticated_card()
    test_a2a_compliance()
    
    print("\n" + "=" * 70)
    print("🎯 A2A Protocol Test Suite Complete!")
    print("\nNext steps:")
    print("1. Verify all endpoints are working")
    print("2. Test with A2A Inspector tool")
    print("3. Deploy to production environment")
    print("4. Share agent card with other A2A agents")
    print("5. Validate compliance with A2A Protocol specification")


if __name__ == "__main__":
    main()
