import { NextApiRequest, NextApiResponse } from 'next';

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

    // Set headers for SSE
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Headers', 'Cache-Control');

    // Always use Python backend now
    await streamFromPythonBackend(query, res);

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

async function streamFromPythonBackend(query: string, res: NextApiResponse) {
  try {
    // Check if Python backend is available
    const healthResponse = await fetch('http://127.0.0.1:8000/health');
    if (!healthResponse.ok) {
      throw new Error('Python backend not available');
    }

    // Send initial progress
    res.write(`event: progress\ndata: ${JSON.stringify({ 
      type: 'progress', 
      data: { 
        stage: 'python_backend', 
        message: 'Connecting to Python backend with advanced AI capabilities...' 
      } 
    })}\n\n`);

    // Call Python backend streaming endpoint
    const response = await fetch('http://127.0.0.1:8000/api/assistant/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        query: query,
        mode: 'hybrid',
        max_results: 15
      }),
    });

    if (!response.ok) {
      throw new Error(`Python backend error: ${response.status}`);
    }

    // Stream the response from Python backend
    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error('No response reader available');
    }

    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          if (data.trim()) {
            // Forward the data from Python backend
            res.write(`data: ${data}\n\n`);
          }
        }
      }
    }

  } catch (error) {
    console.error('Python backend error:', error);
    
    // Send error response
    res.write(`event: error\ndata: ${JSON.stringify({
      error: 'Python backend unavailable',
      message: 'The advanced Python backend is currently unavailable. Please ensure the Python FastAPI server is running on port 8000.',
      details: error instanceof Error ? error.message : 'Unknown error'
    })}\n\n`);
  }
}
