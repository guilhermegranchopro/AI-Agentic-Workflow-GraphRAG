import type { NextApiRequest, NextApiResponse } from 'next';
import { spawn } from 'child_process';
import path from 'path';

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

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<GlobalRAGResponse | { error: string }>
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { query, maxResults = 5 } = req.body as GlobalRAGRequest;

  if (!query || !query.trim()) {
    return res.status(400).json({ error: 'Query is required' });
  }

  const pythonBackendPath = path.join(process.cwd(), 'python-backend');

  const pythonProcess = spawn('python', [
    '-c',
    `
import sys
import os
import json
sys.path.append('${pythonBackendPath.replace(/\\/g, '\\\\')}')

try:
    # Mock global RAG response with community-based analysis
    query_text = "${query.replace(/"/g, '\\"')}"
    
    result = {
        "response": f"Based on global community analysis of UAE legal framework, the query '{query_text}' has been analyzed across multiple legal communities. The Graph Data Science approach reveals interconnected legal concepts spanning Civil Law, Commercial Law, and Administrative regulations. Key communities identified include Contract Law Community, Liability Framework Community, and Judicial Interpretation Community.",
        "sources": [
            {
                "id": "community_1_analysis",
                "title": "Contract Law Community Analysis",
                "content": "This community encompasses UAE Civil Code Articles 125-405, focusing on contractual obligations, formation, and performance standards.",
                "type": "COMMUNITY_ANALYSIS",
                "relevanceScore": 0.91
            }
        ],
        "confidence": 0.88,
        "communities": [
            {
                "id": "contract_law_community",
                "title": "Contract Law Community",
                "summary": "Comprehensive contractual framework governing agreements, obligations, and enforcement mechanisms",
                "size": 45
            }
        ],
        "metadata": {
            "query_time": 2.1,
            "total_sources": 1
        }
    }
    
    print(json.dumps(result, default=str))
except Exception as e:
    error_result = {
        "response": f"Error processing global RAG query: {str(e)}",
        "sources": [],
        "confidence": 0.0,
        "communities": [],
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
        
        const globalResponse: GlobalRAGResponse = {
          response: result.response || 'No response generated',
          sources: result.sources || [],
          confidence: result.confidence || 0.0,
          communities: result.communities || [],
          metadata: {
            query_time: result.metadata?.query_time || 0.0,
            total_sources: result.metadata?.total_sources || 0
          }
        };
        
        res.status(200).json(globalResponse);
      } else {
        console.error('Python process failed:', errorOutput);
        res.status(500).json({ 
          error: errorOutput || 'Failed to process global RAG query'
        });
      }
    } catch (parseError) {
      console.error('Failed to parse Python output:', parseError);
      res.status(500).json({ 
        error: 'Failed to parse global RAG response'
      });
    }
  });

  pythonProcess.on('error', (error) => {
    console.error('Failed to start Python process:', error);
    res.status(500).json({ 
      error: 'Failed to start global RAG process'
    });
  });
}
