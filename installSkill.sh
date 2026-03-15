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

# Resolve download URL — use pinned version if provided, otherwise latest
if [ -n "$SKILL_VERSION" ]; then
  DOWNLOAD_URL="https://github.com/$REPO/releases/download/$SKILL_VERSION/$SKILL_FILE"
  printf "\nInstalling Agent Registry Skill %s...\n" "$SKILL_VERSION"
else
  DOWNLOAD_URL="https://github.com/$REPO/releases/latest/download/$SKILL_FILE"
  printf "\nInstalling Agent Registry Skill (latest release)...\n"
fi

# Download the .skill file
TMP_FILE=$(mktemp /tmp/agent-registry-skill.XXXXXX.zip)
printf "  Downloading %s...\n" "$SKILL_FILE"
if ! curl -sL "$DOWNLOAD_URL" -o "$TMP_FILE"; then
  printf "\nFailed to download %s from %s\n" "$SKILL_FILE" "$DOWNLOAD_URL"
  rm -f "$TMP_FILE"
  exit 1
fi

# Extract into skills directory
mkdir -p "$DEST"
printf "  Extracting into %s...\n" "$DEST"
unzip -qo "$TMP_FILE" -d "$DEST/agent-registry-skill"
rm -f "$TMP_FILE"

printf "\nAgent Registry Skill installed successfully!\n"
printf "Files installed into %s/agent-registry-skill/\n" "$DEST"
printf "\n"