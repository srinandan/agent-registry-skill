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

BASE_URL="https://raw.githubusercontent.com/srinandan/agent-registry-skill/refs/heads/main"
DEST="$HOME/.gemini/skills/agent-registry-skill"

# List of files to download
FILES="SKILL.md references/adk-docs.md"

download_files() {
  printf "\nDownloading Agent Registry Skill items...\n"
  
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

printf "\nAgent Registry Skill Download Complete!\n"
printf "\n"
printf "Files installed into $DEST folder.\n"
printf "\n"
