import React, { useState, useRef, useEffect } from 'react';
import Layout from '@/components/Layout';
import { MessageSquare, Send, Bot, User, Loader2, Brain, Zap } from 'lucide-react';

interface Message {
  id: string;
  type: 'user' | 'assistant' | 'system';
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
      id: Date.now().toString(),
      type: 'user',
      content: inputValue.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/agents/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: userMessage.content,
          session_id: `session_${Date.now()}`,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to get response');
      }

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: data.response,
        timestamp: new Date(),
        metadata: {
          agent_used: data.agent_used,
          strategy_used: data.strategy_used,
          confidence: data.confidence,
          sources: data.sources,
        },
      };

      setMessages(prev => [...prev, assistantMessage]);

    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
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
    if (!confidence) return 'text-gray-500';
    if (confidence >= 0.8) return 'text-green-600';
    if (confidence >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <Layout title="Legal Assistant AI - UAE Legal GraphRAG">
      <div className="flex flex-col h-[calc(100vh-8rem)]">
        <div className="mb-6">
          <div className="flex items-center space-x-3 mb-4">
            <MessageSquare className="h-8 w-8 text-primary-600" />
            <h1 className="text-3xl font-bold text-gray-900">Legal Assistant AI</h1>
          </div>
          <p className="text-lg text-gray-600">
            Multi-agent system for complex legal queries with autonomous reasoning
          </p>
          <div className="mt-4 bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-start space-x-2">
              <Brain className="h-5 w-5 text-blue-600 mt-0.5" />
              <div>
                <h3 className="font-medium text-blue-900 mb-1">AI Agents Workflow</h3>
                <p className="text-blue-800 text-sm">
                  Powered by advanced multi-agent reasoning with Local RAG, Global RAG, and DRIFT strategies. 
                  Each query is intelligently routed to the most appropriate agent for optimal results.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Chat Container */}
        <div className="flex-1 flex flex-col bg-white rounded-lg border border-gray-200 shadow-sm">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6">
            {messages.map((message) => (
              <div key={message.id} className="animate-fade-in">
                {message.type === 'user' && (
                  <div className="flex justify-end">
                    <div className="max-w-3xl">
                      <div className="flex items-center justify-end space-x-2 mb-2">
                        <span className="text-sm text-gray-500">
                          {message.timestamp.toLocaleTimeString()}
                        </span>
                        <User className="h-4 w-4 text-gray-400" />
                      </div>
                      <div className="bg-primary-600 text-white rounded-lg px-4 py-3">
                        <p className="whitespace-pre-wrap">{message.content}</p>
                      </div>
                    </div>
                  </div>
                )}

                {message.type === 'assistant' && (
                  <div className="flex justify-start">
                    <div className="max-w-4xl">
                      <div className="flex items-center space-x-2 mb-2">
                        <Bot className="h-4 w-4 text-blue-600" />
                        <span className="text-sm font-medium text-gray-700">
                          {formatAgentName(message.metadata?.agent_used)}
                        </span>
                        {message.metadata?.strategy_used && (
                          <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                            {getStrategyIcon(message.metadata.strategy_used)} {message.metadata.strategy_used}
                          </span>
                        )}
                        {message.metadata?.confidence && (
                          <span className={`text-xs font-medium ${getConfidenceColor(message.metadata.confidence)}`}>
                            {Math.round(message.metadata.confidence * 100)}% confidence
                          </span>
                        )}
                        <span className="text-sm text-gray-500">
                          {message.timestamp.toLocaleTimeString()}
                        </span>
                      </div>
                      
                      <div className="bg-gray-100 text-gray-900 rounded-lg px-4 py-3">
                        <div className="prose max-w-none">
                          <p className="whitespace-pre-wrap leading-relaxed">{message.content}</p>
                        </div>
                      </div>

                      {/* Sources */}
                      {message.metadata?.sources && message.metadata.sources.length > 0 && (
                        <div className="mt-3 bg-blue-50 border border-blue-200 rounded-lg p-3">
                          <h4 className="text-sm font-medium text-blue-900 mb-2">
                            📚 Sources ({message.metadata.sources.length})
                          </h4>
                          <div className="space-y-2">
                            {message.metadata.sources.slice(0, 3).map((source, index) => (
                              <div key={source.id || index} className="text-sm">
                                <div className="flex items-center justify-between">
                                  <span className="font-medium text-blue-800">
                                    {source.title || `Source ${index + 1}`}
                                  </span>
                                  <span className="text-xs text-blue-600">
                                    {(source.relevanceScore * 100).toFixed(1)}%
                                  </span>
                                </div>
                                <p className="text-blue-700 text-xs mt-1 line-clamp-2">
                                  {source.content.substring(0, 150)}...
                                </p>
                              </div>
                            ))}
                            {message.metadata.sources.length > 3 && (
                              <p className="text-xs text-blue-600">
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
                    <div className="max-w-2xl bg-yellow-50 border border-yellow-200 rounded-lg px-4 py-3 text-center">
                      <p className="text-yellow-800 text-sm">{message.content}</p>
                    </div>
                  </div>
                )}
              </div>
            ))}

            {isLoading && (
              <div className="flex justify-start animate-fade-in">
                <div className="max-w-xs">
                  <div className="flex items-center space-x-2 mb-2">
                    <Bot className="h-4 w-4 text-blue-600" />
                    <span className="text-sm text-gray-600">AI is thinking...</span>
                  </div>
                  <div className="bg-gray-100 rounded-lg px-4 py-3">
                    <div className="flex items-center space-x-2">
                      <Loader2 className="h-4 w-4 animate-spin text-gray-600" />
                      <span className="text-gray-600 text-sm">Processing your query...</span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="border-t border-gray-200 p-4">
            <div className="flex space-x-4">
              <div className="flex-1">
                <textarea
                  ref={inputRef}
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask a legal question (e.g., 'What are the liability rules for commercial companies and how are they interpreted by courts?')"
                  className="textarea-field h-20 resize-none"
                  disabled={isLoading}
                />
              </div>
              <div className="flex flex-col justify-end">
                <button
                  onClick={handleSendMessage}
                  disabled={isLoading || !inputValue.trim()}
                  className="btn-primary px-6 py-3 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
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
            
            <div className="mt-2 text-xs text-gray-500">
              Press Enter to send, Shift+Enter for new line
            </div>
          </div>
        </div>

        {/* Quick Examples */}
        <div className="mt-6 bg-gray-50 rounded-lg p-4">
          <h3 className="text-sm font-medium text-gray-700 mb-3">💡 Try these examples:</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {[
              "What are the liability rules for commercial companies?",
              "How are contract disputes resolved in UAE law?",
              "What are the requirements for establishing a business in Dubai?",
              "Explain the intellectual property protection framework"
            ].map((example, index) => (
              <button
                key={index}
                onClick={() => setInputValue(example)}
                className="text-left text-sm text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded px-2 py-1 transition-colors"
                disabled={isLoading}
              >
                "{example}"
              </button>
            ))}
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default LegalAssistantPage;
