import type { NextApiRequest, NextApiResponse } from 'next';
import { spawn } from 'child_process';
import path from 'path';

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

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<AgentsResponse | { error: string }>
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { query, session_id = 'default_session' } = req.body as AgentsRequest;

  if (!query || !query.trim()) {
    return res.status(400).json({ error: 'Query is required' });
  }

  // Path to the Python backend
  const pythonBackendPath = path.join(process.cwd(), 'python-backend');

  const pythonProcess = spawn('python', [
    '-c',
    `
import sys
import os
import json
sys.path.append('${pythonBackendPath.replace(/\\/g, '\\\\')}')

try:
    # Mock agent response with realistic legal content
    query_text = "${query.replace(/"/g, '\\"')}"
    
    # Determine agent based on query content
    agent_used = "local_rag"
    if "global" in query_text.lower() or "community" in query_text.lower():
        agent_used = "global_rag"
    elif "time" in query_text.lower() or "change" in query_text.lower() or "evolution" in query_text.lower():
        agent_used = "drift_rag"
    
    result = {
        "response": f"Based on UAE legal framework analysis using {agent_used}, the query regarding '{query_text}' involves several key legal considerations. The UAE Civil Code and Federal Laws provide comprehensive guidance on legal obligations, liability rules, and judicial interpretation. Courts typically apply these principles based on established jurisprudence, Islamic law principles where applicable, and contemporary legal precedents.",
        "agent_used": agent_used,
        "sources": [
            {
                "id": "civil_code_282",
                "title": "UAE Civil Code Article 282 - Liability",
                "content": "Every person is liable for damage caused by his wrongful act, even if he is not discerning, save for what is stipulated in the following articles.",
                "type": "LEGAL_TEXT",
                "relevanceScore": 0.89
            }
        ],
        "confidence": 0.85,
        "strategy_used": "multi_agent_reasoning",
        "reasoning": f"Selected {agent_used} based on query analysis. Applied UAE legal framework with emphasis on Civil Code provisions.",
        "metadata": {
            "query_time": 1.25,
            "total_sources": 1
        }
    }
    
    print(json.dumps(result, default=str))
except Exception as e:
    error_result = {
        "response": "I apologize, but I encountered an error processing your legal query. Please try again.",
        "agent_used": "error_handler",
        "sources": [],
        "confidence": 0.0,
        "strategy_used": "error_fallback",
        "reasoning": f"Error occurred: {str(e)}",
        "metadata": {
            "query_time": 0.0,
            "total_sources": 0
        }
    }
    print(json.dumps(error_result))
    `
  ], {
    cwd: pythonBackendPath,
    env: { ...process.env, PYTHONPATH: pythonBackendPath }
  });

  let output = '';
  let errorOutput = '';

  pythonProcess.stdout.on('data', (data) => {
    output += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    errorOutput += data.toString();
  });

  pythonProcess.on('close', (code) => {
    try {
      if (code === 0 && output.trim()) {
        const result = JSON.parse(output.trim());
        
        const agentsResponse: AgentsResponse = {
          response: result.response || 'No response generated',
          agent_used: result.agent_used || 'unknown',
          sources: result.sources || [],
          confidence: result.confidence || 0.0,
          strategy_used: result.strategy_used || 'unknown',
          reasoning: result.reasoning,
          metadata: {
            query_time: result.metadata?.query_time || 0.0,
            total_sources: result.metadata?.total_sources || 0
          }
        };
        
        res.status(200).json(agentsResponse);
      } else {
        console.error('Python process failed:', errorOutput);
        res.status(500).json({ 
          error: errorOutput || 'Failed to process agents query'
        });
      }
    } catch (parseError) {
      console.error('Failed to parse Python output:', parseError);
      res.status(500).json({ 
        error: 'Failed to parse agents response'
      });
    }
  });

  pythonProcess.on('error', (error) => {
    console.error('Failed to start Python process:', error);
    res.status(500).json({ 
      error: 'Failed to start agents process'
    });
  });
}
