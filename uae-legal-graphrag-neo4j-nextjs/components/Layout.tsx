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
      
      {/* Navigation */}
      <Navigation />
      
      {/* Page Content */}
      <div className="gradient-bg flex-1 py-2 md:py-4 lg:py-6 transition-all duration-300">
        <div className="max-w-6xl mx-auto animate-fade-in">
          {children}
        </div>
      </div>

      {/* Footer - Will be positioned by page shell */}
      <footer className="bg-gray-900/90 backdrop-blur-md border-t border-purple-500/20 py-2 md:py-3 transition-all duration-300">
        <div className="max-w-6xl mx-auto px-3 sm:px-4 lg:px-6">
          <div className="flex flex-col sm:flex-row justify-between items-center text-xs text-gray-400">
            <div className="flex items-center space-x-2 mb-1 sm:mb-0">
              <div className="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-pulse"></div>
              <span className="font-medium">UAE Legal GraphRAG v1.0</span>
              <span className="hidden sm:inline">•</span>
              <span className="hidden sm:inline">Next.js + Neo4j + Azure AI</span>
            </div>
            <div className="text-center sm:text-right">
              <span className="text-xs">Advanced legal research with GraphRAG and AI agents</span>
            </div>
          </div>
        </div>
      </footer>
    </>
  );
};

export default Layout;
