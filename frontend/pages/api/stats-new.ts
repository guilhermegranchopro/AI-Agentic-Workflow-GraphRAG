import type { NextApiRequest, NextApiResponse } from 'next';

interface DatabaseStats {
  total_documents: number;
  total_entities: number;
  total_relationships: number;
  communities: number;
  last_updated: string;
}

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<DatabaseStats | { error: string }>
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Return mock database statistics
    const stats: DatabaseStats = {
      total_documents: 1247,
      total_entities: 8934,
      total_relationships: 15627,
      communities: 42,
      last_updated: new Date().toISOString()
    };
    
    res.status(200).json(stats);
  } catch (error) {
    console.error('Stats API error:', error);
    res.status(500).json({ 
      error: 'Failed to fetch database statistics'
    });
  }
}
