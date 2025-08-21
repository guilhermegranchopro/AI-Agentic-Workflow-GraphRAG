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
      <main className="bg-professional min-h-screen">
        <div className="prof-container py-8">
          {children}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-slate-900 border-t border-slate-700 py-6">
        <div className="prof-container">
          <div className="flex flex-col sm:flex-row justify-between items-center text-sm text-slate-400">
            <div className="flex items-center space-x-2 mb-2 sm:mb-0">
              <span className="font-medium text-slate-200">UAE Legal GraphRAG v1.0</span>
              <span className="hidden sm:inline">•</span>
              <span className="hidden sm:inline">Next.js + Neo4j + Azure AI</span>
            </div>
            <div className="text-center sm:text-right">
              <span>Advanced legal research with GraphRAG and AI agents</span>
            </div>
          </div>
        </div>
      </footer>
    </>
  );
};

export default Layout;
