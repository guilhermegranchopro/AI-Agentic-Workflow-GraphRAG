#!/bin/bash

# Export environment variables from .env file
export $(grep -v '^#' .env | xargs)



# Start the Uvicorn server
echo "Starting the Uvicorn server."
python -m uvicorn Main:app --host 0.0.0.0 --port 8000 --reload

echo "Setup complete."
