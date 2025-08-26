import { NextApiRequest, NextApiResponse } from 'next';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

interface GraphNode {
  id: string;
  label: string;
  type: string;
  properties?: Record<string, any>;
}

interface GraphEdge {
  id: string;
  from: string;
  to: string;
  label: string;
  type: string;
  properties?: Record<string, any>;
}

interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
  stats: {
    nodeCount: number;
    edgeCount: number;
    nodeTypes: Record<string, number>;
    edgeTypes: Record<string, number>;
  };
}

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
        },
        {
          id: "4",
          label: "Criminal Code",
          type: "Law",
          properties: { title: "Criminal Code", year: 1987 }
        },
        {
          id: "5",
          label: "Constitution",
          type: "Constitutional",
          properties: { title: "UAE Constitution", year: 1971 }
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
        },
        {
          id: "edge_3",
          from: "5",
          to: "1",
          label: "ESTABLISHES",
          type: "ESTABLISHES",
          properties: {}
        },
        {
          id: "edge_4",
          from: "1",
          to: "4",
          label: "INTERPRETED_BY",
          type: "INTERPRETED_BY",
          properties: {}
        }
      ],
      stats: {
        nodeCount: 5,
        edgeCount: 4,
        nodeTypes: { "Law": 4, "Constitutional": 1 },
        edgeTypes: { "CITES": 1, "AMENDED_BY": 1, "ESTABLISHES": 1, "INTERPRETED_BY": 1 }
      }
    };
    
    res.status(200).json(mockGraphData);
  } catch (error) {
    console.error('Graph data error:', error);
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


