import React, { ReactNode } from 'react';
import Head from 'next/head';
import Navigation from './Navigation';
import Sidebar from './Sidebar';

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
      
      <div className="min-h-screen bg-gray-50">
        <Navigation />
        
        <div className="flex">
          <Sidebar />
          
          <main className="flex-1 ml-64 p-8">
            <div className="max-w-7xl mx-auto">
              {children}
            </div>
          </main>
        </div>
      </div>
    </>
  );
};

export default Layout;
