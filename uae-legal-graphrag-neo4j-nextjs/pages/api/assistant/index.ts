import { NextApiRequest, NextApiResponse } from 'next';
import { orchestrator } from '../../../lib/ai/orchestrator';
import { hasAzureOpenAIConfig } from '../../../lib/config';

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

    // Check Azure OpenAI configuration
    if (!hasAzureOpenAIConfig()) {
      return res.status(503).json({
        error: 'Azure OpenAI not configured',
        message: 'Please configure Azure OpenAI environment variables',
        details: {
          azure_openai_configured: false,
          required_vars: ['AZURE_OPENAI_API_KEY', 'AZURE_OPENAI_ENDPOINT', 'AZURE_OPENAI_DEPLOYMENT']
        }
      });
    }

    // Set headers for SSE
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Headers', 'Cache-Control');

    // Send initial progress
    res.write(`data: ${JSON.stringify({
      type: 'progress',
      data: {
        stage: 'processing',
        message: 'Processing your legal query...'
      }
    })}\n\n`);

    // Process query with orchestrator
    const result = await orchestrator.processQuery({
      query,
      strategy: 'hybrid',
      maxResults: 15
    });

    // Send final response
    res.write(`data: ${JSON.stringify({
      text: result.response,
      citations: result.sources,
      agents: result.agent_results,
      confidence: result.confidence,
      strategy: result.strategy_used,
      metadata: result.metadata
    })}\n\n`);

    res.end();

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
