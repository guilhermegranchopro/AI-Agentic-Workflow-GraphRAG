import type { NextApiRequest, NextApiResponse } from 'next';
import { healthCheck } from '../../lib/graph/neo4j';
import { readNeo4jEnv, readAzureOpenAIEnv } from '../../lib/config';

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
    const neo4jEnv = readNeo4jEnv();
    const azureEnv = readAzureOpenAIEnv();
    
    const neo4jConfigOk = !!(neo4jEnv.NEO4J_URI && neo4jEnv.NEO4J_USERNAME && neo4jEnv.NEO4J_PASSWORD);
    const azureConfigOk = !!(azureEnv.AZURE_OPENAI_API_KEY && azureEnv.AZURE_OPENAI_ENDPOINT && azureEnv.AZURE_OPENAI_DEPLOYMENT);

    // Test Neo4j connectivity (only if config is available)
    let neo4jOk = false;
    if (neo4jConfigOk) {
      try {
        neo4jOk = await healthCheck();
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
