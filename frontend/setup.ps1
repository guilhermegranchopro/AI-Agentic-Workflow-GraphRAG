# UAE Legal GraphRAG Setup Script
Write-Host "Setting up UAE Legal GraphRAG Development Environment" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python not found. Please install Python 3.8+ and try again." -ForegroundColor Red
    exit 1
}

# Check Node.js installation
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "Node.js not found. Please install Node.js 18+ and try again." -ForegroundColor Red
    exit 1
}

# Create Python virtual environment
Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "Virtual environment already exists" -ForegroundColor Green
} else {
    python -m venv .venv
    Write-Host "Virtual environment created" -ForegroundColor Green
}

# Install Node.js dependencies
Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
npm install
Write-Host "Node.js dependencies installed" -ForegroundColor Green

Write-Host ""
Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Activate virtual environment: .venv\Scripts\activate" -ForegroundColor White
Write-Host "2. Install Python dependencies: pip install -r requirements.txt" -ForegroundColor White
Write-Host "3. Copy .env.example to .env and configure environment variables" -ForegroundColor White
Write-Host "4. Start Neo4j database" -ForegroundColor White
Write-Host "5. Run 'npm run dev' to start the Next.js development server" -ForegroundColor White
Write-Host "6. Run 'npm run py:dev' to start the Python backend server" -ForegroundColor White
