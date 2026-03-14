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

URL="https://raw.githubusercontent.com/srinandan/agent-registry-skill/refs/heads/main/SKILL.md"
DEST="$HOME/.gemini/skills/agent-registry-skill"

download_cli() {
  printf "\nDownloading Agent Registry Skill...\n"
  
  if ! curl -o /dev/null -sIf "$URL"; then
    printf "\nAgent Registry Skill is not found, please specify a valid Agent Registry Skill URL\n"
    exit 1
  fi

  # Create destination directory
  mkdir -p "$DEST"

  # Download the file
  curl -sL "$URL" -o "$DEST/SKILL.md"
}

download_cli

printf "\nAgent Registry Skill Download Complete!\n"
printf "\n"
printf "Copied Agent Registry Skill into $DEST folder.\n"
printf "\n"
