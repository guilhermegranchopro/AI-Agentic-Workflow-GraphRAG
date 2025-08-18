import React, { useState } from 'react';
import Layout from '@/components/Layout';
import { TrendingUp, Search, MapPin, Clock, Users, LineChart } from 'lucide-react';

interface TimeContext {
  period: string;
  events: string[];
  relevance: number;
}

interface EntityEvolution {
  entity: string;
  timeline: {
    period: string;
    status: string;
    context: string;
  }[];
}

interface DriftAnalysis {
  response: string;
  temporal_insights: string[];
  confidence: number;
  time_contexts?: TimeContext[];
  entity_evolution?: EntityEvolution[];
  metadata?: {
    query_time: number;
    periods_analyzed: number;
    drift_detected: boolean;
  };
}

const DriftRAGPage: React.FC = () => {
  const [query, setQuery] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [maxResults, setMaxResults] = useState(5);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<DriftAnalysis | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('/api/drift-rag', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query.trim(),
          start_date: startDate || undefined,
          end_date: endDate || undefined,
          maxResults,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Analysis failed');
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
      handleAnalyze();
    }
  };

  return (
    <Layout title="DRIFT RAG - UAE Legal GraphRAG">
      <div className="animate-fade-in">
        <div className="mb-8">
          <div className="flex items-center space-x-3 mb-4">
            <TrendingUp className="h-8 w-8 text-purple-600" />
            <h1 className="text-3xl font-bold text-gray-900">DRIFT RAG</h1>
          </div>
          <p className="text-lg text-gray-600">
            Dynamic temporal analysis for tracking legal evolution and entity drift
          </p>
          <div className="mt-4 bg-purple-50 border border-purple-200 rounded-lg p-4">
            <p className="text-purple-800 text-sm">
              <strong>DRIFT:</strong> Dynamic Retrieval with Intelligent Temporal Filtering for legal timeline analysis
            </p>
          </div>
        </div>

        {/* Analysis Interface */}
        <div className="card mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-6">📈 Temporal Legal Analysis</h2>
          
          <div className="space-y-6">
            {/* Query Input */}
            <div>
              <label htmlFor="query" className="block text-sm font-medium text-gray-700 mb-2">
                Legal Query for Temporal Analysis
              </label>
              <textarea
                id="query"
                className="textarea-field h-24"
                placeholder="Enter your legal question to analyze temporal changes and evolution"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={handleKeyPress}
              />
            </div>

            {/* Date Range */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="startDate" className="block text-sm font-medium text-gray-700 mb-2">
                  <MapPin className="inline h-4 w-4 mr-1" />
                  Start Date (optional)
                </label>
                <input
                  type="date"
                  id="startDate"
                  className="input-field"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                />
              </div>
              <div>
                <label htmlFor="endDate" className="block text-sm font-medium text-gray-700 mb-2">
                  <MapPin className="inline h-4 w-4 mr-1" />
                  End Date (optional)
                </label>
                <input
                  type="date"
                  id="endDate"
                  className="input-field"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                />
              </div>
            </div>

            {/* Max Results */}
            <div className="w-full md:w-64">
              <label htmlFor="maxResults" className="block text-sm font-medium text-gray-700 mb-2">
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

            {/* Analyze Button */}
            <div>
              <button
                onClick={handleAnalyze}
                disabled={loading || !query.trim()}
                className="btn-primary w-full md:w-auto px-8 py-3 text-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    <span>Analyzing Temporal Patterns...</span>
                  </>
                ) : (
                  <>
                    <TrendingUp className="h-5 w-5" />
                    <span>Analyze Temporal Drift</span>
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
            {/* Analysis Response */}
            <div className="card">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">📈 Temporal Analysis</h3>
                <div className="flex items-center space-x-4 text-sm text-gray-500">
                  <div className="flex items-center space-x-1">
                    <Clock className="h-4 w-4" />
                    <span>{result.metadata?.query_time?.toFixed(2) || '0'}s</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <span>Confidence: {Math.round((result.confidence || 0) * 100)}%</span>
                  </div>
                  {result.metadata?.drift_detected && (
                    <div className="flex items-center space-x-1">
                      <div className="h-2 w-2 bg-purple-500 rounded-full animate-pulse"></div>
                      <span className="text-purple-600 font-medium">Drift Detected</span>
                    </div>
                  )}
                </div>
              </div>
              <div className="prose max-w-none">
                <p className="text-gray-800 leading-relaxed">{result.response}</p>
              </div>
            </div>

            {/* Temporal Insights */}
            {result.temporal_insights && result.temporal_insights.length > 0 && (
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  🔍 Temporal Insights
                </h3>
                <div className="space-y-3">
                  {result.temporal_insights.map((insight, index) => (
                    <div key={index} className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                      <div className="flex items-start space-x-2">
                        <LineChart className="h-4 w-4 text-purple-600 mt-1" />
                        <p className="text-purple-800 text-sm leading-relaxed">{insight}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Time Contexts */}
            {result.time_contexts && result.time_contexts.length > 0 && (
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  📅 Time Contexts ({result.time_contexts.length})
                </h3>
                <div className="space-y-4">
                  {result.time_contexts.map((context, index) => (
                    <div key={index} className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-medium text-blue-900">{context.period}</h4>
                        <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                          Relevance: {(context.relevance * 100).toFixed(1)}%
                        </span>
                      </div>
                      <div className="space-y-2">
                        {context.events.map((event, eventIndex) => (
                          <div key={eventIndex} className="flex items-start space-x-2">
                            <div className="h-2 w-2 bg-blue-400 rounded-full mt-2"></div>
                            <p className="text-sm text-blue-700">{event}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Entity Evolution */}
            {result.entity_evolution && result.entity_evolution.length > 0 && (
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  🏛️ Entity Evolution Timeline
                </h3>
                <div className="space-y-6">
                  {result.entity_evolution.map((evolution, index) => (
                    <div key={index} className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                      <div className="flex items-center space-x-2 mb-4">
                        <Users className="h-5 w-5 text-gray-600" />
                        <h4 className="font-medium text-gray-900">{evolution.entity}</h4>
                      </div>
                      <div className="space-y-3">
                        {evolution.timeline.map((timepoint, timeIndex) => (
                          <div key={timeIndex} className="flex items-start space-x-4 p-3 bg-white rounded border">
                            <div className="flex-shrink-0">
                              <div className="h-3 w-3 bg-purple-400 rounded-full mt-1"></div>
                            </div>
                            <div className="flex-grow">
                              <div className="flex items-center space-x-2 mb-1">
                                <span className="text-sm font-medium text-gray-900">{timepoint.period}</span>
                                <span className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
                                  {timepoint.status}
                                </span>
                              </div>
                              <p className="text-sm text-gray-600">{timepoint.context}</p>
                            </div>
                          </div>
                        ))}
                      </div>
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
                    <span className="text-gray-500">Periods Analyzed:</span>
                    <p className="font-medium">{result.metadata.periods_analyzed}</p>
                  </div>
                  <div>
                    <span className="text-gray-500">Drift Detection:</span>
                    <p className="font-medium">
                      {result.metadata.drift_detected ? 
                        <span className="text-purple-600">Active</span> : 
                        <span className="text-gray-600">None</span>
                      }
                    </p>
                  </div>
                  <div>
                    <span className="text-gray-500">Strategy:</span>
                    <p className="font-medium">DRIFT RAG</p>
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

export default DriftRAGPage;
