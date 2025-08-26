import type { NextApiRequest, NextApiResponse } from "next";
import { getNeo4jConfig } from "../../../lib/config";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Test Neo4j configuration
    const config = getNeo4jConfig();
    
    // Just test if we can get a driver (don't actually connect)
    const { default: Neo4jSingleton } = await import('../../../lib/graph/neo4j');
    
    res.status(200).json({ 
      status: 'Neo4j configuration valid',
      hasCredentials: true,
      uri: config.NEO4J_URI ? config.NEO4J_URI.substring(0, 20) + '...' : 'not set'
    });
  } catch (error) {
    console.error('Neo4j config test error:', error);
    
    if (error instanceof Error && error.message.includes('Missing Neo4j env')) {
      return res.status(503).json({ 
        error: 'Neo4j configuration incomplete',
        message: error.message,
        present: (error as any).present ?? {}
      });
    }
    
    res.status(500).json({ 
      error: 'Neo4j configuration test failed',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  }
}
