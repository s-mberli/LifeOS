#!/bin/bash
# Start the MarkusOS Ingestion API
echo "Starting MarkusOS Ingestion API on http://localhost:8000..."
echo "To test the endpoint manually, run:"
echo 'curl -X POST http://localhost:8000/ingest -H "Content-Type: application/json" -d '\''{"url": "https://example.com"}'\'''
echo ""

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run the FastAPI app via uvicorn
uvicorn src.api:app --host 127.0.0.1 --port 8000 --reload
