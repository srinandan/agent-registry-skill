#!/bin/bash

# mcp-dashboard.sh - Generates a markdown table of MCP servers in the project

PROJECT=$(gcloud config get-value project 2>/dev/null)
LOCATION=$(gcloud config get-value compute/region 2>/dev/null)

while [[ $# -gt 0 ]]; do
  case $1 in
    --project=*)
      PROJECT="${1#*=}"
      shift
      ;;
    --location=*)
      LOCATION="${1#*=}"
      shift
      ;;
    *)
      shift
      ;;
  esac
done

if [ -z "$PROJECT" ]; then
  echo "Error: Project not set. Use --project=PROJECT_ID"
  exit 1
fi

# Default location to us-central1 if not set
if [ -z "$LOCATION" ]; then
  LOCATION="us-central1"
fi

echo "Fetching MCP servers for project: $PROJECT..." >&2

# Fetch global MCP servers
GLOBAL_MCP=$(gcloud alpha agent-registry mcp-servers list --location=global --project="$PROJECT" --format=json --quiet 2>/dev/null)
if [ $? -ne 0 ] || [ -z "$GLOBAL_MCP" ]; then
  GLOBAL_MCP="[]"
fi

# Fetch regional MCP servers
REGIONAL_MCP=$(gcloud alpha agent-registry mcp-servers list --location="$LOCATION" --project="$PROJECT" --format=json --quiet 2>/dev/null)
if [ $? -ne 0 ] || [ -z "$REGIONAL_MCP" ]; then
  REGIONAL_MCP="[]"
fi

# Combine and format
echo "$GLOBAL_MCP $REGIONAL_MCP" | jq -s 'add | map({
  name: (.name | split("/") | last),
  displayName: .displayName,
  location: (.name | split("/") | .[3]),
  tools: (.tools | map(.name) | if length > 3 then (.[0:3] | join(", ")) + ", ..." else join(", ") end),
  runtime: (if .attributes["agentregistry.googleapis.com/system/RuntimeReference"].uri then 
              (.attributes["agentregistry.googleapis.com/system/RuntimeReference"].uri | sub("^//"; "") | split("/") | if length > 4 then .[-2:] | join("/") else .[-1] end) 
            else "-" end)
})' > /tmp/mcp_combined.json

# Check if we have servers
COUNT=$(jq '. | length' /tmp/mcp_combined.json)

if [ "$COUNT" -eq 0 ]; then
  echo "No MCP servers found in global or $LOCATION."
  exit 0
fi

# Output Markdown Table
echo ""
echo "| Name | Display Name | Location | Tools | Runtime |"
echo "|------|--------------|----------|-------|---------|"
jq -r '.[] | "| \(.name) | \(.displayName // "-") | \(.location) | \(.tools // "-") | \(.runtime // "-") |"' /tmp/mcp_combined.json
