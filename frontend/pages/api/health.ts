import { NextApiRequest, NextApiResponse } from 'next';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8012';

interface HealthCheckResponse {
  status: 'healthy' | 'unhealthy';
  timestamp: string;
  services: {
    neo4j: boolean;
    azure_openai: boolean;
  };
  error?: string;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<HealthCheckResponse>
) {
  if (req.method !== 'GET') {
    return res.status(405).json({
      status: 'unhealthy',
      timestamp: new Date().toISOString(),
      services: { neo4j: false, azure_openai: false },
      error: 'Method not allowed'
    });
  }

  try {
    console.log(`Attempting to connect to backend at: ${BACKEND_URL}/health`);
    
    // Proxy request to backend
    const backendResponse = await fetch(`${BACKEND_URL}/health`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      // Add timeout to prevent hanging
      signal: AbortSignal.timeout(5000)
    });
    
    if (!backendResponse.ok) {
      throw new Error(`Backend responded with status: ${backendResponse.status}`);
    }
    
    const backendData = await backendResponse.json();
    console.log('Backend health response:', backendData);
    
    // Transform backend response to frontend format
    const isHealthy = backendData.status === 'healthy' || backendData.status === 'degraded';
    
    res.status(isHealthy ? 200 : 503).json({
      status: isHealthy ? 'healthy' : 'unhealthy',
      timestamp: backendData.timestamp,
      services: {
        neo4j: backendData.dependencies?.neo4j === 'healthy',
        azure_openai: backendData.dependencies?.azure_openai === 'healthy'
      }
    });

  } catch (error) {
    console.error('Health check error:', error);
    console.error('Backend URL being used:', BACKEND_URL);
    res.status(503).json({
      status: 'unhealthy',
      timestamp: new Date().toISOString(),
      services: { neo4j: false, azure_openai: false },
      error: error instanceof Error ? error.message : 'Unknown error'
    });
  }
}
