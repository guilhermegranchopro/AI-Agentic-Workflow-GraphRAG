#!/bin/bash

# UAE Legal GraphRAG - Next.js Setup Script
# This script completes the setup for the Next.js application

echo "🚀 Setting up UAE Legal GraphRAG Next.js Application..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version 18+ is required. Current version: $(node -v)"
    exit 1
fi

echo "✅ Node.js $(node -v) detected"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Create additional required directories
echo "📁 Creating additional directories..."
mkdir -p public
mkdir -p public/images

# Create a simple favicon
echo "🎨 Setting up basic assets..."
cat > public/favicon.ico << 'EOF'
# This would contain favicon data in a real setup
# For now, just creating the file placeholder
EOF

# Create .gitignore if it doesn't exist
if [ ! -f .gitignore ]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << 'EOF'
# Dependencies
node_modules/
.npm
.yarn/

# Next.js
.next/
out/

# Environment files
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Python backend cache
python-backend/__pycache__/
python-backend/*.pyc
python-backend/.env

# Build outputs
build/
dist/
EOF
fi

# Verify Python backend exists
if [ ! -d "python-backend" ]; then
    echo "⚠️  Warning: python-backend directory not found. Make sure it's copied from the Streamlit version."
fi

# Verify environment file exists
if [ ! -f ".env.local" ]; then
    echo "⚠️  Warning: .env.local not found. Copy it from the Streamlit version or create it manually."
    echo "📝 Creating .env.local template..."
    cat > .env.local << 'EOF'
# Neo4j Configuration
NEO4J_URI=your_neo4j_uri
NEO4J_USERNAME=your_username
NEO4J_PASSWORD=your_password

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_CHAT_DEPLOYMENT=your_chat_deployment
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=your_embedding_deployment
EOF
    echo "⚠️  Please update .env.local with your actual credentials!"
fi

# Type checking
echo "🔍 Running type check..."
npm run type-check

if [ $? -ne 0 ]; then
    echo "⚠️  TypeScript errors detected. This is expected until dependencies are properly resolved."
fi

# Final status
echo ""
echo "🎉 Setup completed!"
echo ""
echo "Next steps:"
echo "1. Update .env.local with your actual credentials"
echo "2. Ensure python-backend directory contains the Python GraphRAG backend"
echo "3. Run 'npm run dev' to start the development server"
echo "4. Visit http://localhost:3000 to see your application"
echo ""
echo "📚 For more information, see README.md"
EOF
