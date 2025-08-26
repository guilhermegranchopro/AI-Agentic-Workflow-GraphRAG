import React, { useState, useRef, useEffect } from 'react';
import Layout from '@/components/Layout';
import Container from '@/components/ui/Container';
import { Search, AlertTriangle, CheckCircle, XCircle, Clock, FileText, Download, Copy, Eye } from 'lucide-react';
import { AnalysisRequest, AnalysisResult, Contradiction, Harmonisation, Severity, AnalysisProgressEvent } from '@/lib/ai/analysis/types';
import { generateId } from '@/utils/helpers';

interface AnalysisState {
  isRunning: boolean;
  progress: number;
  stage: string;
  message: string;
  result: AnalysisResult | null;
  findings: Contradiction[];
  suggestions: Harmonisation[];
  logs: Array<{id: string, message: string, timestamp: Date, type: 'info' | 'finding' | 'suggestion'}>;
}

const AIAnalysisPage: React.FC = () => {
  const [analysisState, setAnalysisState] = useState<AnalysisState>({
    isRunning: false,
    progress: 0,
    stage: '',
    message: '',
    result: null,
    findings: [],
    suggestions: [],
    logs: []
  });

  const [formData, setFormData] = useState<AnalysisRequest>({
    query: '',
    scope: 'all',
    maxFindings: 10
  });

  const [selectedContradiction, setSelectedContradiction] = useState<Contradiction | null>(null);
  const [showSidePanel, setShowSidePanel] = useState(false);

  const logsEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottomLogs = () => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottomLogs();
  }, [analysisState.logs]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.query.trim()) return;

    // Reset state
    setAnalysisState({
      isRunning: true,
      progress: 0,
      stage: 'initializing',
      message: 'Starting analysis...',
      result: null,
      findings: [],
      suggestions: [],
      logs: [{
        id: generateId(),
        message: 'Analysis started',
        timestamp: new Date(),
        type: 'info'
      }]
    });

    try {
      // Update progress
      setAnalysisState(prev => ({
        ...prev,
        progress: 25,
        stage: 'searching',
        message: 'Searching knowledge graph for contradictions...',
        logs: [...prev.logs, {
          id: generateId(),
          message: 'Searching knowledge graph for contradictions...',
          timestamp: new Date(),
          type: 'info'
        }]
      }));

      await new Promise(resolve => setTimeout(resolve, 1000));

      setAnalysisState(prev => ({
        ...prev,
        progress: 50,
        stage: 'analyzing',
        message: 'Analyzing legal contradictions and generating recommendations...',
        logs: [...prev.logs, {
          id: generateId(),
          message: 'Analyzing legal contradictions and generating recommendations...',
          timestamp: new Date(),
          type: 'info'
        }]
      }));

      await new Promise(resolve => setTimeout(resolve, 1000));

      setAnalysisState(prev => ({
        ...prev,
        progress: 75,
        stage: 'finalizing',
        message: 'Finalizing analysis results...',
        logs: [...prev.logs, {
          id: generateId(),
          message: 'Finalizing analysis results...',
          timestamp: new Date(),
          type: 'info'
        }]
      }));

      await new Promise(resolve => setTimeout(resolve, 500));

      // Make the API call
      const response = await fetch('/api/analysis', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error(`Analysis request failed: ${response.status}`);
      }

      const analysisResult = await response.json();

      // Update state with results
      setAnalysisState(prev => ({
        ...prev,
        isRunning: false,
        progress: 100,
        stage: 'complete',
        message: 'Analysis complete',
        result: analysisResult,
        findings: analysisResult.contradictions || [],
        suggestions: analysisResult.recommendations || [],
        logs: [...prev.logs, {
          id: generateId(),
          message: `Analysis complete. Found ${analysisResult.contradictions?.length || 0} contradictions.`,
          timestamp: new Date(),
          type: 'info'
        }]
      }));

    } catch (error) {
      setAnalysisState(prev => ({
        ...prev,
        isRunning: false,
        message: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
        logs: [...prev.logs, {
          id: generateId(),
          message: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
          timestamp: new Date(),
          type: 'info'
        }]
      }));
    }
  };

  const handleAnalysisEvent = (event: AnalysisProgressEvent) => {
    const { type, data } = event;

    switch (type) {
      case 'progress':
        setAnalysisState(prev => ({
          ...prev,
          progress: data.pct || prev.progress,
          stage: data.stage || prev.stage,
          message: data.message || prev.message,
          logs: [...prev.logs, {
            id: generateId(),
            message: data.message || 'Progress update',
            timestamp: new Date(),
            type: 'info'
          }]
        }));
        break;

      case 'finding':
        if (data.contradiction) {
          setAnalysisState(prev => ({
            ...prev,
            findings: [...prev.findings, data.contradiction!],
            logs: [...prev.logs, {
              id: generateId(),
              message: `Found contradiction: ${data.contradiction!.title}`,
              timestamp: new Date(),
              type: 'finding'
            }]
          }));
        }
        break;

      case 'suggestion':
        if (data.harmonisation) {
          setAnalysisState(prev => ({
            ...prev,
            suggestions: [...prev.suggestions, data.harmonisation!],
            logs: [...prev.logs, {
              id: generateId(),
              message: `Generated harmonisation suggestion`,
              timestamp: new Date(),
              type: 'suggestion'
            }]
          }));
        }
        break;

      case 'done':
        if (data.result) {
          setAnalysisState(prev => ({
            ...prev,
            isRunning: false,
            progress: 100,
            result: data.result!,
            message: 'Analysis complete',
            logs: [...prev.logs, {
              id: generateId(),
              message: data.message || 'Analysis complete',
              timestamp: new Date(),
              type: 'info'
            }]
          }));
        }
        break;
    }
  };

  const getSeverityIcon = (severity: Severity) => {
    switch (severity) {
      case 'critical': return <XCircle className="h-4 w-4 text-red-500" />;
      case 'high': return <AlertTriangle className="h-4 w-4 text-orange-500" />;
      case 'medium': return <AlertTriangle className="h-4 w-4 text-yellow-500" />;
      case 'low': return <CheckCircle className="h-4 w-4 text-blue-500" />;
    }
  };

  const getSeverityColor = (severity: Severity) => {
    switch (severity) {
      case 'critical': return 'text-red-400 bg-red-900/30 border-red-500/30';
      case 'high': return 'text-orange-400 bg-orange-900/30 border-orange-500/30';
      case 'medium': return 'text-yellow-400 bg-yellow-900/30 border-yellow-500/30';
      case 'low': return 'text-blue-400 bg-blue-900/30 border-blue-500/30';
    }
  };

  const exportResults = () => {
    if (!analysisState.result) return;

    const data = {
      query: formData.query,
      timestamp: new Date().toISOString(),
      findings: analysisState.findings,
      suggestions: analysisState.suggestions,
      stats: analysisState.result.stats
    };

    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `legal-analysis-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const openContradictionDetails = (contradiction: Contradiction) => {
    setSelectedContradiction(contradiction);
    setShowSidePanel(true);
  };

  return (
    <Layout title="AI Analysis - Legal Contradiction Finder">
      <Container>
        <div className="flex min-h-full">
          {/* Main Content */}
          <div className={`flex-1 flex flex-col transition-all duration-300 ${showSidePanel ? 'mr-96' : ''}`}>
            {/* Header */}
            <div className="flex-shrink-0 mb-3 md:mb-4 lg:mb-6">
              <div className="flex items-center justify-between mb-2 md:mb-3 lg:mb-4">
                <div className="flex items-center space-x-2 md:space-x-3">
                  <AlertTriangle className="h-5 w-5 md:h-6 md:w-6 lg:h-8 lg:w-8 text-orange-400" />
                  <h1 className="text-xl md:text-2xl lg:text-3xl font-bold text-white">AI Analysis</h1>
              </div>
              {analysisState.result && (
                <button
                  onClick={exportResults}
                  className="flex items-center space-x-2 px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl"
                >
                  <Download className="h-4 w-4" />
                  <span>Export Results</span>
                </button>
              )}
            </div>
            <p className="text-sm md:text-base lg:text-lg text-gray-300 mb-3 md:mb-4 lg:mb-6 leading-relaxed">
              Automated legal analysis to find contradictions and suggest harmonising amendments
            </p>

            {/* Analysis Form */}
            <form onSubmit={handleSubmit} className="bg-gradient-to-r from-gray-900/50 to-gray-800/50 rounded-xl border border-purple-500/20 p-4 md:p-6 backdrop-blur-sm shadow-xl">
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-3 md:gap-4 mb-3 md:mb-4">
                <div className="lg:col-span-2">
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Analysis Query
                  </label>
                  <input
                    type="text"
                    value={formData.query}
                    onChange={(e) => setFormData(prev => ({ ...prev, query: e.target.value }))}
                    placeholder="e.g., contract formation requirements, penalty provisions, liability rules"
                    className="w-full px-3 md:px-4 py-3 bg-gray-800/80 border border-gray-600/50 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all duration-200 text-sm md:text-base"
                    disabled={analysisState.isRunning}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Legal Scope
                  </label>
                  <select
                    value={formData.scope}
                    onChange={(e) => setFormData(prev => ({ ...prev, scope: e.target.value as any }))}
                    className="w-full px-4 py-3 bg-gray-800/80 border border-gray-600/50 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all duration-200"
                    disabled={analysisState.isRunning}
                  >
                    <option value="all">All Areas</option>
                    <option value="criminal">Criminal Law</option>
                    <option value="civil">Civil Law</option>
                    <option value="commercial">Commercial Law</option>
                    <option value="family">Family Law</option>
                  </select>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <label className="text-sm text-gray-300">
                    Max Findings:
                    <input
                      type="number"
                      min="1"
                      max="20"
                      value={formData.maxFindings}
                      onChange={(e) => setFormData(prev => ({ ...prev, maxFindings: parseInt(e.target.value) || 10 }))}
                      className="ml-2 w-16 px-2 py-1 bg-gray-800/80 border border-gray-600/50 rounded text-white text-center focus:outline-none focus:ring-1 focus:ring-purple-500"
                      disabled={analysisState.isRunning}
                    />
                  </label>
                </div>
                <button
                  type="submit"
                  disabled={analysisState.isRunning || !formData.query.trim()}
                  className="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-purple-600 to-cyan-600 hover:from-purple-700 hover:to-cyan-700 disabled:from-gray-600 disabled:to-gray-700 text-white rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl disabled:shadow-none font-medium"
                >
                  <Search className="h-4 w-4" />
                  <span>{analysisState.isRunning ? 'Analyzing...' : 'Run Analysis'}</span>
                </button>
              </div>

              {/* Progress Bar */}
              {analysisState.isRunning && (
                <div className="mt-4">
                  <div className="flex items-center justify-between text-sm text-gray-300 mb-2">
                    <span className="truncate flex-1 mr-2">{analysisState.stage} - {analysisState.message}</span>
                    <span className="text-purple-400 font-medium">{analysisState.progress}%</span>
                  </div>
                  <div className="w-full bg-gray-700/50 rounded-full h-3 overflow-hidden">
                    <div 
                      className="bg-gradient-to-r from-purple-500 via-purple-400 to-cyan-500 h-3 rounded-full transition-all duration-700 ease-out shadow-lg"
                      style={{ width: `${analysisState.progress}%` }}
                    />
                  </div>
                </div>
              )}
            </form>
          </div>

          {/* KPIs */}
          {analysisState.result && (
            <div className="grid grid-cols-1 md:grid-cols-4 gap-3 md:gap-4 mb-4 md:mb-6">
              <div className="bg-gradient-to-r from-purple-900/30 to-purple-800/30 border border-purple-500/30 rounded-xl p-3 md:p-4 shadow-lg backdrop-blur-sm">
                <div className="text-lg md:text-xl lg:text-2xl font-bold text-purple-300">{analysisState.result.stats.total}</div>
                <div className="text-xs md:text-sm text-gray-300">Total Contradictions</div>
              </div>
              <div className="bg-gradient-to-r from-red-900/30 to-red-800/30 border border-red-500/30 rounded-xl p-3 md:p-4 shadow-lg backdrop-blur-sm">
                <div className="text-lg md:text-xl lg:text-2xl font-bold text-red-300">{analysisState.result.stats.bySeverity.critical || 0}</div>
                <div className="text-xs md:text-sm text-gray-300">Critical Issues</div>
              </div>
              <div className="bg-gradient-to-r from-orange-900/30 to-orange-800/30 border border-orange-500/30 rounded-xl p-3 md:p-4 shadow-lg backdrop-blur-sm">
                <div className="text-lg md:text-xl lg:text-2xl font-bold text-orange-300">{analysisState.result.stats.bySeverity.high || 0}</div>
                <div className="text-xs md:text-sm text-gray-300">High Priority</div>
              </div>
              <div className="bg-gradient-to-r from-green-900/30 to-green-800/30 border border-green-500/30 rounded-xl p-3 md:p-4 shadow-lg backdrop-blur-sm">
                <div className="text-lg md:text-xl lg:text-2xl font-bold text-green-300">{analysisState.suggestions.length}</div>
                <div className="text-xs md:text-sm text-gray-300">Harmonisation Suggestions</div>
              </div>
            </div>
          )}

          <div className="flex-1 grid grid-cols-1 lg:grid-cols-2 gap-6 min-h-0">
            {/* Results Table */}
            <div className="bg-gradient-to-br from-gray-900/50 to-gray-800/50 rounded-xl border border-purple-500/20 shadow-2xl backdrop-blur-sm overflow-hidden flex flex-col">
              <div className="p-4 border-b border-gray-700/50">
                <h2 className="text-lg md:text-xl font-semibold text-white flex items-center">
                  <AlertTriangle className="h-5 w-5 mr-2 text-orange-400" />
                  Contradictions Found
                </h2>
              </div>
              <div className="flex-1 overflow-y-auto">
                {analysisState.findings.length > 0 ? (
                  <div className="divide-y divide-gray-700">
                    {analysisState.findings.map((contradiction) => (
                      <div
                        key={contradiction.id}
                        className="p-4 hover:bg-gray-800/50 cursor-pointer transition-all duration-200 border-l-4 border-transparent hover:border-purple-500/30"
                        onClick={() => openContradictionDetails(contradiction)}
                      >
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex items-center space-x-2">
                            {getSeverityIcon(contradiction.severity)}
                            <span className={`text-xs px-2 py-1 rounded border ${getSeverityColor(contradiction.severity)}`}>
                              {contradiction.severity.toUpperCase()}
                            </span>
                            <span className="text-xs text-gray-400 bg-gray-800 px-2 py-1 rounded">
                              {contradiction.category}
                            </span>
                          </div>
                          <Eye className="h-4 w-4 text-gray-400" />
                        </div>
                        <h3 className="font-medium text-white mb-1">{contradiction.title}</h3>
                        <p className="text-sm text-gray-300 mb-2 line-clamp-2">{contradiction.description}</p>
                        <div className="text-xs text-gray-400">
                          Sources: {contradiction.sources.length} legal documents
                        </div>
                        <div className="text-xs text-gray-400 mt-1">
                          Impact: {contradiction.impact}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="flex items-center justify-center h-full text-gray-400 p-8">
                    {analysisState.isRunning ? (
                      <div className="text-center">
                        <Clock className="h-12 w-12 mx-auto mb-4 animate-spin text-purple-400" />
                        <p className="text-sm">Analyzing for contradictions...</p>
                      </div>
                    ) : (
                      <div className="text-center">
                        <FileText className="h-12 w-12 mx-auto mb-4 text-gray-500" />
                        <p className="text-sm text-gray-400">No contradictions found yet</p>
                        <p className="text-xs text-gray-500 mt-1">Run an analysis to discover legal contradictions</p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>

            {/* Analysis Logs */}
            <div className="bg-gradient-to-br from-gray-900/50 to-gray-800/50 rounded-xl border border-purple-500/20 shadow-2xl backdrop-blur-sm overflow-hidden flex flex-col">
              <div className="p-4 border-b border-gray-700/50">
                <h2 className="text-lg md:text-xl font-semibold text-white flex items-center">
                  <FileText className="h-5 w-5 mr-2 text-purple-400" />
                  Analysis Log
                </h2>
              </div>
              <div className="flex-1 overflow-y-auto p-4 space-y-2">
                {analysisState.logs.length > 0 ? (
                  <>
                    {analysisState.logs.map((log) => (
                      <div key={log.id} className="flex items-start space-x-2 text-sm">
                        <span className="text-gray-500 text-xs whitespace-nowrap">
                          {log.timestamp.toLocaleTimeString()}
                        </span>
                        <span className={`${
                          log.type === 'finding' ? 'text-orange-300' :
                          log.type === 'suggestion' ? 'text-green-300' :
                          'text-gray-300'
                        }`}>
                          {log.message}
                        </span>
                      </div>
                    ))}
                    <div ref={logsEndRef} />
                  </>
                ) : (
                  <div className="flex items-center justify-center h-full text-gray-400 p-8">
                    <div className="text-center">
                      <div className="h-12 w-12 mx-auto mb-4 rounded-full bg-gray-800/50 flex items-center justify-center">
                        <div className="h-6 w-6 border-2 border-gray-600 border-t-purple-400 rounded-full animate-spin"></div>
                      </div>
                      <p className="text-sm text-gray-400">Analysis log will appear here</p>
                      <p className="text-xs text-gray-500 mt-1">Start an analysis to see progress updates</p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Side Panel */}
        {showSidePanel && selectedContradiction && (
          <div className="fixed right-0 top-0 h-full w-96 bg-gradient-to-br from-gray-900 to-gray-800 border-l border-purple-500/20 shadow-2xl z-50 overflow-y-auto backdrop-blur-sm">
            <div className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg md:text-xl font-semibold text-white">Contradiction Details</h2>
                <button
                  onClick={() => setShowSidePanel(false)}
                  className="text-gray-400 hover:text-white"
                >
                  <XCircle className="h-5 w-5" />
                </button>
              </div>

              <div className="space-y-4">
                <div>
                  <div className="flex items-center space-x-2 mb-2">
                    {getSeverityIcon(selectedContradiction.severity)}
                    <span className={`text-xs px-2 py-1 rounded border ${getSeverityColor(selectedContradiction.severity)}`}>
                      {selectedContradiction.severity.toUpperCase()}
                    </span>
                    <span className="text-xs text-gray-400 bg-gray-800 px-2 py-1 rounded">
                      {selectedContradiction.category}
                    </span>
                  </div>
                  <h3 className="font-medium text-white mb-2">{selectedContradiction.title}</h3>
                  <p className="text-sm text-gray-300">{selectedContradiction.description}</p>
                </div>

                <div>
                  <h4 className="font-medium text-purple-300 mb-2">Legal Sources</h4>
                  <div className="space-y-2">
                    {selectedContradiction.sources.map((source, i) => (
                      <div key={i} className="bg-gray-800/50 border border-gray-700/50 rounded p-3">
                        <div className="text-sm text-white font-medium">{source}</div>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="font-medium text-orange-300 mb-2">Impact Assessment</h4>
                  <div className="bg-orange-900/20 border border-orange-500/30 rounded p-3">
                    <div className="text-sm text-gray-300">{selectedContradiction.impact}</div>
                  </div>
                </div>

                {/* Recommendation */}
                <div>
                  <h4 className="font-medium text-green-300 mb-2">Recommendation</h4>
                  <div className="bg-green-900/20 border border-green-500/30 rounded p-3">
                    <div className="text-sm text-gray-300">{selectedContradiction.recommendation}</div>
                    <button
                      onClick={() => copyToClipboard(selectedContradiction.recommendation)}
                      className="flex items-center space-x-1 text-xs text-green-400 hover:text-green-300 mt-3"
                    >
                      <Copy className="h-3 w-3" />
                      <span>Copy Recommendation</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
        </div>
      </Container>
    </Layout>
  );
};

export default AIAnalysisPage;
