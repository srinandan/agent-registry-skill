#!/bin/bash

# quick-add-gcp-service.sh - Registers all 5 URL variants (Base, Base mTLS,
# Locational, Locational mTLS, and Regional REP) for a Governed Target GCP
# Service in Agent Registry.

set -euo pipefail

PROJECT=$(gcloud config get-value project 2>/dev/null || true)
LOCATION=$(gcloud config get-value compute/region 2>/dev/null || true)
SERVICE_ID=""

usage() {
  cat <<EOF
Usage: $0 --service=SERVICE_ID [--location=LOCATION] [--project=PROJECT_ID]

Registers all 5 Google Cloud API endpoint URL variants in Agent Registry for a
Governed Target Service (e.g., aiplatform, discoveryengine, pubsub, storage):
  1. Base:            https://<SERVICE_ID>.googleapis.com
  2. Base mTLS:       https://<SERVICE_ID>.mtls.googleapis.com
  3. Locational:      https://<LOCATION>-<SERVICE_ID>.googleapis.com
  4. Locational mTLS: https://<LOCATION>-<SERVICE_ID>.mtls.googleapis.com
  5. Regional REP:    https://<SERVICE_ID>.<LOCATION>.rep.googleapis.com

Options:
  --service=SERVICE_ID   GCP service short name (e.g., aiplatform, pubsub, storage)
  --location=LOCATION    Target GCP region (defaults to gcloud compute/region or us-central1)
  --project=PROJECT_ID   Target GCP project ID (defaults to gcloud config project)
  --help                 Show this help message
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --service=*)
      SERVICE_ID="${1#*=}"
      shift
      ;;
    --service)
      SERVICE_ID="${2:-}"
      shift 2
      ;;
    --location=*)
      LOCATION="${1#*=}"
      shift
      ;;
    --location)
      LOCATION="${2:-}"
      shift 2
      ;;
    --project=*)
      PROJECT="${1#*=}"
      shift
      ;;
    --project)
      PROJECT="${2:-}"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    -*)
      echo "Error: Unknown flag $1" >&2
      usage
      exit 1
      ;;
    *)
      if [ -z "$SERVICE_ID" ]; then
        SERVICE_ID="$1"
      fi
      shift
      ;;
  esac
done

# Strip .googleapis.com suffix if provided
SERVICE_ID="${SERVICE_ID%.googleapis.com}"

if [ -z "$SERVICE_ID" ]; then
  echo "Error: Service ID is required. Use --service=SERVICE_ID (e.g., --service=aiplatform)." >&2
  usage
  exit 1
fi

if [ -z "$PROJECT" ]; then
  echo "Error: Project not set. Use --project=PROJECT_ID." >&2
  exit 1
fi

if [ -z "$LOCATION" ]; then
  LOCATION="us-central1"
fi

echo "Registering 5 endpoint URL variants for service '${SERVICE_ID}' in project '${PROJECT}' (${LOCATION})..."

# 1. Base
gcloud agent-registry services create "${SERVICE_ID}" \
  --project="${PROJECT}" \
  --location="${LOCATION}" \
  --display-name="${SERVICE_ID}" \
  --endpoint-spec-type=no-spec \
  --interfaces='[{"protocolBinding": "jsonrpc", "url": "https://'"${SERVICE_ID}"'.googleapis.com"}]'

# 2. Base mTLS
gcloud agent-registry services create "${SERVICE_ID}-mtls" \
  --project="${PROJECT}" \
  --location="${LOCATION}" \
  --display-name="${SERVICE_ID} mTLS" \
  --endpoint-spec-type=no-spec \
  --interfaces='[{"protocolBinding": "jsonrpc", "url": "https://'"${SERVICE_ID}"'.mtls.googleapis.com"}]'

# 3. Locational
gcloud agent-registry services create "${LOCATION}-${SERVICE_ID}" \
  --project="${PROJECT}" \
  --location="${LOCATION}" \
  --display-name="${SERVICE_ID} Locational" \
  --endpoint-spec-type=no-spec \
  --interfaces='[{"protocolBinding": "jsonrpc", "url": "https://'"${LOCATION}-${SERVICE_ID}"'.googleapis.com"}]'

# 4. Locational mTLS
gcloud agent-registry services create "${LOCATION}-${SERVICE_ID}-mtls" \
  --project="${PROJECT}" \
  --location="${LOCATION}" \
  --display-name="${SERVICE_ID} Locational mTLS" \
  --endpoint-spec-type=no-spec \
  --interfaces='[{"protocolBinding": "jsonrpc", "url": "https://'"${LOCATION}-${SERVICE_ID}"'.mtls.googleapis.com"}]'

# 5. Regional REP
gcloud agent-registry services create "${SERVICE_ID}-${LOCATION}-rep" \
  --project="${PROJECT}" \
  --location="${LOCATION}" \
  --display-name="${SERVICE_ID} Regional (REP)" \
  --endpoint-spec-type=no-spec \
  --interfaces='[{"protocolBinding": "jsonrpc", "url": "https://'"${SERVICE_ID}.${LOCATION}"'.rep.googleapis.com"}]'

echo "Successfully registered all 5 endpoint variants for '${SERVICE_ID}' in '${LOCATION}'."
echo "Reminder: Ensure the Agent Identity has 'roles/iap.egressor' bound for Agent Gateway egress."
