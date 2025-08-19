# UAE Legal GraphRAG - Setup Script for Windows
# This script sets up the development environment for the Next.js application

Write-Host "🚀 Setting up UAE Legal GraphRAG - Next.js Application" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan

# Check if Python is available
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = py --version 2>$null
    if ($pythonVersion) {
        Write-Host "✅ Found: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.11+ from https://python.org" -ForegroundColor Yellow
    exit 1
}

# Check if Node.js is available
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>$null
    if ($nodeVersion) {
        Write-Host "✅ Found Node.js: $nodeVersion" -ForegroundColor Green
    } else {
        throw "Node.js not found"
    }
} catch {
    Write-Host "❌ Node.js is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Node.js 18+ from https://nodejs.org" -ForegroundColor Yellow
    exit 1
}

# Create Python virtual environment
Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "⚠️  Virtual environment already exists" -ForegroundColor DarkYellow
} else {
    py -m venv .venv
    Write-Host "✅ Created Python virtual environment" -ForegroundColor Green
}

# Activate virtual environment and install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Write-Host "✅ Installed Python dependencies" -ForegroundColor Green

# Install Node.js dependencies
Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
npm install
Write-Host "✅ Installed Node.js dependencies" -ForegroundColor Green

# Check if .env.local exists
Write-Host "Checking environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env.local") {
    Write-Host "✅ Found .env.local configuration" -ForegroundColor Green
} else {
    Write-Host "⚠️  .env.local not found" -ForegroundColor DarkYellow
    if (Test-Path ".env") {
        Copy-Item ".env" ".env.local"
        Write-Host "📋 Copied .env to .env.local" -ForegroundColor Blue
        Write-Host "🔧 Please edit .env.local with your actual credentials" -ForegroundColor Yellow
    } else {
        Write-Host "❌ No environment template found" -ForegroundColor Red
        Write-Host "Please create .env.local with required environment variables" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "🎉 Setup complete!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Configure your .env.local file with:" -ForegroundColor White
Write-Host "   - Neo4j connection details" -ForegroundColor Gray
Write-Host "   - Azure OpenAI credentials" -ForegroundColor Gray
Write-Host "   - Application settings" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Start the development server:" -ForegroundColor White
Write-Host "   npm run dev" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Open http://localhost:3000 in your browser" -ForegroundColor White
Write-Host ""
Write-Host "For more information, see README.md" -ForegroundColor Blue
