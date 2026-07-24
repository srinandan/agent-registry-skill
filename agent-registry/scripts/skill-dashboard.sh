#!/bin/bash

# skill-dashboard.sh - Generates a markdown table of skills in the project

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

echo "Fetching skills for project: $PROJECT..." >&2

# Fetch global skills
GLOBAL_SKILLS=$(gcloud alpha agent-registry skills list --location=global --project="$PROJECT" --format=json --quiet 2>/dev/null)
if [ $? -ne 0 ] || [ -z "$GLOBAL_SKILLS" ]; then
  GLOBAL_SKILLS="[]"
fi

# Skills only work in "global", "us", or "eu" regions.
# If LOCATION is not "us" or "eu" (and not "global"), do not pass it to gcloud.
REGIONAL_SKILLS="[]"
if [ -n "$LOCATION" ] && [ "$LOCATION" != "global" ]; then
  if [ "$LOCATION" = "us" ] || [ "$LOCATION" = "eu" ]; then
    REGIONAL_SKILLS=$(gcloud alpha agent-registry skills list --location="$LOCATION" --project="$PROJECT" --format=json --quiet 2>/dev/null)
    if [ $? -ne 0 ] || [ -z "$REGIONAL_SKILLS" ]; then
      REGIONAL_SKILLS="[]"
    fi
  else
    echo "Warning: Skills only work in 'global', 'us', or 'eu' regions. Ignoring unsupported region '$LOCATION'." >&2
  fi
fi

# Combine and format
echo "$GLOBAL_SKILLS $REGIONAL_SKILLS" | jq -s 'add | map({
  name: (.name | split("/") | last),
  displayName: .displayName,
  location: (.name | split("/") | .[3]),
  type: (.type // "-"),
  defaultRevision: (if .defaultRevision then (.defaultRevision | split("/") | last) else "-" end)
})' > /tmp/skills_combined.json

# Check if we have skills
COUNT=$(jq '. | length' /tmp/skills_combined.json)

if [ "$COUNT" -eq 0 ]; then
  echo "No skills found in global or $LOCATION."
  exit 0
fi

# Output Markdown Table
echo ""
echo "| Name | Display Name | Location | Type | Default Revision |"
echo "|------|--------------|----------|------|------------------|"
jq -r '.[] | "| \(.name) | \(.displayName // "-") | \(.location) | \(.type // "-") | \(.defaultRevision // "-") |"' /tmp/skills_combined.json
