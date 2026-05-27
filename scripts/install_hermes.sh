#!/bin/bash
echo "Installing hermes-agent by NousResearch..."
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

echo "Installation complete. Please run 'hermes setup' to configure your LLM provider (e.g., OpenRouter)."
echo "Then, to add the MarkusOS MCP server, edit ~/.hermes/config.yaml and add the following under mcp_servers:"
echo ""
echo "mcp_servers:"
echo "  markusos:"
echo "    command: \"python\""
echo "    args:"
echo "      - \"$(pwd)/src/core/mcp_server.py\""
echo ""
