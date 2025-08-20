import type { NextApiRequest, NextApiResponse } from "next";
import { readNeo4jEnv, readAzureOpenAIEnv, getConfigKeys } from "../../../lib/config";

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

  try {
    const neo4jEnv = readNeo4jEnv();
    const azureEnv = readAzureOpenAIEnv();
    
    const neo4jPresent = {
      NEO4J_URI: !!neo4jEnv.NEO4J_URI,
      NEO4J_USERNAME: !!neo4jEnv.NEO4J_USERNAME,
      NEO4J_PASSWORD: !!neo4jEnv.NEO4J_PASSWORD,
    };
    
    const azurePresent = {
      AZURE_OPENAI_API_KEY: !!azureEnv.AZURE_OPENAI_API_KEY,
      AZURE_OPENAI_ENDPOINT: !!azureEnv.AZURE_OPENAI_ENDPOINT,
      AZURE_OPENAI_DEPLOYMENT: !!azureEnv.AZURE_OPENAI_DEPLOYMENT,
      AZURE_OPENAI_API_VERSION: !!azureEnv.AZURE_OPENAI_API_VERSION,
    };
    
    const allPresent = { ...neo4jPresent, ...azurePresent };
    const allConfigured = Object.values(allPresent).every(Boolean);
    
    res.status(200).json({ 
      ok: allConfigured, 
      present: allPresent,
      groups: {
        neo4j: neo4jPresent,
        azure_openai: azurePresent
      },
      message: allConfigured ? "All environment variables configured" : "Some environment variables missing"
    });
  } catch (e: any) {
    res.status(200).json({ 
      ok: false, 
      message: e.message, 
      present: {},
      groups: { neo4j: {}, azure_openai: {} }
    });
  }
}
