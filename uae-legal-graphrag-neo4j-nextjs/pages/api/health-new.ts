import type { NextApiRequest, NextApiResponse } from 'next';
import { healthCheck } from '../../lib/graph/neo4j';
import { getConfig } from '../../lib/config';

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
    // Test configuration availability
    let azureConfigOk = false;
    try {
      getConfig();
      azureConfigOk = true;
    } catch {
      azureConfigOk = false;
    }

    // Test Neo4j connectivity
    const neo4jOk = await healthCheck();
    
    const isHealthy = neo4jOk && azureConfigOk;
    
    res.status(isHealthy ? 200 : 503).json({
      status: isHealthy ? 'healthy' : 'unhealthy',
      timestamp: new Date().toISOString(),
      services: {
        neo4j: neo4jOk,
        azure_openai: azureConfigOk
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
