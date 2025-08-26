import { NextApiRequest, NextApiResponse } from 'next';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export const config = {
  runtime: 'nodejs',
};

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { messages } = req.body;

    if (!Array.isArray(messages) || messages.length === 0) {
      return res.status(400).json({ error: 'Invalid messages format' });
    }

    // Extract the latest user query
    const userMessage = messages[messages.length - 1];
    const query = userMessage?.content || '';

    // For now, return mock response since Azure OpenAI is not fully configured
    const mockResponse = {
      text: `Based on UAE legal framework, I can help you with your query: "${query}". This is a mock response for testing purposes. In a production environment, this would be processed by the GraphRAG orchestrator with access to the full legal knowledge graph.`,
      citations: [
        {
          title: "UAE Civil Code",
          source: "Federal Law No. 5 of 1985",
          relevance: 0.95
        },
        {
          title: "Commercial Code", 
          source: "Federal Law No. 18 of 1993",
          relevance: 0.87
        }
      ],
      agents: {
        local: "Local GraphRAG agent processed query",
        global: "Global GraphRAG agent provided context",
        drift: "DRIFT agent analyzed legal changes"
      },
      confidence: 0.85,
      strategy_used: "hybrid",
      metadata: {
        processing_time: 1.2,
        sources_consulted: 2,
        legal_jurisdiction: "UAE"
      }
    };

    // Set headers for JSON response
    res.setHeader('Content-Type', 'application/json');
    res.status(200).json(mockResponse);

  } catch (error) {
    console.error('Assistant API error:', error);
    
    if (!res.headersSent) {
      res.setHeader('Content-Type', 'application/json');
      res.status(500).json({ 
        error: 'Internal server error',
        details: error instanceof Error ? error.message : 'Unknown error'
      });
    } else {
      res.write(`data: ${JSON.stringify({
        error: 'Processing failed',
        message: error instanceof Error ? error.message : 'Unknown error'
      })}\n\n`);
      res.end();
    }
  }
}
