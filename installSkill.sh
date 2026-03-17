#!/bin/sh
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -e

REPO="srinandan/agent-registry-skill"
SKILL_FILE="agent-registry.skill"
DEST="$HOME/.gemini/skills"

# Check dependencies
if ! command -v curl >/dev/null 2>&1; then
  printf "Error: curl is required but not installed.\n"
  exit 1
fi

if ! command -v unzip >/dev/null 2>&1; then
  printf "Error: unzip is required but not installed.\n"
  exit 1
fi

# Determine the version to install
if [ "${SKILL_VERSION}" = "" ] ; then
  # Try to get the latest release tag from GitHub API
  printf "Detecting latest version...\n"
  # We use -s to be silent, -S to show errors. sed extracts the tag_name from the JSON response.
  LATEST_TAG=$(curl -sS https://api.github.com/repos/srinandan/agent-registry-skill/releases/latest | grep "tag_name" | sed -E 's/.*"([^"]+)".*/\1/')
  
  if [ "${LATEST_TAG}" != "" ]; then
    SKILL_VERSION="${LATEST_TAG}"
    printf "Latest version detected: %s\n" "${SKILL_VERSION}"
  else
    SKILL_VERSION="main"
    printf "Unable to detect latest version, defaulting to branch: %s\n" "${SKILL_VERSION}"
  fi
else
  printf "Using specified version: %s\n" "${SKILL_VERSION}"
fi

BASE_URL="https://raw.githubusercontent.com/srinandan/agent-registry-skill/${SKILL_VERSION}"
DEST="$HOME/.gemini/skills/agent-registry-skill"

# List of files to download
FILES="SKILL.md references/adk-docs.md references/gcloud-command.md scripts/agent-dashboard.sh scripts/mcp-dashboard.sh"

download_files() {
  printf "\nDownloading Agent Registry Skill (%s) items...\n" "${SKILL_VERSION}"
  
  for FILE in $FILES; do
    URL="$BASE_URL/$FILE"
    TARGET="$DEST/$FILE"
    
    # Create directory for the file
    mkdir -p "$(dirname "$TARGET")"
    
    printf "  Downloading $FILE...\n"
    if ! curl -sL "$URL" -o "$TARGET"; then
      printf "\nFailed to download $FILE from $URL\n"
      exit 1
    fi
  done
}

download_files

printf "\nAgent Registry Skill (%s) Download Complete!\n" "${SKILL_VERSION}"
printf "\n"
printf "Files installed into $DEST folder.\n"
printf "\n"