import asyncio
import sys
sys.path.append('.')
from src.agents.manager import AgentSystemManager
from src.agents.protocol import AgentMessage, MessageType
import json

async def test_drift_rag():
    try:
        # Initialize the agent system
        manager = AgentSystemManager()
        await manager.initialize_system()
        
        # Create a test query for temporal legal analysis
        query = 'What changes have occurred in Constitutional Law regarding citizen rights?'
        
        # Create task dictionary for DRIFT RAG agent
        task = {
            'id': 'test_drift_001',
            'type': 'drift_rag_query',
            'priority': 1,
            'query': query,
            'reference_date': '2024-01-01',
            'time_scope': 'comprehensive',
            'context': {'agent_preference': 'drift'}
        }
        
        # Create message for DRIFT RAG agent
        message = AgentMessage(
            type=MessageType.REQUEST,
            sender_id='test_client',
            recipient_id='drift_rag_agent',
            content={'task': task}
        )
        
        print(f'Testing DRIFT RAG agent with query: {query}')
        print('Reference date: 2024-01-01, Time scope: comprehensive')
        print(f'Available agents: {list(manager.agents.keys())}')
        print('-' * 80)
        
        # Process through DRIFT RAG agent directly
        drift_agent = manager.agents.get('drift_rag')
        if not drift_agent:
            print("DRIFT RAG agent not found in manager.agents")
            return
            
        result = await drift_agent.handle_message(message)
        
        if result and result.content:
            task_result = result.content.get('result', {})
            response = task_result.get('response', '')
            sources = task_result.get('sources', [])
            timeline = task_result.get('timeline', [])
            amendments = task_result.get('amendments', [])
            confidence = task_result.get('confidence', 0.0)
            error = task_result.get('error', False)
            
            print(f'Response generated: {bool(response)}')
            print(f'Response length: {len(response)}')
            print(f'Strategy used: drift_rag')
            print(f'Sources: {len(sources)}')
            print(f'Timeline events: {len(timeline)}')
            print(f'Amendments: {len(amendments)}')
            print(f'Confidence: {confidence}')
            print(f'Error present: {error}')
            print()
            
            if response and not error:
                print('RESPONSE:')
                print(response[:500] + '...' if len(response) > 500 else response)
                print()
                
                if sources:
                    print('SOURCES:')
                    for i, source in enumerate(sources[:2]):
                        print(f'{i+1}. {source.get("title", "Unknown")}')
                        print(f'   Content: {source.get("content", "")[:100]}...')
                
                if timeline:
                    print()
                    print('TIMELINE:')
                    for event in timeline[:3]:
                        print(f'- {event.get("date", "Unknown")}: {event.get("event", "Unknown event")}')
                        
            else:
                print('ERROR in response generation!')
                print(f'Error details: {task_result}')
        else:
            print('No result received from DRIFT RAG agent')
    
    except Exception as e:
        print(f'Error during testing: {e}')
        import traceback
        traceback.print_exc()

# Run the test
if __name__ == "__main__":
    asyncio.run(test_drift_rag())
