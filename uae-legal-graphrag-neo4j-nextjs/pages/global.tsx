import React, { useState } from 'react';
import Layout from '@/components/Layout';
import { Globe, Search, Filter, Clock, FileText, Users } from 'lucide-react';

interface CommunityInfo {
  id: string;
  title: string;
  summary: string;
  size: number;
  relevance_score: number;
}

interface SearchResult {
  id: string;
  title: string;
  content: string;
  type: string;
  relevanceScore: number;
}

interface GlobalRAGResponse {
  response: string;
  sources: SearchResult[];
  confidence: number;
  communities?: CommunityInfo[];
  metadata?: {
    query_time: number;
    total_sources: number;
  };
}

const GlobalRAGPage: React.FC = () => {
  const [query, setQuery] = useState('');
  const [maxResults, setMaxResults] = useState(5);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<GlobalRAGResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('/api/global-rag', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query.trim(),
          maxResults,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Search failed');
      }

      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSearch();
    }
  };

  return (
    <Layout title="Global RAG - UAE Legal GraphRAG">
      <div className="animate-fade-in">
        <div className="mb-8">
          <div className="flex items-center space-x-3 mb-4">
            <Globe className="h-8 w-8 text-primary-600" />
            <h1 className="text-3xl font-bold text-gray-900">Global RAG</h1>
          </div>
          <p className="text-lg text-gray-600">
            Community-based analysis using Graph Data Science for comprehensive insights
          </p>
          <div className="mt-4 bg-green-50 border border-green-200 rounded-lg p-4">
            <p className="text-green-800 text-sm">
              <strong>How it works:</strong> Query → Community Detection → Louvain Analysis → Global Synthesis
            </p>
          </div>
        </div>

        {/* Search Interface */}
        <div className="card mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-6">🌐 Global Legal Analysis</h2>
          
          <div className="space-y-6">
            {/* Query Input */}
            <div>
              <label htmlFor="query" className="block text-sm font-medium text-gray-700 mb-2">
                Legal Query
              </label>
              <textarea
                id="query"
                className="textarea-field h-24"
                placeholder="Enter your legal question for comprehensive community-based analysis"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={handleKeyPress}
              />
            </div>

            {/* Max Results */}
            <div className="w-full md:w-64">
              <label htmlFor="maxResults" className="block text-sm font-medium text-gray-700 mb-2">
                <Filter className="inline h-4 w-4 mr-1" />
                Max Results
              </label>
              <select
                id="maxResults"
                className="select-field"
                value={maxResults}
                onChange={(e) => setMaxResults(parseInt(e.target.value))}
              >
                <option value={3}>3 results</option>
                <option value={5}>5 results</option>
                <option value={10}>10 results</option>
                <option value={15}>15 results</option>
              </select>
            </div>

            {/* Search Button */}
            <div>
              <button
                onClick={handleSearch}
                disabled={loading || !query.trim()}
                className="btn-primary w-full md:w-auto px-8 py-3 text-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    <span>Analyzing Communities...</span>
                  </>
                ) : (
                  <>
                    <Search className="h-5 w-5" />
                    <span>Analyze Global Context</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="card border-red-200 bg-red-50 mb-8">
            <div className="flex items-center space-x-2">
              <div className="h-4 w-4 bg-red-500 rounded-full"></div>
              <h3 className="text-lg font-semibold text-red-800">Error</h3>
            </div>
            <p className="mt-2 text-red-700">{error}</p>
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="space-y-8">
            {/* Answer */}
            <div className="card">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">🌐 Global Analysis</h3>
                <div className="flex items-center space-x-4 text-sm text-gray-500">
                  <div className="flex items-center space-x-1">
                    <Clock className="h-4 w-4" />
                    <span>{result.metadata?.query_time?.toFixed(2) || '0'}s</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <span>Confidence: {Math.round((result.confidence || 0) * 100)}%</span>
                  </div>
                </div>
              </div>
              <div className="prose max-w-none">
                <p className="text-gray-800 leading-relaxed">{result.response}</p>
              </div>
            </div>

            {/* Communities */}
            {result.communities && result.communities.length > 0 && (
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  🏘️ Relevant Communities ({result.communities.length})
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {result.communities.map((community, index) => (
                    <div key={community.id || index} className="bg-green-50 border border-green-200 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          <Users className="h-4 w-4 text-green-600" />
                          <h4 className="font-medium text-green-900">
                            {community.title || `Community ${index + 1}`}
                          </h4>
                        </div>
                        <div className="flex items-center space-x-2 text-xs text-green-600">
                          <span>Size: {community.size}</span>
                          <span>Relevance: {(community.relevance_score * 100).toFixed(1)}%</span>
                        </div>
                      </div>
                      <p className="text-sm text-green-700 leading-relaxed">
                        {community.summary}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Sources */}
            {result.sources && result.sources.length > 0 && (
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  📚 Supporting Sources ({result.sources.length})
                </h3>
                <div className="space-y-4">
                  {result.sources.map((source, index) => (
                    <div key={source.id || index} className="citation-card">
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          <FileText className="h-4 w-4 text-blue-600" />
                          <h4 className="font-medium text-blue-900">
                            {source.title || `Source ${index + 1}`}
                          </h4>
                        </div>
                        <div className="flex items-center space-x-2 text-xs text-gray-500">
                          <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded">
                            {source.type}
                          </span>
                          <span>Score: {(source.relevanceScore * 100).toFixed(1)}%</span>
                        </div>
                      </div>
                      <p className="text-sm text-gray-700 leading-relaxed">
                        {source.content}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Metadata */}
            {result.metadata && (
              <div className="card bg-gray-50">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">🔍 Analysis Metadata</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  <div>
                    <span className="text-gray-500">Query Time:</span>
                    <p className="font-medium">{result.metadata.query_time?.toFixed(3)}s</p>
                  </div>
                  <div>
                    <span className="text-gray-500">Total Sources:</span>
                    <p className="font-medium">{result.metadata.total_sources}</p>
                  </div>
                  <div>
                    <span className="text-gray-500">Communities:</span>
                    <p className="font-medium">{result.communities?.length || 0}</p>
                  </div>
                  <div>
                    <span className="text-gray-500">Strategy:</span>
                    <p className="font-medium">Global RAG</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </Layout>
  );
};

export default GlobalRAGPage;
