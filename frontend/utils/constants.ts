// Application Constants
export const APP_CONFIG = {
  name: 'UAE Legal GraphRAG',
  version: '1.0.0',
  description: 'Advanced legal research with GraphRAG and AI agents',
  author: 'Guilherme Grancho - EY Portugal',
} as const;

// API Endpoints
export const API_ENDPOINTS = {
  HEALTH: '/api/health',
  GRAPH: '/api/graph',
  STATS: '/api/stats-new',
  ASSISTANT: '/api/assistant',
  ANALYSIS: '/api/analysis',
} as const;

// UI Constants
export const UI_CONFIG = {
  ANIMATION_DURATION: 300,
  DEBOUNCE_DELAY: 500,
  MAX_RETRIES: 3,
} as const;

// Graph Visualization
export const GRAPH_CONFIG = {
  DEFAULT_NODE_LIMIT: 150,
  MAX_NODE_LIMIT: 300,
  DEFAULT_PHYSICS_ENABLED: true,
};

// Agent Types
export const AGENT_TYPES = {
  LOCAL: 'local',
  GLOBAL: 'global', 
  DRIFT: 'drift',
  HYBRID: 'hybrid',
} as const;

// Node Colors for Graph Visualization
export const NODE_COLORS = {
  CONCEPT: '#8B5CF6', // Purple
  DOCUMENT: '#06B6D4', // Cyan
  LAW: '#EF4444', // Red
  ENTITY: '#10B981', // Green
  DEFAULT: '#6B7280', // Gray
} as const;
