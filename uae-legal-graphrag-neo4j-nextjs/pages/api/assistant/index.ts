import { NextApiRequest, NextApiResponse } from 'next';
import { orchestrator } from '../../../lib/ai/orchestrator';
import { ChatMessage } from '../../../lib/ai/types';

export const config = {
  runtime: 'nodejs',
};

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { messages }: { messages: ChatMessage[] } = req.body;

    if (!Array.isArray(messages) || messages.length === 0) {
      return res.status(400).json({ error: 'Invalid messages format' });
    }

    // Set headers for SSE
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Headers', 'Cache-Control');

    // Start streaming
    const stream = orchestrator.streamHandle(messages);
    
    try {
      for await (const chunk of stream) {
        if (typeof chunk === 'string') {
          // Send text token chunk
          res.write(`event: token\ndata: ${JSON.stringify({ token: chunk })}\n\n`);
        } else if (chunk && typeof chunk === 'object' && chunk.type === 'progress') {
          // Send progress event
          res.write(`event: progress\ndata: ${JSON.stringify(chunk)}\n\n`);
        } else {
          // This is the final OrchestratorResponse object
          res.write(`event: complete\ndata: ${JSON.stringify(chunk)}\n\n`);
          break;
        }
      }
    } catch (streamError) {
      console.error('Streaming error:', streamError);
      res.write(`event: error\ndata: ${JSON.stringify({ error: 'Streaming failed', details: streamError instanceof Error ? streamError.message : 'Unknown error' })}\n\n`);
    }

    res.end();

  } catch (error) {
    console.error('Assistant API error:', error);
    
    // Check if it's an Azure OpenAI configuration error
    const isAzureConfigError = error instanceof Error && 
      error.message.includes('Missing Azure OpenAI env');
    
    if (!res.headersSent) {
      res.setHeader('Content-Type', 'application/json');
      
      if (isAzureConfigError) {
        res.status(503).json({ 
          error: 'Azure OpenAI service configuration incomplete',
          message: 'Azure OpenAI environment variables not configured. Please check your .env file.',
          details: error.message,
          present: (error as any).present ?? {}
        });
      } else {
        res.status(500).json({ 
          error: 'Internal server error',
          details: error instanceof Error ? error.message : 'Unknown error'
        });
      }
    } else {
      const errorMessage = isAzureConfigError 
        ? 'Azure OpenAI service configuration incomplete' 
        : 'Internal server error';
      res.write(`event: error\ndata: ${JSON.stringify({ error: errorMessage })}\n\n`);
      res.end();
    }
  }
}
