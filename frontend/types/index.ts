// Type definitions for UAE Legal GraphRAG application

export interface SearchResult {
  id: string;
  content: string;
  score: number;
  metadata: {
    type: string;
    source: string;
    date?: string;
    [key: string]: any;
  };
}

export interface CitationSource {
  id: string;
  title: string;
  content: string;
  type: 'law' | 'regulation' | 'case' | 'article';
  date?: string;
  url?: string;
  relevanceScore: number;
}

export interface GraphNode {
  id: string;
  label: string;
  type: string;
  properties: Record<string, any>;
  group?: number;
}

export interface GraphEdge {
  from: string;
  to: string;
  label: string;
  type: string;
  weight?: number;
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface RAGResponse {
  response: string;
  sources: CitationSource[];
  confidence: number;
  strategy_used: 'local' | 'global' | 'drift' | 'hybrid';
  metadata?: {
    query_time: number;
    total_sources: number;
    [key: string]: any;
  };
}

export interface AgentResponse {
  response: string;
  agent_used: string;
  sources: CitationSource[];
  confidence: number;
  reasoning?: string;
  metadata?: Record<string, any>;
}

export interface DatabaseStats {
  total_documents: number;
  total_entities: number;
  total_relationships: number;
  communities: number;
  last_updated: string;
}

export interface HealthCheck {
  status: 'healthy' | 'unhealthy';
  database: boolean;
  embeddings: boolean;
  ai_service: boolean;
  message?: string;
}

export interface SearchFilters {
  dateFrom?: string;
  dateTo?: string;
  documentType?: string[];
  jurisdiction?: string[];
  maxResults?: number;
}

export interface PathResult {
  path: GraphNode[];
  relationships: GraphEdge[];
  score: number;
  summary: string;
}

export interface CommunityInfo {
  id: string;
  title: string;
  summary: string;
  size: number;
  relevance_score: number;
  key_entities: string[];
}

export interface DriftResult {
  communities: CommunityInfo[];
  local_results: SearchResult[];
  combined_summary: string;
  confidence: number;
}
