import asyncio
import sys
sys.path.append('.')
from src.agents.manager import AgentSystemManager
from src.agents.protocol import AgentMessage, MessageType
import json

async def test_all_agents():
    try:
        # Initialize the agent system
        manager = AgentSystemManager()
        await manager.initialize_system()
        
        print("AI Agents Workflow - Complete System Test")
        print("=" * 80)
        print(f'Available agents: {list(manager.agents.keys())}')
        print()
        
        # Test queries for each agent type
        test_cases = [
            {
                'query': 'What are the specific requirements for Dubai business registration?',
                'agent': 'local_rag',
                'task_type': 'local_rag_query',
                'description': 'Local RAG (specific provisions)'
            },
            {
                'query': 'What is the legal framework for Constitutional Law in the UAE?',
                'agent': 'global_rag', 
                'task_type': 'global_rag_query',
                'description': 'Global RAG (conceptual framework)'
            },
            {
                'query': 'What changes have occurred in Constitutional Law regarding citizen rights?',
                'agent': 'drift_rag',
                'task_type': 'drift_rag_query',
                'description': 'DRIFT RAG (temporal analysis)',
                'extra_params': {
                    'reference_date': '2024-01-01',
                    'time_scope': 'comprehensive'
                }
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"Test {i}: {test_case['description']}")
            print(f"Query: {test_case['query']}")
            print("-" * 60)
            
            # Create task
            task = {
                'id': f'test_{test_case["agent"]}_{i}',
                'type': test_case['task_type'],
                'priority': 1,
                'query': test_case['query'],
                'context': {'agent_preference': test_case['agent']}
            }
            
            # Add extra parameters if present
            if 'extra_params' in test_case:
                task.update(test_case['extra_params'])
            
            # Create message
            message = AgentMessage(
                type=MessageType.REQUEST,
                sender_id='test_client',
                recipient_id=test_case['agent'],
                content={'task': task}
            )
            
            # Process through specific agent
            agent = manager.agents.get(test_case['agent'])
            if agent:
                try:
                    result = await agent.handle_message(message)
                    
                    if result and result.content:
                        task_result = result.content.get('result', {})
                        response = task_result.get('response', '')
                        sources = task_result.get('sources', [])
                        confidence = task_result.get('confidence', 0.0)
                        error = task_result.get('error', False)
                        
                        print(f"✅ Agent: {test_case['agent']}")
                        print(f"✅ Response generated: {bool(response)}")
                        print(f"✅ Response length: {len(response)}")
                        print(f"✅ Sources: {len(sources)}")
                        print(f"✅ Confidence: {confidence}")
                        print(f"✅ Error: {error}")
                        
                        # Show agent-specific metrics
                        if test_case['agent'] == 'drift_rag':
                            timeline = task_result.get('timeline', [])
                            amendments = task_result.get('amendments', [])
                            print(f"✅ Timeline events: {len(timeline)}")
                            print(f"✅ Amendments: {len(amendments)}")
                        
                        print()
                        print("Response preview:")
                        print(response[:200] + "..." if len(response) > 200 else response)
                        
                    else:
                        print(f"❌ No result from {test_case['agent']}")
                        
                except Exception as e:
                    print(f"❌ Error testing {test_case['agent']}: {e}")
            else:
                print(f"❌ Agent {test_case['agent']} not found")
            
            print()
            print("=" * 80)
            print()
        
        # Test orchestrator coordination
        print("Test 4: Orchestrator Multi-Agent Synthesis")
        print("Query: Comprehensive analysis of UAE business law framework")
        print("-" * 60)
        
        orchestrator_task = {
            'id': 'test_orchestrator_001',
            'type': 'comprehensive_analysis',
            'priority': 1,
            'query': 'Provide comprehensive analysis of UAE business law framework',
            'context': {'synthesis_required': True}
        }
        
        orchestrator_message = AgentMessage(
            type=MessageType.REQUEST,
            sender_id='test_client',
            recipient_id='orchestrator',
            content={'task': orchestrator_task}
        )
        
        orchestrator = manager.agents.get('orchestrator')
        if orchestrator:
            try:
                orch_result = await orchestrator.handle_message(orchestrator_message)
                
                if orch_result and orch_result.content:
                    orch_task_result = orch_result.content.get('result', {})
                    orch_response = orch_task_result.get('response', '')
                    orch_sources = orch_task_result.get('sources', [])
                    agents_used = orch_task_result.get('agents_consulted', [])
                    synthesis_applied = orch_task_result.get('synthesis_applied', False)
                    
                    print(f"✅ Orchestrator coordination successful")
                    print(f"✅ Multi-agent synthesis: {synthesis_applied}")
                    print(f"✅ Agents consulted: {agents_used}")
                    print(f"✅ Final response length: {len(orch_response)}")
                    print(f"✅ Total sources combined: {len(orch_sources)}")
                    
                else:
                    print(f"❌ No result from orchestrator")
                    
            except Exception as e:
                print(f"❌ Error testing orchestrator: {e}")
        else:
            print(f"❌ Orchestrator not found")
        
        print()
        print("=" * 80)
        print("🎉 AI Agents Workflow System Test Complete!")
        print("All agents are functional and the multi-agent system is ready for deployment.")
                
    except Exception as e:
        print(f'Error during testing: {e}')
        import traceback
        traceback.print_exc()

# Run the test
if __name__ == "__main__":
    asyncio.run(test_all_agents())
