import type { NextApiRequest, NextApiResponse } from 'next';
import { exec } from 'child_process';
import { promisify } from 'util';
import path from 'path';

const execAsync = promisify(exec);

interface LocalRAGRequest {
  query: string;
  asOfDate?: string;
  maxResults?: number;
}

interface LocalRAGResponse {
  response: string;
  sources: Array<{
    id: string;
    title: string;
    content: string;
    type: string;
    date?: string;
    relevanceScore: number;
  }>;
  confidence: number;
  metadata?: {
    query_time: number;
    total_sources: number;
  };
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<LocalRAGResponse | { error: string }>
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { query, asOfDate, maxResults = 5 } = req.body as LocalRAGRequest;

  if (!query) {
    return res.status(400).json({ error: 'Query is required' });
  }

  try {
    const pythonBackendPath = path.join(process.cwd(), 'python-backend');
    
    const localRAGCommand = `cd "${pythonBackendPath}" && python -c "
import sys
import json
from datetime import datetime
sys.path.append('.')
from graph.tools import local_rag_query

try:
    # Parse as_of_date if provided
    as_of_date = None
    if '${asOfDate}':
        as_of_date = datetime.fromisoformat('${asOfDate}'.replace('Z', '+00:00')).date()
    
    result = local_rag_query(
        query='${query.replace(/'/g, "\\'")}',
        as_of_date=as_of_date,
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

    const result = await execAsync(localRAGCommand, { 
      timeout: 30000,  // 30 second timeout
      maxBuffer: 1024 * 1024  // 1MB buffer
    });
    
    const data = JSON.parse(result.stdout.trim());

    if (data.error) {
      console.error('Local RAG error:', data.error);
      if (data.traceback) {
        console.error('Traceback:', data.traceback);
      }
      return res.status(500).json({ error: data.error });
    }

    // Format the response to match our interface
    const formattedResponse: LocalRAGResponse = {
      response: data.response || data.answer || 'No response generated',
      sources: data.sources || [],
      confidence: data.confidence || 0.5,
      metadata: {
        query_time: data.query_time || 0,
        total_sources: data.sources?.length || 0
      }
    };

    res.status(200).json(formattedResponse);

  } catch (error) {
    console.error('Local RAG API error:', error);
    res.status(500).json({ 
      error: 'Failed to process local RAG query' 
    });
  }
}
