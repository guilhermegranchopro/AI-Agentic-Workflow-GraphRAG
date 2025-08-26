import { NextApiRequest, NextApiResponse } from 'next';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

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
    // Proxy request to backend
    const backendResponse = await fetch(`${BACKEND_URL}/health`);
    const backendData = await backendResponse.json();
    
    // Transform backend response to frontend format
    const isHealthy = backendData.status === 'healthy';
    
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
    res.status(503).json({
      status: 'unhealthy',
      timestamp: new Date().toISOString(),
      services: { neo4j: false, azure_openai: false },
      error: error instanceof Error ? error.message : 'Unknown error'
    });
  }
}
