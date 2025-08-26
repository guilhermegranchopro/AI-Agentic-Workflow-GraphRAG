import type { NextApiRequest, NextApiResponse } from "next";
import { readNeo4jEnv, readAzureOpenAIEnv } from "../../../lib/config";

interface DebugResponse {
  neo4j: {
    configured: boolean;
    variables: Record<string, boolean>;
  };
  azure: {
    configured: boolean;
    variables: Record<string, boolean>;
  };
  timestamp: string;
}

export default function handler(req: NextApiRequest, res: NextApiResponse<DebugResponse>) {
  if (req.method !== 'GET') {
    return res.status(405).json({
      neo4j: { configured: false, variables: {} },
      azure: { configured: false, variables: {} },
      timestamp: new Date().toISOString()
    });
  }

  try {
    const neo4jEnv = readNeo4jEnv();
    const azureEnv = readAzureOpenAIEnv();
    
    const neo4jVariables = {
      NEO4J_URI: !!neo4jEnv.NEO4J_URI,
      NEO4J_USERNAME: !!neo4jEnv.NEO4J_USERNAME,
      NEO4J_PASSWORD: !!neo4jEnv.NEO4J_PASSWORD,
    };
    
    const azureVariables = {
      AZURE_OPENAI_API_KEY: !!azureEnv.AZURE_OPENAI_API_KEY,
      AZURE_OPENAI_ENDPOINT: !!azureEnv.AZURE_OPENAI_ENDPOINT,
      AZURE_OPENAI_DEPLOYMENT: !!azureEnv.AZURE_OPENAI_DEPLOYMENT,
      AZURE_OPENAI_API_VERSION: !!azureEnv.AZURE_OPENAI_API_VERSION,
    };
    
    res.status(200).json({
      neo4j: {
        configured: Object.values(neo4jVariables).every(Boolean),
        variables: neo4jVariables
      },
      azure: {
        configured: Object.values(azureVariables).every(Boolean),
        variables: azureVariables
      },
      timestamp: new Date().toISOString()
    });
  } catch (e: any) {
    res.status(500).json({
      neo4j: { configured: false, variables: {} },
      azure: { configured: false, variables: {} },
      timestamp: new Date().toISOString()
    });
  }
}
