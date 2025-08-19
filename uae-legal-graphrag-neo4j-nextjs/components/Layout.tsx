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
      
      <div className="min-h-screen bg-gray-50 flex flex-col">
        <Navigation />
        
        <main className="flex-1 py-8 px-4 sm:px-6 lg:px-8">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>

        {/* Footer */}
        <footer className="bg-white border-t border-gray-200 py-4">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center text-xs text-gray-500">
              <div>
                <p>UAE Legal GraphRAG v1.0</p>
                <p>Next.js + Neo4j + Azure AI</p>
              </div>
              <div className="hidden sm:block">
                <p>Advanced legal research with GraphRAG and AI agents</p>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </>
  );
};

export default Layout;
