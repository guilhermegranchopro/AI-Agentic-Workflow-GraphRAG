import React, { useState, useRef, useEffect } from 'react';
import Layout from '@/components/Layout';
import Container from '@/components/ui/Container';
import { Send, Bot, User, Loader2, Brain, Zap, Settings, Code, Cpu } from 'lucide-react';
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
    backend?: string;
    agent_used?: string;
    strategy_used?: string;
    confidence?: number;
    advanced_processing?: boolean;
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
    stage?: string;
    agentResults?: Array<{
      agent: string;
      score: number;
      citations: number;
    }>;
    timestamp?: number;
    duration?: number;
  };
}

const HybridLegalAssistantPage: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'system',
      content: 'Welcome to the Hybrid Legal Assistant AI! Choose between our TypeScript-based system or the advanced Python backend with sentence transformers, multi-agent reasoning, and sophisticated legal analysis.',
      timestamp: new Date(),
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [usePythonBackend, setUsePythonBackend] = useState(false);
  const [pythonBackendStatus, setPythonBackendStatus] = useState<'checking' | 'available' | 'unavailable'>('checking');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Check Python backend status on mount
  useEffect(() => {
    checkPythonBackendStatus();
  }, []);

  const checkPythonBackendStatus = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/health');
      if (response.ok) {
        setPythonBackendStatus('available');
      } else {
        setPythonBackendStatus('unavailable');
      }
    } catch (error) {
      setPythonBackendStatus('unavailable');
    }
  };

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
      // Prepare messages for the hybrid API
      const chatMessages = [
        ...messages.slice(-5).map(m => ({
          role: m.type === 'user' ? 'user' as const : 'assistant' as const,
          content: m.content
        })),
        { role: 'user' as const, content: userMessage.content }
      ];

      // Use hybrid API endpoint
      const response = await fetch('/api/assistant/hybrid', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          messages: chatMessages, 
          use_python: usePythonBackend 
        }),
      });

      if (!response.ok) throw new Error('Failed to get response');

      // Handle SSE streaming
      const reader = response.body?.getReader();
      if (!reader) throw new Error('No response reader available');

      let assistantContent = '';
      const assistantMessage: Message = {
        id: generateId(),
        type: 'assistant',
        content: '',
        timestamp: new Date(),
        metadata: {
          backend: usePythonBackend ? 'python_fastapi' : 'typescript',
          agent_used: usePythonBackend ? 'multi_agent_system' : 'orchestrator',
          strategy_used: usePythonBackend ? 'hybrid_python' : 'typescript_only',
          confidence: 0.8,
          advanced_processing: usePythonBackend,
          sources: []
        }
      };

      // Add initial message
      setMessages(prev => [...prev, assistantMessage]);

      // Track progress message ID for updates
      let currentProgressMessageId: string | null = null;

      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ') && line.startsWith('event: ')) {
            const eventMatch = line.match(/event: (\w+)\ndata: (.+)/);
            if (eventMatch) {
              const [, eventType, data] = eventMatch;
              
              try {
                const parsed = JSON.parse(data);
                
                if (eventType === 'progress') {
                  const progressData = parsed.data || parsed;
                  
                  if (currentProgressMessageId) {
                    // Update existing progress message
                    setMessages(prev => prev.map(msg => 
                      msg.id === currentProgressMessageId 
                        ? { 
                            ...msg, 
                            content: progressData.message || progressData.step,
                            progressData 
                          }
                        : msg
                    ));
                  } else {
                    // Create new progress message
                    const progressMessage: Message = {
                      id: generateId(),
                      type: 'progress',
                      content: progressData.message || progressData.step,
                      timestamp: new Date(),
                      progressData
                    };
                    currentProgressMessageId = progressMessage.id;
                    setMessages(prev => [...prev, progressMessage]);
                  }
                } else if (eventType === 'token') {
                  // Handle token streaming
                  assistantContent += parsed.token;
                  setMessages(prev => prev.map(msg => 
                    msg.id === assistantMessage.id 
                      ? { ...msg, content: assistantContent }
                      : msg
                  ));
                } else if (eventType === 'complete') {
                  // Handle completion
                  const responseData = parsed;
                  
                  // Update assistant message with final content
                  setMessages(prev => prev.map(msg => {
                    if (msg.id === assistantMessage.id) {
                      return {
                        ...msg,
                        content: formatResponse(responseData),
                        metadata: {
                          ...msg.metadata,
                          sources: responseData.passages || [],
                          agent_results: responseData.agentResults || []
                        }
                      };
                    }
                    return msg;
                  }));
                  
                  // Remove progress message if exists
                  if (currentProgressMessageId) {
                    setMessages(prev => prev.filter(msg => msg.id !== currentProgressMessageId));
                  }
                }
              } catch (parseError) {
                console.error('Error parsing SSE data:', parseError);
              }
            }
          } else if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') continue;

            try {
              const parsed = JSON.parse(data);
              
              if (parsed.type === 'progress') {
                const progressData = parsed.data || parsed;
                
                if (currentProgressMessageId) {
                  setMessages(prev => prev.map(msg => 
                    msg.id === currentProgressMessageId 
                      ? { 
                          ...msg, 
                          content: progressData.message || progressData.step,
                          progressData 
                        }
                      : msg
                  ));
                } else {
                  const progressMessage: Message = {
                    id: generateId(),
                    type: 'progress',
                    content: progressData.message || progressData.step,
                    timestamp: new Date(),
                    progressData
                  };
                  currentProgressMessageId = progressMessage.id;
                  setMessages(prev => [...prev, progressMessage]);
                }
              } else if (parsed.token) {
                assistantContent += parsed.token;
                setMessages(prev => prev.map(msg => 
                  msg.id === assistantMessage.id 
                    ? { ...msg, content: assistantContent }
                    : msg
                ));
              } else {
                // Complete response
                const responseData = parsed;
                
                setMessages(prev => prev.map(msg => {
                  if (msg.id === assistantMessage.id) {
                    return {
                      ...msg,
                      content: formatResponse(responseData),
                      metadata: {
                        ...msg.metadata,
                        sources: responseData.passages || [],
                        agent_results: responseData.agentResults || []
                      }
                    };
                  }
                  return msg;
                }));
                
                if (currentProgressMessageId) {
                  setMessages(prev => prev.filter(msg => msg.id !== currentProgressMessageId));
                }
              }
            } catch (parseError) {
              console.error('Error parsing SSE data:', parseError);
            }
          }
        }
      }

    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, {
        id: generateId(),
        type: 'system',
        content: `Error: ${error instanceof Error ? error.message : 'Unknown error occurred'}`,
        timestamp: new Date(),
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const formatResponse = (data: any) => {
    if (!data) return 'No response data available.';
    
    let response = '';
    
    // Add passages if available
    if (data.passages && data.passages.length > 0) {
      response += '## Legal Analysis\n\n';
      data.passages.forEach((passage: any, index: number) => {
        response += `**Source ${index + 1}** (Score: ${passage.score?.toFixed(2) || 'N/A'})\n`;
        response += `${passage.text}\n\n`;
        
        if (passage.metadata?.backend === 'python_fastapi') {
          response += `*✨ Enhanced by Python backend with advanced ML processing*\n\n`;
        }
      });
    }
    
    // Add agent results if available
    if (data.agentResults && data.agentResults.length > 0) {
      response += '## Agent Analysis\n\n';
      data.agentResults.forEach((result: any) => {
        response += `**${result.agent}** (Confidence: ${result.confidence?.toFixed(2) || 'N/A'})\n`;
        if (result.findings) {
          if (typeof result.findings === 'string') {
            response += `${result.findings}\n\n`;
          } else {
            response += `${result.findings.analysis || JSON.stringify(result.findings)}\n\n`;
          }
        }
      });
    }
    
    // Add metadata info
    if (data.metadata) {
      response += '---\n';
      response += `*Backend: ${data.metadata.backend || 'unknown'} | `;
      response += `Processed: ${data.metadata.timestamp || new Date().toLocaleTimeString()}*\n`;
    }
    
    return response || 'Processing complete.';
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const BackendStatusIndicator = () => (
    <div className="flex items-center gap-2 mb-4 p-3 bg-gray-50 rounded-lg">
      <div className="flex items-center gap-2">
        <Code className="w-4 h-4" />
        <span className="text-sm font-medium">Backend:</span>
        <button
          onClick={() => setUsePythonBackend(!usePythonBackend)}
          disabled={pythonBackendStatus === 'unavailable'}
          className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
            usePythonBackend 
              ? 'bg-blue-100 text-blue-800 border border-blue-200' 
              : 'bg-gray-100 text-gray-800 border border-gray-200'
          } ${pythonBackendStatus === 'unavailable' ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:opacity-80'}`}
        >
          {usePythonBackend ? 'Python (Advanced)' : 'TypeScript (Standard)'}
        </button>
      </div>
      
      <div className="flex items-center gap-2 ml-auto">
        <Cpu className="w-4 h-4" />
        <span className="text-sm">Python Backend:</span>
        <div className={`w-2 h-2 rounded-full ${
          pythonBackendStatus === 'available' ? 'bg-green-500' : 
          pythonBackendStatus === 'checking' ? 'bg-yellow-500' : 'bg-red-500'
        }`} />
        <span className="text-xs text-gray-600">
          {pythonBackendStatus === 'available' ? 'Ready' : 
           pythonBackendStatus === 'checking' ? 'Checking...' : 'Offline'}
        </span>
        {pythonBackendStatus !== 'checking' && (
          <button 
            onClick={checkPythonBackendStatus}
            className="text-xs text-blue-600 hover:text-blue-800 ml-1"
          >
            Refresh
          </button>
        )}
      </div>
    </div>
  );

  return (
    <Layout>
      <Container className="flex flex-col h-screen max-h-screen">
        <div className="mb-6">
          <div className="flex items-center gap-3 mb-4">
            <Brain className="w-8 h-8 text-blue-600" />
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Hybrid Legal Assistant</h1>
              <p className="text-gray-600">Advanced AI with TypeScript + Python backend options</p>
            </div>
          </div>
          
          <BackendStatusIndicator />
        </div>

        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto mb-4 bg-white rounded-lg border border-gray-200 p-4">
          <div className="space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex gap-3 ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {message.type !== 'user' && (
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                    message.type === 'progress' ? 'bg-yellow-100' :
                    message.type === 'system' ? 'bg-gray-100' : 'bg-blue-100'
                  }`}>
                    {message.type === 'progress' ? (
                      <Loader2 className="w-4 h-4 text-yellow-600 animate-spin" />
                    ) : message.type === 'system' ? (
                      <Settings className="w-4 h-4 text-gray-600" />
                    ) : (
                      <Bot className="w-4 h-4 text-blue-600" />
                    )}
                  </div>
                )}
                
                <div className={`max-w-3xl ${message.type === 'user' ? 'order-first' : ''}`}>
                  <div className={`rounded-lg px-4 py-3 ${
                    message.type === 'user' 
                      ? 'bg-blue-600 text-white ml-auto' 
                      : message.type === 'progress'
                      ? 'bg-yellow-50 border border-yellow-200'
                      : message.type === 'system'
                      ? 'bg-gray-50 border border-gray-200'
                      : 'bg-gray-50 border border-gray-200'
                  }`}>
                    {message.type === 'user' ? (
                      <p className="whitespace-pre-wrap">{message.content}</p>
                    ) : (
                      <div className="prose prose-sm max-w-none">
                        <ReactMarkdown
                          remarkPlugins={[remarkGfm]}
                          rehypePlugins={[rehypeRaw]}
                        >
                          {message.content}
                        </ReactMarkdown>
                      </div>
                    )}
                    
                    {/* Metadata */}
                    {message.metadata && (
                      <div className="mt-2 pt-2 border-t border-gray-200">
                        <div className="flex items-center gap-2 text-xs text-gray-500">
                          {message.metadata.backend && (
                            <span className={`px-2 py-1 rounded-full ${
                              message.metadata.backend === 'python_fastapi' 
                                ? 'bg-green-100 text-green-700' 
                                : 'bg-blue-100 text-blue-700'
                            }`}>
                              {message.metadata.backend === 'python_fastapi' ? '🐍 Python' : '📝 TypeScript'}
                            </span>
                          )}
                          {message.metadata.advanced_processing && (
                            <span className="px-2 py-1 bg-purple-100 text-purple-700 rounded-full">
                              ✨ Advanced ML
                            </span>
                          )}
                          {message.metadata.confidence && (
                            <span>Confidence: {(message.metadata.confidence * 100).toFixed(0)}%</span>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                  
                  <div className="text-xs text-gray-500 mt-1">
                    {message.timestamp.toLocaleTimeString()}
                  </div>
                </div>

                {message.type === 'user' && (
                  <div className="w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center flex-shrink-0">
                    <User className="w-4 h-4 text-white" />
                  </div>
                )}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Area */}
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <div className="flex gap-3">
            <textarea
              ref={inputRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder={`Ask a legal question... (${usePythonBackend ? 'Python backend' : 'TypeScript backend'} active)`}
              className="flex-1 resize-none border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              rows={3}
              disabled={isLoading}
            />
            <button
              onClick={handleSendMessage}
              disabled={isLoading || !inputValue.trim()}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Processing
                </>
              ) : (
                <>
                  <Send className="w-4 h-4" />
                  Send
                </>
              )}
            </button>
          </div>
          
          {usePythonBackend && pythonBackendStatus === 'available' && (
            <div className="mt-2 text-xs text-green-600 flex items-center gap-1">
              <Zap className="w-3 h-3" />
              Advanced Python backend with sentence transformers and multi-agent system active
            </div>
          )}
        </div>
      </Container>
    </Layout>
  );
};

export default HybridLegalAssistantPage;
