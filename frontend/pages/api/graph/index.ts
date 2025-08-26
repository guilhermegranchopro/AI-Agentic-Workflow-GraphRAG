import { NextApiRequest, NextApiResponse } from 'next';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export const config = {
  runtime: 'nodejs',
};

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // For now, return mock data since Neo4j is not configured
    const mockGraphData = {
      nodes: [
        {
          id: "1",
          label: "UAE Civil Code",
          type: "Law",
          properties: { title: "UAE Civil Code", year: 1985 }
        },
        {
          id: "2", 
          label: "Commercial Code",
          type: "Law",
          properties: { title: "Commercial Code", year: 1993 }
        },
        {
          id: "3",
          label: "Labor Law",
          type: "Law", 
          properties: { title: "Labor Law", year: 1980 }
        }
      ],
      edges: [
        {
          id: "edge_1",
          from: "1",
          to: "2",
          label: "CITES",
          type: "CITES",
          properties: {}
        },
        {
          id: "edge_2", 
          from: "2",
          to: "3",
          label: "AMENDED_BY",
          type: "AMENDED_BY",
          properties: {}
        }
      ],
      stats: {
        nodeCount: 3,
        edgeCount: 2,
        nodeTypes: { "Law": 3 },
        edgeTypes: { "CITES": 1, "AMENDED_BY": 1 }
      }
    };
    
    res.status(200).json(mockGraphData);
  } catch (error) {
    console.error('Graph API error:', error);
    res.status(500).json({ 
      error: error instanceof Error ? error.message : 'Failed to fetch graph data',
      nodes: [],
      edges: [],
      stats: {
        nodeCount: 0,
        edgeCount: 0,
        nodeTypes: {},
        edgeTypes: {}
      }
    });
  }
}
