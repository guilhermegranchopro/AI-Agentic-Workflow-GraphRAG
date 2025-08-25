import { NextApiRequest, NextApiResponse } from 'next';

export const config = {
  runtime: 'nodejs',
};

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { query, scope = 'all', maxFindings = 10 } = req.body;

    if (!query || typeof query !== 'string') {
      return res.status(400).json({ error: 'Invalid query format' });
    }

    // Set headers for SSE
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Headers', 'Cache-Control');

    const startTime = Date.now();

    // Always use Python backend for analysis
    await analyzeWithPythonBackend(query, scope, maxFindings, res, startTime);

    res.end();

  } catch (error) {
    console.error('Analysis API error:', error);
    
    if (!res.headersSent) {
      res.setHeader('Content-Type', 'application/json');
      res.status(500).json({ 
        error: 'Internal server error',
        details: error instanceof Error ? error.message : 'Unknown error'
      });
    } else {
      res.write(`event: error\ndata: ${JSON.stringify({ error: 'Analysis failed' })}\n\n`);
      res.end();
    }
  }
}

async function analyzeWithPythonBackend(query: string, scope: string, maxFindings: number, res: NextApiResponse, startTime: number) {
  try {
    // Check if Python backend is available
    const healthResponse = await fetch('http://127.0.0.1:8000/health');
    if (!healthResponse.ok) {
      throw new Error('Python backend not available');
    }

    // Send progress updates
    res.write(`event: progress\ndata: ${JSON.stringify({
      type: 'progress',
      data: {
        step: 'initialization',
        message: 'Initializing advanced legal analysis with Python backend...',
        timestamp: Date.now()
      }
    })}\n\n`);

    await new Promise(resolve => setTimeout(resolve, 500));

    res.write(`event: progress\ndata: ${JSON.stringify({
      type: 'progress',
      data: {
        step: 'graphrag_search',
        message: 'Performing advanced GraphRAG search with semantic embeddings...',
        timestamp: Date.now()
      }
    })}\n\n`);

    // Call Python GraphRAG endpoint
    const graphragResponse = await fetch('http://127.0.0.1:8000/api/graphrag/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: query,
        search_mode: 'hybrid',
        max_results: maxFindings
      }),
    });

    if (!graphragResponse.ok) {
      throw new Error(`GraphRAG query failed: ${graphragResponse.status}`);
    }

    const graphragData: any = await graphragResponse.json();

    await new Promise(resolve => setTimeout(resolve, 800));

    res.write(`event: progress\ndata: ${JSON.stringify({
      type: 'progress',
      data: {
        step: 'advanced_analysis',
        message: 'Running advanced legal analysis with NLP and pattern recognition...',
        timestamp: Date.now()
      }
    })}\n\n`);

    // Call Python advanced analysis endpoint
    const analysisResponse = await fetch('http://127.0.0.1:8000/api/analysis/advanced', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: query,
        analysis_types: ['legal_patterns', 'citations', 'contradictions'],
        jurisdiction: 'UAE'
      }),
    });

    let analysisData: any = {};
    if (analysisResponse.ok) {
      analysisData = await analysisResponse.json();
    }

    await new Promise(resolve => setTimeout(resolve, 1000));

    // Combine results and send final response
    const finalResult = {
      query,
      scope,
      maxFindings,
      passages: graphragData.passages || [],
      contradictions: analysisData.contradictions || [],
      harmonisations: [],
      citations: analysisData.citations || [],
      legal_patterns: analysisData.legal_patterns || [],
      agent_results: graphragData.agent_results || [],
      metadata: {
        backend: 'python_fastapi_advanced',
        processing_time: Date.now() - startTime,
        graphrag_results: graphragData.passages?.length || 0,
        analysis_features: ['semantic_search', 'legal_nlp', 'pattern_recognition', 'contradiction_detection'],
        timestamp: Date.now()
      }
    };

    res.write(`event: complete\ndata: ${JSON.stringify(finalResult)}\n\n`);

  } catch (error) {
    console.error('Python backend analysis error:', error);
    
    // Send error response
    res.write(`event: error\ndata: ${JSON.stringify({
      error: 'Python backend analysis failed',
      message: 'The advanced Python backend analysis is currently unavailable. Please ensure the Python FastAPI server is running on port 8000.',
      details: error instanceof Error ? error.message : 'Unknown error'
    })}\n\n`);
  }
}
