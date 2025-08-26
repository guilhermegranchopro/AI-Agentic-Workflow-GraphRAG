import React, { useState, useRef, useEffect } from 'react';
import Layout from '@/components/Layout';
import Container from '@/components/ui/Container';
import { MessageSquare, Send, Bot, User, Loader2, Brain, Zap } from 'lucide-react';
import { API_ENDPOINTS } from '@/utils/constants';
import { generateId } from '@/utils/helpers';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';

interface Message {
  id: string;
  type: 'user' | 'assistant' | 'system' | 'progress';
  content: string;
  timestamp: Date;
  metadata?: {
    agent_used?: string;
    strategy_used?: string;
    confidence?: number;
    sources?: Array<{
      id: string;
      title: string;
      content: string;
      type: string;
      relevanceScore: number;
    }>;
  };
  progressData?: {
    step: string;
    message: string;
    agentResults?: Array<{
      agent: string;
      score: number;
      citations: number;
    }>;
    timestamp?: number;
    duration?: number;
  };
}

const LegalAssistantPage: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'system',
      content: 'Welcome to the Legal Assistant AI! I can help you with complex legal queries using advanced GraphRAG techniques and multi-agent reasoning. Ask me anything about UAE legal matters.',
      timestamp: new Date(),
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: generateId(),
      type: 'user',
      content: inputValue.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Prepare messages for the orchestrator
      const chatMessages = [
        ...messages.slice(-5).map(m => ({
          role: m.type === 'user' ? 'user' as const : 'assistant' as const,
          content: m.content
        })),
        { role: 'user' as const, content: userMessage.content }
      ];

      const response = await fetch('/api/assistant', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: chatMessages }),
      });

      if (!response.ok) throw new Error('Failed to get response');

      // Handle regular JSON response
      const responseData = await response.json();
      
      const assistantMessage: Message = {
        id: generateId(),
        type: 'assistant',
        content: responseData.text || 'I apologize, but I couldn\'t generate a response.',
        timestamp: new Date(),
        metadata: {
          agent_used: responseData.agents?.local || 'orchestrator',
          strategy_used: responseData.strategy_used || 'multi-agent',
          confidence: responseData.confidence || 0.8,
          sources: responseData.citations?.map((c: any) => ({
            id: c.title || 'unknown',
            title: c.title || 'Unknown Source',
            content: c.source || '',
            type: 'knowledge_graph',
            relevanceScore: c.relevance || 0.8
          })) || []
        }
      };

      // Add assistant message
      setMessages(prev => [...prev, assistantMessage]);

    } catch (error) {
      const errorMessage: Message = {
        id: generateId(),
        type: 'system',
        content: `Error: ${error instanceof Error ? error.message : 'An error occurred'}`,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const formatAgentName = (agentName?: string) => {
    if (!agentName) return 'AI Assistant';
    return agentName.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase());
  };

  const getStrategyIcon = (strategy?: string) => {
    switch (strategy?.toLowerCase()) {
      case 'local':
        return '🎯';
      case 'global':
        return '🌐';
      case 'drift':
        return '🎪';
      case 'hybrid':
        return '🔗';
      default:
        return '🤖';
    }
  };

  const getConfidenceColor = (confidence?: number) => {
    if (!confidence) return 'text-gray-400';
    if (confidence >= 0.8) return 'text-green-400';
    if (confidence >= 0.6) return 'text-yellow-400';
    return 'text-red-400';
  };

  return (
    <Layout title="AI Assistant - UAE Legal GraphRAG">
      <Container>
        <div className="flex flex-col">
          {/* Fixed Header */}
          <div className="flex-shrink-0 mb-3 md:mb-4 lg:mb-6">
            <div className="flex items-center space-x-2 md:space-x-3 mb-2 md:mb-3 lg:mb-4">
              <MessageSquare className="h-5 w-5 md:h-6 md:w-6 lg:h-8 lg:w-8 text-cyan-400" />
              <h1 className="text-xl md:text-2xl lg:text-3xl font-bold text-white">AI Assistant</h1>
            </div>
            <p className="text-sm md:text-base lg:text-lg text-gray-300 leading-relaxed">
              Multi-agent system for complex legal queries with autonomous reasoning
            </p>
            <div className="mt-3 md:mt-4 bg-gradient-to-r from-purple-900/30 to-cyan-900/30 border border-purple-500/30 rounded-xl p-3 md:p-4 backdrop-blur-sm shadow-lg">
              <div className="flex items-start space-x-2">
                <Brain className="h-4 w-4 md:h-5 md:w-5 text-cyan-400 mt-0.5" />
                <div>
                  <h3 className="font-medium text-cyan-100 mb-1 text-sm md:text-base">AI Agents Workflow</h3>
                  <p className="text-gray-300 text-xs md:text-sm leading-relaxed">
                    Powered by advanced multi-agent reasoning with Local RAG, Global RAG, and DRIFT strategies. 
                  Each query is intelligently routed to the most appropriate agent for optimal results.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Chat Container - Fixed Height with Internal Scrolling */}
        <div className="flex-1 flex flex-col bg-gradient-to-br from-gray-900/50 to-gray-800/50 rounded-xl border border-purple-500/20 shadow-2xl backdrop-blur-sm overflow-hidden">
          {/* Messages - Scrollable Area */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin scrollbar-thumb-purple-500/50 scrollbar-track-gray-800/20">
            {messages.map((message) => (
              <div key={message.id} className="animate-fade-in">
                {message.type === 'user' && (
                  <div className="flex justify-end">
                    <div className="max-w-3xl">
                      <div className="flex items-center justify-end space-x-2 mb-2">
                        <span className="text-sm text-gray-400">
                          {message.timestamp.toLocaleTimeString()}
                        </span>
                        <User className="h-4 w-4 text-cyan-400" />
                      </div>
                      <div className="bg-gradient-to-r from-cyan-600 to-blue-600 text-white rounded-xl px-4 py-3 shadow-lg">
                        <p className="whitespace-pre-wrap">{message.content}</p>
                      </div>
                    </div>
                  </div>
                )}

                {message.type === 'assistant' && (
                  <div className="flex justify-start">
                    <div className="max-w-4xl">
                      <div className="flex items-center space-x-2 mb-2">
                        <Bot className="h-4 w-4 text-purple-400" />
                        <span className="text-sm font-medium text-gray-300">
                          {formatAgentName(message.metadata?.agent_used)}
                        </span>
                        {message.metadata?.strategy_used && (
                          <span className="text-xs bg-purple-900/50 text-purple-300 px-2 py-1 rounded border border-purple-500/30">
                            {getStrategyIcon(message.metadata.strategy_used)} {message.metadata.strategy_used}
                          </span>
                        )}
                        {message.metadata?.confidence && (
                          <span className={`text-xs font-medium ${getConfidenceColor(message.metadata.confidence)}`}>
                            {Math.round(message.metadata.confidence * 100)}% confidence
                          </span>
                        )}
                        <span className="text-sm text-gray-400">
                          {message.timestamp.toLocaleTimeString()}
                        </span>
                      </div>
                      
                      <div className="bg-gradient-to-br from-gray-800/80 to-gray-700/80 text-gray-100 rounded-xl px-4 py-3 border border-purple-500/20 backdrop-blur-sm shadow-lg">
                        <div className="prose max-w-none prose-invert prose-purple">
                          <ReactMarkdown
                            remarkPlugins={[remarkGfm]}
                            rehypePlugins={[rehypeRaw]}
                            className="text-gray-100"
                            components={{
                              // Custom styling for markdown elements
                              h1: ({node, ...props}) => <h1 className="text-2xl font-bold text-purple-300 mb-4 border-b border-purple-500/30 pb-2" {...props} />,
                              h2: ({node, ...props}) => <h2 className="text-xl font-semibold text-purple-300 mb-3 mt-6" {...props} />,
                              h3: ({node, ...props}) => <h3 className="text-lg font-medium text-purple-300 mb-2 mt-4" {...props} />,
                              h4: ({node, ...props}) => <h4 className="text-base font-medium text-purple-300 mb-2 mt-3" {...props} />,
                              p: ({node, ...props}) => <p className="text-gray-100 mb-3 leading-relaxed" {...props} />,
                              ul: ({node, ...props}) => <ul className="list-disc list-inside text-gray-100 mb-3 space-y-1" {...props} />,
                              ol: ({node, ...props}) => <ol className="list-decimal list-inside text-gray-100 mb-3 space-y-1" {...props} />,
                              li: ({node, ...props}) => <li className="text-gray-100 ml-4" {...props} />,
                              blockquote: ({node, ...props}) => <blockquote className="border-l-4 border-purple-500/50 pl-4 italic text-gray-300 my-4" {...props} />,
                              code: ({node, ...props}: any) => {
                                const inline = 'inline' in props;
                                return inline ? 
                                  <code className="bg-gray-700/60 text-cyan-300 px-1.5 py-0.5 rounded text-sm font-mono" {...props} /> :
                                  <code className="block bg-gray-800/80 text-cyan-300 p-3 rounded text-sm font-mono overflow-x-auto border border-gray-600/50" {...props} />
                              },
                              pre: ({node, ...props}) => <pre className="bg-gray-800/80 p-3 rounded overflow-x-auto border border-gray-600/50 mb-3" {...props} />,
                              strong: ({node, ...props}) => <strong className="font-semibold text-white" {...props} />,
                              em: ({node, ...props}) => <em className="italic text-gray-200" {...props} />,
                              a: ({node, ...props}) => <a className="text-cyan-400 hover:text-cyan-300 underline decoration-cyan-400/50 hover:decoration-cyan-300" {...props} />,
                              hr: ({node, ...props}) => <hr className="border-gray-600/50 my-6" {...props} />,
                              table: ({node, ...props}) => <table className="min-w-full table-auto border-collapse border border-gray-600/50 my-4" {...props} />,
                              th: ({node, ...props}) => <th className="border border-gray-600/50 px-3 py-2 bg-gray-700/50 font-semibold text-purple-300" {...props} />,
                              td: ({node, ...props}) => <td className="border border-gray-600/50 px-3 py-2 text-gray-100" {...props} />,
                            }}
                          >
                            {message.content}
                          </ReactMarkdown>
                        </div>
                      </div>

                      {/* Sources */}
                      {message.metadata?.sources && message.metadata.sources.length > 0 && (
                        <div className="mt-3 bg-gradient-to-r from-blue-900/30 to-purple-900/30 border border-blue-500/30 rounded-xl p-3 backdrop-blur-sm shadow-lg">
                          <h4 className="text-sm font-medium text-blue-300 mb-2">
                            📚 Sources ({message.metadata.sources.length})
                          </h4>
                          <div className="space-y-2">
                            {message.metadata.sources.slice(0, 3).map((source, index) => (
                              <div key={source.id || index} className="text-sm">
                                <div className="flex items-center justify-between">
                                  <span className="font-medium text-blue-200">
                                    {source.title || `Source ${index + 1}`}
                                  </span>
                                  <span className="text-xs text-cyan-400">
                                    {(source.relevanceScore * 100).toFixed(1)}%
                                  </span>
                                </div>
                                <p className="text-gray-300 text-xs mt-1 line-clamp-2">
                                  {source.content.substring(0, 150)}...
                                </p>
                              </div>
                            ))}
                            {message.metadata.sources.length > 3 && (
                              <p className="text-xs text-blue-400">
                                +{message.metadata.sources.length - 3} more sources
                              </p>
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {message.type === 'system' && (
                  <div className="flex justify-center">
                    <div className="max-w-2xl bg-gradient-to-r from-yellow-900/30 to-orange-900/30 border border-yellow-500/30 rounded-xl px-4 py-3 text-center backdrop-blur-sm shadow-lg">
                      <p className="text-yellow-200 text-sm">{message.content}</p>
                    </div>
                  </div>
                )}

                {message.type === 'progress' && (
                  <div className="flex justify-center">
                    <div className="max-w-3xl bg-gradient-to-r from-blue-900/40 to-purple-900/40 border border-blue-500/40 rounded-xl px-4 py-3 backdrop-blur-sm shadow-lg">
                      <div className="flex items-center space-x-3">
                        <Loader2 className="h-4 w-4 text-blue-400 animate-spin" />
                        <div className="flex-1">
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-sm font-medium text-blue-300">
                              {message.progressData?.step?.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase()) || 'Processing'}
                            </span>
                            {message.progressData?.timestamp && (
                              <span className="text-xs text-gray-400">
                                {new Date(message.progressData.timestamp).toLocaleTimeString()}
                              </span>
                            )}
                          </div>
                          <p className="text-blue-200 text-sm">{message.content}</p>
                          
                          {message.progressData?.agentResults && message.progressData.agentResults.length > 0 && (
                            <div className="mt-2 flex flex-wrap gap-2">
                              {message.progressData.agentResults.map((result, index) => (
                                <div key={index} className="text-xs bg-purple-800/50 text-purple-200 px-2 py-1 rounded border border-purple-500/30">
                                  {getStrategyIcon(result.agent)} {result.agent}: {result.score?.toFixed(2)} ({result.citations} citations)
                                </div>
                              ))}
                            </div>
                          )}
                          
                          {message.progressData?.duration && (
                            <div className="mt-1 text-xs text-gray-400">
                              Duration: {message.progressData.duration}ms
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}

            {isLoading && (
              <div className="flex justify-start animate-fade-in">
                <div className="max-w-xs">
                  <div className="flex items-center space-x-2 mb-2">
                    <Bot className="h-4 w-4 text-purple-400" />
                    <span className="text-sm text-gray-300">AI is thinking...</span>
                  </div>
                  <div className="bg-gradient-to-br from-gray-800/80 to-gray-700/80 border border-purple-500/20 rounded-xl px-4 py-3 backdrop-blur-sm">
                    <div className="flex items-center space-x-2">
                      <Loader2 className="h-4 w-4 animate-spin text-purple-400" />
                      <span className="text-gray-300 text-sm">Processing your query...</span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Fixed Input Section */}
          <div className="flex-shrink-0 border-t border-purple-500/20 bg-gradient-to-r from-gray-900/50 to-gray-800/50 backdrop-blur-sm">
            {/* Quick Examples - Compact Version */}
            <div className="px-4 py-2 border-b border-purple-500/10">
              <div className="flex items-center space-x-2 overflow-x-auto scrollbar-thin scrollbar-thumb-purple-500/50 scrollbar-track-transparent">
                <span className="text-xs text-gray-400 whitespace-nowrap">💡 Examples:</span>
                {[
                  "Liability rules for companies",
                  "Contract disputes in UAE",
                  "Business establishment in Dubai",
                  "IP protection framework"
                ].map((example, index) => (
                  <button
                    key={index}
                    onClick={() => setInputValue(example + " - explain in detail")}
                    className="text-xs text-cyan-400 hover:text-cyan-300 bg-cyan-900/20 hover:bg-cyan-900/30 rounded px-2 py-1 transition-colors border border-cyan-500/30 whitespace-nowrap"
                    disabled={isLoading}
                  >
                    {example}
                  </button>
                ))}
              </div>
            </div>
            
            {/* Input Area */}
            <div className="p-4">
              <div className="flex space-x-4">
                <div className="flex-1">
                  <textarea
                    ref={inputRef}
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Ask a legal question (e.g., 'What are the liability rules for commercial companies and how are they interpreted by courts?')"
                    className="w-full h-20 resize-none bg-gray-800/80 border border-purple-500/30 rounded-xl px-4 py-3 text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500/50 backdrop-blur-sm transition-all duration-200"
                    disabled={isLoading}
                  />
                </div>
                <div className="flex flex-col justify-end">
                  <button
                    onClick={handleSendMessage}
                    disabled={isLoading || !inputValue.trim()}
                    className="bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 disabled:from-gray-600 disabled:to-gray-700 disabled:opacity-50 disabled:cursor-not-allowed text-white px-6 py-3 rounded-xl font-medium transition-all duration-200 shadow-lg hover:shadow-cyan-500/25 flex items-center space-x-2"
                  >
                    {isLoading ? (
                      <Loader2 className="h-5 w-5 animate-spin" />
                    ) : (
                      <Send className="h-5 w-5" />
                    )}
                    <span>Send</span>
                  </button>
                </div>
              </div>
              
              <div className="mt-2 text-xs text-gray-400">
                Press Enter to send, Shift+Enter for new line
              </div>
            </div>
          </div>
        </div>
        </div>
      </Container>
    </Layout>
  );
};

export default LegalAssistantPage;
