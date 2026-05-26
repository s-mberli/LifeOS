# MarkusOS Firefox Clipper

A minimal Manifest V3 Firefox extension that acts as a 1-click clipper to send the current tab's URL to the local MarkusOS ingestion pipeline.

## Setup Instructions

1. **Start the API Server**
   Ensure your local FastAPI ingestion endpoint is running. From the root of the `markusos` project, run:
   ```bash
   ./start_api.sh
   ```
   *This starts the server on `http://localhost:8000`.*

2. **Load the Extension in Firefox**
   - Open Firefox and navigate to `about:debugging`
   - Click **"This Firefox"** in the left sidebar.
   - Click the **"Load Temporary Add-on..."** button.
   - Navigate to the `apps/firefox-clipper/` directory and select the `manifest.json` file.
   - The extension icon should appear in your Firefox toolbar.

3. **Verify Functionality**
   - Click the extension icon while viewing any webpage.
   - The extension will silently send the URL to the local MarkusOS pipeline.
   - You can verify the API is receiving requests by checking the output in the terminal where you ran `./start_api.sh`, or by testing it manually with curl:
   
   ```bash
   curl -X POST http://localhost:8000/ingest \
        -H "Content-Type: application/json" \
        -d '{"url": "https://example.com"}'
   ```
