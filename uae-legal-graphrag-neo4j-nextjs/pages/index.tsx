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
      const response = await fetch('/api/stats');
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
    <div className="glass-card hover:shadow-2xl hover:border-primary-200 dark:hover:border-primary-700 transition-all duration-300 cursor-pointer group transform hover:-translate-y-1"
         onClick={() => window.location.href = href}>
      <div className="flex items-start space-x-4">
        <div className="flex-shrink-0">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary-100 to-primary-200 dark:from-primary-900 dark:to-primary-800 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
            <Icon className="h-6 w-6 text-primary-600 dark:text-primary-300" />
          </div>
        </div>
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white group-hover:text-primary-700 dark:group-hover:text-primary-300 mb-2 transition-colors duration-200">{title}</h3>
          <p className="text-gray-700 dark:text-gray-300 group-hover:text-gray-800 dark:group-hover:text-gray-200 transition-colors duration-200 leading-relaxed">{description}</p>
          <div className="mt-4 flex items-center text-sm text-primary-600 dark:text-primary-400 group-hover:text-primary-700 dark:group-hover:text-primary-300 font-medium">
            <span>Click to access</span>
            <svg className="ml-2 w-4 h-4 transform group-hover:translate-x-1 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
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
      primary: 'text-primary-600 dark:text-primary-400 bg-primary-100 dark:bg-primary-900',
      green: 'text-green-600 dark:text-green-400 bg-green-100 dark:bg-green-900',
      blue: 'text-blue-600 dark:text-blue-400 bg-blue-100 dark:bg-blue-900',
      purple: 'text-purple-600 dark:text-purple-400 bg-purple-100 dark:bg-purple-900'
    };

    return (
      <div className="glass-card hover:shadow-lg transition-all duration-300 group">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className={`w-12 h-12 rounded-xl ${colorClasses[color]} flex items-center justify-center group-hover:scale-110 transition-transform duration-300`}>
              <Icon className={`h-6 w-6 ${colorClasses[color].split(' ')[0]} ${colorClasses[color].split(' ')[1]}`} />
            </div>
          </div>
          <div className="ml-4 flex-1">
            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">{title}</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">{value}</p>
          </div>
        </div>
      </div>
    );
  };

  return (
    <Layout title="UAE Legal GraphRAG - Home">
      <div className="animate-fade-in space-y-8">
        {/* Hero Section */}
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4 bg-gradient-to-r from-primary-600 to-primary-800 dark:from-primary-400 dark:to-primary-600 bg-clip-text text-transparent">
            ⚖️ UAE Legal GraphRAG
          </h1>
          <p className="text-xl text-gray-700 dark:text-gray-300 max-w-3xl mx-auto leading-relaxed">
            Advanced legal research with GraphRAG and AI agents
          </p>
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
              href="/local"
            />
            <OverviewCard
              title="🌐 Global RAG"
              description="Community-based analysis using Graph Data Science for comprehensive insights"
              icon={Network}
              href="/global"
            />
            <OverviewCard
              title="🎪 DRIFT RAG"
              description="Community-guided local search combining global context with local precision"
              icon={Zap}
              href="/drift"
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
              title="🤖 Legal Assistant AI"
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
