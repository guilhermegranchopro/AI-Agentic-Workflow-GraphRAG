import { NextApiRequest, NextApiResponse } from 'next';
import { getGraphData } from '../../../lib/graph/graphRag';

export const config = {
  runtime: 'nodejs',
};

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const graphData = await getGraphData();
    
    res.status(200).json({
      nodes: graphData.nodes,
      edges: graphData.edges,
      stats: {
        nodeCount: graphData.nodes.length,
        edgeCount: graphData.edges.length,
        timestamp: new Date().toISOString()
      }
    });

  } catch (error) {
    console.error('Graph API error:', error);
    
    // Check if it's a Neo4j configuration error
    if (error instanceof Error && error.message.includes('Missing Neo4j env')) {
      return res.status(503).json({ 
        error: 'Neo4j service configuration incomplete',
        message: 'Neo4j environment variables not configured. Please check your .env file.',
        details: error.message,
        present: (error as any).present ?? {}
      });
    }
    
    res.status(500).json({ 
      error: 'Failed to fetch graph data',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  }
}
