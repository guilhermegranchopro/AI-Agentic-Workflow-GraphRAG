import React, { useState, useEffect } from 'react';
import Layout from '@/components/Layout';
import { DatabaseStats, HealthCheck } from '@/types';
import { Database, Activity, Users, FileText, Network, Zap } from 'lucide-react';

const HomePage: React.FC = () => {
  const [healthStatus, setHealthStatus] = useState<HealthCheck | null>(null);
  const [dbStats, setDbStats] = useState<DatabaseStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHealthStatus();
    fetchDatabaseStats();
  }, []);

  const fetchHealthStatus = async () => {
    try {
      const response = await fetch('/api/health');
      const data = await response.json();
      setHealthStatus(data);
    } catch (error) {
      console.error('Failed to fetch health status:', error);
    }
  };

  const fetchDatabaseStats = async () => {
    try {
      const response = await fetch('/api/stats-new');
      const data = await response.json();
      setDbStats(data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch database stats:', error);
      setLoading(false);
    }
  };

  const OverviewCard = ({ 
    title, 
    description, 
    icon: Icon, 
    href 
  }: { 
    title: string; 
    description: string; 
    icon: any; 
    href: string; 
  }) => (
    <div className="group relative glass-card hover:shadow-2xl hover:shadow-purple-500/25 transition-all duration-500 cursor-pointer transform hover:-translate-y-4 hover:scale-105"
         onClick={() => window.location.href = href}>
      {/* Epic Background Effects */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-600/5 via-blue-600/5 to-cyan-600/5 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
      <div className="absolute -inset-1 bg-gradient-to-r from-purple-600 via-blue-600 to-cyan-600 rounded-2xl opacity-0 group-hover:opacity-20 blur transition-opacity duration-500"></div>
      
      <div className="relative z-10 flex items-start space-x-6">
        <div className="flex-shrink-0">
          <div className="relative w-16 h-16 rounded-2xl bg-gradient-to-br from-purple-600/20 to-blue-600/20 flex items-center justify-center group-hover:scale-110 transition-transform duration-500 border border-purple-500/30">
            <div className="absolute inset-0 bg-gradient-to-br from-purple-600/30 to-blue-600/30 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <Icon className="h-8 w-8 text-purple-400 group-hover:text-purple-300 relative z-10 transition-colors duration-300" />
          </div>
        </div>
        <div className="flex-1">
          <h3 className="text-xl font-bold text-white group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-purple-400 group-hover:to-blue-400 group-hover:bg-clip-text mb-3 transition-all duration-300">{title}</h3>
          <p className="text-gray-300 group-hover:text-gray-200 transition-colors duration-300 leading-relaxed text-base">{description}</p>
          <div className="mt-6 flex items-center text-sm text-purple-400 group-hover:text-purple-300 font-semibold">
            <span>Launch Experience</span>
            <svg className="ml-3 w-5 h-5 transform group-hover:translate-x-2 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
            <div className="ml-2 w-2 h-2 bg-purple-400 rounded-full animate-ping"></div>
          </div>
        </div>
      </div>
    </div>
  );

  const StatCard = ({ 
    title, 
    value, 
    icon: Icon, 
    color = 'primary' 
  }: { 
    title: string; 
    value: string | number; 
    icon: any; 
    color?: 'primary' | 'green' | 'blue' | 'purple'; 
  }) => {
    const colorClasses = {
      primary: 'from-purple-600/20 to-blue-600/20 border-purple-500/30 text-purple-400',
      green: 'from-green-600/20 to-emerald-600/20 border-green-500/30 text-green-400',
      blue: 'from-blue-600/20 to-cyan-600/20 border-blue-500/30 text-blue-400',
      purple: 'from-purple-600/20 to-violet-600/20 border-purple-500/30 text-violet-400'
    };

    return (
      <div className="group glass-card hover:shadow-xl hover:shadow-purple-500/10 transition-all duration-500 transform hover:-translate-y-2">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${colorClasses[color]} border flex items-center justify-center group-hover:scale-110 transition-transform duration-300`}>
              <Icon className={`h-7 w-7 ${colorClasses[color].split(' ').pop()}`} />
            </div>
          </div>
          <div className="ml-6 flex-1">
            <p className="text-sm font-semibold text-gray-400 group-hover:text-gray-300 transition-colors duration-300 mb-1">{title}</p>
            <p className="text-3xl font-black text-white group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-purple-400 group-hover:to-blue-400 group-hover:bg-clip-text transition-all duration-300">{value}</p>
          </div>
          <div className="w-3 h-3 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full animate-pulse opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
        </div>
      </div>
    );
  };

  return (
    <Layout title="UAE Legal GraphRAG - Home">
      <div className="animate-fade-in space-y-8">
        {/* Epic Hero Section */}
        <div className="text-center mb-16">
          <div className="relative">
            <div className="absolute -inset-4 bg-gradient-to-r from-purple-600 via-blue-600 to-cyan-600 rounded-3xl opacity-20 blur-xl"></div>
            <h1 className="relative text-6xl lg:text-7xl font-black text-transparent bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 bg-clip-text mb-6 animate-pulse">
              ⚖️ UAE Legal GraphRAG
            </h1>
          </div>
          <p className="text-2xl text-gray-300 max-w-4xl mx-auto leading-relaxed mb-8 font-light">
            🚀 <span className="text-transparent bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text font-semibold">Advanced legal research</span> with GraphRAG and AI agents 🤖
          </p>
          <div className="flex justify-center">
            <div className="px-6 py-3 rounded-full bg-gradient-to-r from-purple-600/30 to-blue-600/30 border border-purple-400/50 backdrop-blur-sm">
              <span className="text-purple-300 font-medium">✨ The Future of Legal Tech ✨</span>
            </div>
          </div>
        </div>

        {/* Health Status */}
        <div className="glass-card">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">System Health</h2>
            <div className={`status-indicator ${
              healthStatus?.status === 'healthy' ? 'status-healthy' : 'status-error'
            }`}>
              <Activity className="h-4 w-4 mr-1" />
              {healthStatus?.status || 'Checking...'}
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="flex items-center space-x-3 p-4 rounded-lg bg-gray-50 dark:bg-gray-800/50 transition-colors">
              <Database className={`h-6 w-6 ${
                healthStatus?.database ? 'text-green-500' : 'text-red-500'
              }`} />
              <span className="text-sm font-medium text-gray-800 dark:text-gray-300">Database Connection</span>
            </div>
            <div className="flex items-center space-x-3 p-4 rounded-lg bg-gray-50 dark:bg-gray-800/50 transition-colors">
              <Zap className={`h-6 w-6 ${
                healthStatus?.embeddings ? 'text-green-500' : 'text-red-500'
              }`} />
              <span className="text-sm font-medium text-gray-800 dark:text-gray-300">Embeddings Service</span>
            </div>
            <div className="flex items-center space-x-3 p-4 rounded-lg bg-gray-50 dark:bg-gray-800/50 transition-colors">
              <Activity className={`h-6 w-6 ${
                healthStatus?.ai_service ? 'text-green-500' : 'text-red-500'
              }`} />
              <span className="text-sm font-medium text-gray-800 dark:text-gray-300">AI Service</span>
            </div>
          </div>
        </div>

        {/* Database Statistics */}
        <div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">Database Statistics</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <StatCard
              title="Documents"
              value={dbStats?.total_documents?.toLocaleString() || '---'}
              icon={FileText}
              color="blue"
            />
            <StatCard
              title="Entities"
              value={dbStats?.total_entities?.toLocaleString() || '---'}
              icon={Users}
              color="green"
            />
            <StatCard
              title="Relationships"
              value={dbStats?.total_relationships?.toLocaleString() || '---'}
              icon={Network}
              color="purple"
            />
            <StatCard
              title="Communities"
              value={dbStats?.communities?.toLocaleString() || '---'}
              icon={Database}
              color="primary"
            />
          </div>
        </div>

        {/* GraphRAG Methods Overview */}
        <div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">GraphRAG Retrieval Methods</h2>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <OverviewCard
              title="🎯 Local RAG"
              description="Entity-centric traversal with temporal filtering for precise legal research"
              icon={Database}
              href="/assistant"
            />
            <OverviewCard
              title="🌐 Global RAG"
              description="Community-based analysis using Graph Data Science for comprehensive insights"
              icon={Network}
              href="/assistant"
            />
            <OverviewCard
              title="🎪 DRIFT RAG"
              description="Dynamic temporal analysis for tracking legal evolution over time"
              icon={Zap}
              href="/assistant"
            />
          </div>
        </div>

        {/* Additional Features */}
        <div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">Additional Features</h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <OverviewCard
              title="📊 Graph Visualization"
              description="Interactive exploration of legal knowledge graphs with advanced filtering"
              icon={Network}
              href="/graph"
            />
            <OverviewCard
              title="🤖 AI Assistant"
              description="Multi-agent system for complex legal queries with autonomous reasoning"
              icon={Activity}
              href="/assistant"
            />
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default HomePage;
