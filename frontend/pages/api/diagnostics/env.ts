import { NextApiRequest, NextApiResponse } from 'next';
import { hasNeo4jConfig, hasAzureOpenAIConfig } from '../../../lib/config';

interface DiagnosticsResponse {
  ok: boolean;
  message?: string;
  present: Record<string, boolean>;
  groups: {
    neo4j: Record<string, boolean>;
    azure_openai: Record<string, boolean>;
  };
}

export default function handler(req: NextApiRequest, res: NextApiResponse<DiagnosticsResponse>) {
  if (req.method !== 'GET') {
    return res.status(405).json({ 
      ok: false, 
      message: 'Method not allowed',
      present: {},
      groups: { neo4j: {}, azure_openai: {} }
    });
  }

  // Check individual environment variables
  const present = {
    NEO4J_URI: !!process.env.NEO4J_URI,
    NEO4J_USERNAME: !!process.env.NEO4J_USERNAME,
    NEO4J_PASSWORD: !!process.env.NEO4J_PASSWORD,
    NEO4J_DATABASE: !!process.env.NEO4J_DATABASE,
    AZURE_OPENAI_API_KEY: !!process.env.AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT: !!process.env.AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_DEPLOYMENT: !!process.env.AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_API_VERSION: !!process.env.AZURE_OPENAI_API_VERSION,
  };

  // Check grouped configurations
  const groups = {
    neo4j: {
      configured: hasNeo4jConfig(),
      uri: !!process.env.NEO4J_URI,
      username: !!process.env.NEO4J_USERNAME,
      password: !!process.env.NEO4J_PASSWORD,
      database: !!process.env.NEO4J_DATABASE,
    },
    azure_openai: {
      configured: hasAzureOpenAIConfig(),
      api_key: !!process.env.AZURE_OPENAI_API_KEY,
      endpoint: !!process.env.AZURE_OPENAI_ENDPOINT,
      deployment: !!process.env.AZURE_OPENAI_DEPLOYMENT,
      api_version: !!process.env.AZURE_OPENAI_API_VERSION,
    }
  };

  const allConfigured = groups.neo4j.configured && groups.azure_openai.configured;

  res.status(200).json({
    ok: allConfigured,
    message: allConfigured ? 'All configurations present' : 'Some configurations missing',
    present,
    groups
  });
}
