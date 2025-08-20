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
          // Send token chunk
          res.write(`event: token\ndata: ${JSON.stringify({ token: chunk })}\n\n`);
        } else {
          // Send final result
          res.write(`event: complete\ndata: ${JSON.stringify(chunk)}\n\n`);
          break;
        }
      }
    } catch (streamError) {
      console.error('Streaming error:', streamError);
      res.write(`event: error\ndata: ${JSON.stringify({ error: 'Streaming failed' })}\n\n`);
    }

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
      res.write(`event: error\ndata: ${JSON.stringify({ error: 'Internal server error' })}\n\n`);
      res.end();
    }
  }
}
