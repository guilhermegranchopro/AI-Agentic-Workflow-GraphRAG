import type { NextApiRequest, NextApiResponse } from 'next';
import { exec } from 'child_process';
import { promisify } from 'util';
import path from 'path';

const execAsync = promisify(exec);

interface DatabaseStats {
  total_documents: number;
  total_entities: number;
  total_relationships: number;
  communities: number;
  last_updated: string;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<DatabaseStats | { error: string }>
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const pythonBackendPath = path.join(process.cwd(), 'python-backend');
    
    const statsCommand = `cd "${pythonBackendPath}" && python -c "
import sys
import json
sys.path.append('.')
from db import db
from graph.queries import get_database_statistics

try:
    with db.get_driver() as driver:
        stats = get_database_statistics(driver)
        print(json.dumps(stats))
except Exception as e:
    print(json.dumps({'error': str(e)}))
"`;

    const result = await execAsync(statsCommand);
    const stats = JSON.parse(result.stdout.trim());

    if (stats.error) {
      return res.status(500).json({ error: stats.error });
    }

    // Format the response with default values if needed
    const formattedStats: DatabaseStats = {
      total_documents: stats.total_documents || 0,
      total_entities: stats.total_entities || 0,
      total_relationships: stats.total_relationships || 0,
      communities: stats.communities || 0,
      last_updated: stats.last_updated || new Date().toISOString()
    };

    res.status(200).json(formattedStats);

  } catch (error) {
    console.error('Database stats error:', error);
    res.status(500).json({ 
      error: 'Failed to fetch database statistics' 
    });
  }
}
