#!/bin/bash

# agent-dashboard.sh - Generates a markdown table of agents in the project

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

echo "Fetching agents for project: $PROJECT..." >&2

# Fetch global agents
GLOBAL_AGENTS=$(gcloud alpha agent-registry agents list --location=global --project="$PROJECT" --format=json --quiet 2>/dev/null)
if [ $? -ne 0 ] || [ -z "$GLOBAL_AGENTS" ]; then
  GLOBAL_AGENTS="[]"
fi

# Fetch regional agents
REGIONAL_AGENTS=$(gcloud alpha agent-registry agents list --location="$LOCATION" --project="$PROJECT" --format=json --quiet 2>/dev/null)
if [ $? -ne 0 ] || [ -z "$REGIONAL_AGENTS" ]; then
  REGIONAL_AGENTS="[]"
fi

# Combine and format
echo "$GLOBAL_AGENTS $REGIONAL_AGENTS" | jq -s 'add | map({
  name: (.name | split("/") | last),
  displayName: .displayName,
  location: (.name | split("/") | .[3]),
  runtime: (if .attributes["agentregistry.googleapis.com/system/RuntimeReference"].uri then 
              (.attributes["agentregistry.googleapis.com/system/RuntimeReference"].uri | sub("^//"; "") | split("/") | if length > 4 then .[-2:] | join("/") else .[-1] end) 
            else "-" end)
})' > /tmp/agents_combined.json

# Check if we have agents
COUNT=$(jq '. | length' /tmp/agents_combined.json)

if [ "$COUNT" -eq 0 ]; then
  echo "No agents found in global or $LOCATION."
  exit 0
fi

# Output Markdown Table
echo ""
echo "| Name | Display Name | Location | Runtime |"
echo "|------|--------------|----------|---------|"
jq -r '.[] | "| \(.name) | \(.displayName // "-") | \(.location) | \(.runtime // "-") |"' /tmp/agents_combined.json
