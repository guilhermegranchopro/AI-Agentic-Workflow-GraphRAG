# Load environment variables from .env file
$envFilePath = "C:\Users\jn132nu\OneDrive - EY\Desktop\Worten\Gen AI\LLM-Call-Center\LLM-Call-Center\environment"
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
Write-Host "AZURE_OPENAI_DEPLOYMENT=$env:AZURE_OPENAI_DEPLOYMENT"
Write-Host "AZURE_OPENAI_API_KEY=$env:AZURE_OPENAI_API_KEY"

# Check for required environment variables
if (-not $env:AZURE_OPENAI_DEPLOYMENT -or -not $env:AZURE_OPENAI_API_KEY) {
    Write-Error "Error: Required environment variables are not set."
    Write-Error "Ensure AZURE_OPENAI_DEPLOYMENT, AZURE_OPENAI_API_KEY, AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_API_VERSION and AZURE_SEARCH_API_KEY are set."
    exit 1
}

# Start the Uvicorn server
Write-Host "Starting the Uvicorn server."
python -m uvicorn Main:app --host 0.0.0.0 --port 8000 --reload

Write-Host "Setup complete."
