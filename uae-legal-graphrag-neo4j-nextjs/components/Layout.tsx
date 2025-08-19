import React, { ReactNode } from 'react';
import Head from 'next/head';
import Navigation from './Navigation';

interface LayoutProps {
  children: ReactNode;
  title?: string;
  description?: string;
}

const Layout: React.FC<LayoutProps> = ({ 
  children, 
  title = 'UAE Legal GraphRAG',
  description = 'Advanced legal research with GraphRAG and AI agents'
}) => {
  return (
    <>
      <Head>
        <title>{title}</title>
        <meta name="description" content={description} />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <div className="min-h-screen gradient-bg flex flex-col transition-all duration-300">
        <Navigation />
        
        <main className="flex-1 py-8 px-4 sm:px-6 lg:px-8">
          <div className="max-w-7xl mx-auto animate-fade-in">
            {children}
          </div>
        </main>

        {/* Enhanced Footer */}
        <footer className="bg-white/80 backdrop-blur-md border-t border-gray-200/50 py-6 dark:bg-gray-900/80 dark:border-gray-700/50 transition-all duration-300">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex flex-col sm:flex-row justify-between items-center text-sm text-gray-500 dark:text-gray-400">
              <div className="flex items-center space-x-2 mb-2 sm:mb-0">
                <div className="w-2 h-2 bg-primary-500 rounded-full animate-pulse"></div>
                <span className="font-medium">UAE Legal GraphRAG v1.0</span>
                <span className="hidden sm:inline">•</span>
                <span className="hidden sm:inline">Next.js + Neo4j + Azure AI</span>
              </div>
              <div className="text-center sm:text-right">
                <p className="text-xs">Advanced legal research with GraphRAG and AI agents</p>
                <p className="text-xs mt-1">Built with ❤️ for legal professionals</p>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </>
  );
};

export default Layout;
