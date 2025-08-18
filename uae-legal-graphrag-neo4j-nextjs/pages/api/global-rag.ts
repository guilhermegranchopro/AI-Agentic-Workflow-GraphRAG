import type { NextApiRequest, NextApiResponse } from 'next';
import { exec } from 'child_process';
import { promisify } from 'util';
import path from 'path';

const execAsync = promisify(exec);

interface GlobalRAGRequest {
  query: string;
  maxResults?: number;
}

interface GlobalRAGResponse {
  response: string;
  sources: Array<{
    id: string;
    title: string;
    content: string;
    type: string;
    relevanceScore: number;
  }>;
  confidence: number;
  communities?: Array<{
    id: string;
    title: string;
    summary: string;
    size: number;
  }>;
  metadata?: {
    query_time: number;
    total_sources: number;
  };
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<GlobalRAGResponse | { error: string }>
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { query, maxResults = 5 } = req.body as GlobalRAGRequest;

  if (!query) {
    return res.status(400).json({ error: 'Query is required' });
  }

  try {
    const pythonBackendPath = path.join(process.cwd(), 'python-backend');
    
    const globalRAGCommand = `cd "${pythonBackendPath}" && python -c "
import sys
import json
sys.path.append('.')
from graph.tools import global_rag_query

try:
    result = global_rag_query(
        query='${query.replace(/'/g, "\\'")}',
        max_results=${maxResults}
    )
    
    print(json.dumps(result))
except Exception as e:
    import traceback
    print(json.dumps({
        'error': str(e),
        'traceback': traceback.format_exc()
    }))
"`;

    const result = await execAsync(globalRAGCommand, { 
      timeout: 45000,  // 45 second timeout for global queries
      maxBuffer: 2 * 1024 * 1024  // 2MB buffer
    });
    
    const data = JSON.parse(result.stdout.trim());

    if (data.error) {
      console.error('Global RAG error:', data.error);
      if (data.traceback) {
        console.error('Traceback:', data.traceback);
      }
      return res.status(500).json({ error: data.error });
    }

    // Format the response to match our interface
    const formattedResponse: GlobalRAGResponse = {
      response: data.response || data.answer || 'No response generated',
      sources: data.sources || [],
      confidence: data.confidence || 0.5,
      communities: data.communities || [],
      metadata: {
        query_time: data.query_time || 0,
        total_sources: data.sources?.length || 0
      }
    };

    res.status(200).json(formattedResponse);

  } catch (error) {
    console.error('Global RAG API error:', error);
    res.status(500).json({ 
      error: 'Failed to process global RAG query' 
    });
  }
}
