import type { NextApiRequest, NextApiResponse } from 'next';
import { exec } from 'child_process';
import { promisify } from 'util';
import path from 'path';

const execAsync = promisify(exec);

interface AgentsRequest {
  query: string;
  session_id?: string;
}

interface AgentsResponse {
  response: string;
  agent_used: string;
  sources: Array<{
    id: string;
    title: string;
    content: string;
    type: string;
    relevanceScore: number;
  }>;
  confidence: number;
  strategy_used: string;
  reasoning?: string;
  metadata?: {
    query_time: number;
    total_sources: number;
  };
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<AgentsResponse | { error: string }>
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { query, session_id = 'default_session' } = req.body as AgentsRequest;

  if (!query) {
    return res.status(400).json({ error: 'Query is required' });
  }

  try {
    const pythonBackendPath = path.join(process.cwd(), 'python-backend');
    
    const agentsCommand = `cd "${pythonBackendPath}" && python -c "
import sys
import json
import asyncio
sys.path.append('.')
from agents.manager import get_agent_system

async def run_agents():
    try:
        system = await get_agent_system()
        result = await system.process_user_query(
            query='${query.replace(/'/g, "\\'")}',
            session_id='${session_id}'
        )
        return result
    except Exception as e:
        import traceback
        return {
            'error': str(e),
            'traceback': traceback.format_exc()
        }

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
result = loop.run_until_complete(run_agents())
loop.close()

print(json.dumps(result))
"`;

    const result = await execAsync(agentsCommand, { 
      timeout: 60000,  // 60 second timeout for agent queries
      maxBuffer: 3 * 1024 * 1024  // 3MB buffer
    });
    
    const data = JSON.parse(result.stdout.trim());

    if (data.error) {
      console.error('Agents error:', data.error);
      if (data.traceback) {
        console.error('Traceback:', data.traceback);
      }
      return res.status(500).json({ error: data.error });
    }

    // Format the response to match our interface
    const formattedResponse: AgentsResponse = {
      response: data.response || 'No response generated',
      agent_used: data.agent_used || 'Unknown',
      sources: data.sources || [],
      confidence: data.confidence || 0.5,
      strategy_used: data.strategy_used || 'Unknown',
      reasoning: data.reasoning,
      metadata: {
        query_time: data.query_time || 0,
        total_sources: data.sources?.length || 0
      }
    };

    res.status(200).json(formattedResponse);

  } catch (error) {
    console.error('Agents API error:', error);
    res.status(500).json({ 
      error: 'Failed to process agent query' 
    });
  }
}
