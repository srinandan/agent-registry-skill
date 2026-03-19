#!/usr/bin/env python3

import os
import sys
import argparse

def process_yaml(content, functional_type):
    lines = content.split('\n')

    # Simple state machine to track if we're inside a Deployment's top-level metadata
    in_deployment = False
    in_metadata = False
    metadata_indent = 0
    in_annotations = False
    annotations_indent = 0

    modified_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Check if it's a new document
        if line.startswith('---'):
            # Edge case: file ends while still in metadata without annotations having been added
            if in_metadata and not in_annotations:
                # Add annotations before the next document
                new_annotations = [
                    ' ' * (metadata_indent + 2) + 'annotations:',
                    ' ' * (metadata_indent + 4) + f'apphub.cloud.google.com/functional-type: "{functional_type}"'
                ]

                # We need to insert these before any trailing blank lines that might precede the '---'
                insert_idx = len(modified_lines)
                for j in range(len(modified_lines) - 1, -1, -1):
                     if modified_lines[j].strip():
                         insert_idx = j + 1
                         break

                modified_lines = modified_lines[:insert_idx] + new_annotations + modified_lines[insert_idx:]

            in_deployment = False
            in_metadata = False
            in_annotations = False
            modified_lines.append(line)
            i += 1
            continue

        # Determine if we're in a Deployment
        if line.startswith('kind: Deployment') or line.startswith('kind: "Deployment"') or line.startswith("kind: 'Deployment'"):
            in_deployment = True

        # Determine if we're in top-level metadata
        if in_deployment and line.startswith('metadata:'):
            in_metadata = True
            metadata_indent = len(line) - len(line.lstrip())
            modified_lines.append(line)
            i += 1
            continue

        # If we exit metadata or deployment context
        if in_metadata and stripped and not line.startswith(' ') and not line.startswith('metadata:'):
            # We reached another top-level key like 'spec:' or 'apiVersion:'

            # If we were in metadata but didn't find annotations, we need to add them before leaving metadata
            if not in_annotations:
                # Backtrack to the last non-empty line of metadata
                insert_idx = len(modified_lines)
                for j in range(len(modified_lines) - 1, -1, -1):
                    if modified_lines[j].strip() and modified_lines[j].startswith(' ' * (metadata_indent + 2)):
                        insert_idx = j + 1
                        break
                    elif modified_lines[j].startswith('metadata:'):
                        insert_idx = j + 1
                        break

                new_annotations = [
                    ' ' * (metadata_indent + 2) + 'annotations:',
                    ' ' * (metadata_indent + 4) + f'apphub.cloud.google.com/functional-type: "{functional_type}"'
                ]
                modified_lines = modified_lines[:insert_idx] + new_annotations + modified_lines[insert_idx:]

            in_metadata = False
            in_annotations = False

        if in_metadata and line.startswith(' ' * (metadata_indent + 2) + 'annotations:'):
            in_annotations = True
            annotations_indent = len(line) - len(line.lstrip())

            # Check if our specific annotation already exists
            found_annotation = False
            j = i + 1
            while j < len(lines):
                next_line = lines[j]
                next_stripped = next_line.strip()
                next_indent = len(next_line) - len(next_line.lstrip())

                if next_stripped and next_indent <= annotations_indent:
                    break # Reached end of annotations block

                if next_stripped.startswith('apphub.cloud.google.com/functional-type:'):
                    found_annotation = True
                    current_val = next_stripped.split(':', 1)[1].strip().strip('"\'')
                    if current_val != functional_type:
                        print(f"Warning: Updating existing annotation from '{current_val}' to '{functional_type}'")
                        lines[j] = ' ' * next_indent + f'apphub.cloud.google.com/functional-type: "{functional_type}"'
                    else:
                        print(f"Info: Annotation '{functional_type}' already exists. Skipping update.")
                    break
                j += 1

            if not found_annotation:
                # Add the annotation right after 'annotations:'
                modified_lines.append(line)
                modified_lines.append(' ' * (annotations_indent + 2) + f'apphub.cloud.google.com/functional-type: "{functional_type}"')
                i += 1
                continue

        modified_lines.append(line)
        i += 1

    # Edge case: file ends while still in metadata without annotations having been added
    if in_metadata and not in_annotations:
        new_annotations = [
            ' ' * (metadata_indent + 2) + 'annotations:',
            ' ' * (metadata_indent + 4) + f'apphub.cloud.google.com/functional-type: "{functional_type}"'
        ]

        insert_idx = len(modified_lines)
        for j in range(len(modified_lines) - 1, -1, -1):
             if modified_lines[j].strip():
                 insert_idx = j + 1
                 break

        modified_lines = modified_lines[:insert_idx] + new_annotations + modified_lines[insert_idx:]

    return '\n'.join(modified_lines)


def process_file(filepath, functional_type):
    try:
        with open(filepath, 'r') as f:
            content = f.read()

        # Basic check if it contains a Deployment
        if 'kind: Deployment' in content or 'kind: "Deployment"' in content or "kind: 'Deployment'" in content:
            updated_content = process_yaml(content, functional_type)

            if content != updated_content:
                with open(filepath, 'w') as f:
                    f.write(updated_content)
                print(f"Successfully updated {filepath}")
            else:
                print(f"No changes needed for {filepath} (Annotation already exists)")
        else:
            print(f"Skipping {filepath} (no Deployment found)")
    except Exception as e:
        print(f"Error processing {filepath}: {e}", file=sys.stderr)

def process_directory(directory, functional_type):
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist.", file=sys.stderr)
        sys.exit(1)

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                filepath = os.path.join(root, file)
                print(f"Processing {filepath}...")
                process_file(filepath, functional_type)

def main():
    parser = argparse.ArgumentParser(description="Annotate GKE Deployment YAML files with apphub functional-type.")
    parser.add_argument("path", nargs="?", default=".", help="File or directory to process (default: current directory)")
    parser.add_argument("--type", "-t", choices=["AGENT", "MCP_SERVER"], required=True, help="The functional type to set (AGENT or MCP_SERVER)")

    args = parser.parse_args()

    path = os.path.abspath(args.path)
    print(f"Setting functional type: {args.type}")

    if os.path.isfile(path):
        if path.endswith('.yaml') or path.endswith('.yml'):
            print(f"Processing file: {path}")
            process_file(path, args.type)
        else:
             print(f"Error: File '{path}' is not a YAML file.", file=sys.stderr)
             sys.exit(1)
    else:
        print(f"Scanning directory: {path}")
        process_directory(path, args.type)

if __name__ == "__main__":
    main()
