import { NextApiRequest, NextApiResponse } from 'next';
import { neo4jDriver } from '../../lib/graph/neo4j';
import { hasNeo4jConfig, hasAzureOpenAIConfig } from '../../lib/config';

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
    const neo4jConfigOk = hasNeo4jConfig();
    const azureConfigOk = hasAzureOpenAIConfig();

    // Test Neo4j connectivity (only if config is available)
    let neo4jOk = false;
    if (neo4jConfigOk) {
      try {
        neo4jOk = await neo4jDriver.healthCheck();
      } catch {
        neo4jOk = false;
      }
    }
    
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
