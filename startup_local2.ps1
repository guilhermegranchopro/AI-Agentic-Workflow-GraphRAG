# Load environment variables from .env file
$envFilePath = ".env"
if (Test-Path $envFilePath) {
    Get-Content $envFilePath | ForEach-Object {
        if ($_ -match "^(?!#)([^=]+)=(.+)$") {
            [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2], [System.EnvironmentVariableTarget]::Process)
        }
    }
} else {
    Write-Host "Error: .env file not found."
    exit 1
}

# Debugging: Print environment variables
Write-Host "AZURE_OPENAI_ENDPOINT=$env:AZURE_OPENAI_ENDPOINT "
Write-Host "AZURE_OPENAI_API_KEY=$env:AZURE_OPENAI_API_KEY"

# Check for required environment variables
if (-not $env:AZURE_OPENAI_ENDPOINT -or -not $env:AZURE_OPENAI_API_KEY) {
    Write-Error "Error: Required environment variables are not set."
    Write-Error "Ensure AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY are set."
    exit 1
}

# Start the Uvicorn server
Write-Host "Starting the Uvicorn server."
python -m uvicorn Main:app --host 0.0.0.0 --port 8000 --reload

Write-Host "Setup complete."