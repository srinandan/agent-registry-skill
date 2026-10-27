#!/usr/bin/env python3

import argparse
import os
import sys


def _upsert_metadata_map_key(meta_lines, metadata_indent, map_name, key, value):
    """Ensures `map_name.<key>: "<value>"` exists inside a Deployment's metadata block."""
    child_indent = metadata_indent + 2
    map_idx = None
    map_indent = child_indent

    for idx, line in enumerate(meta_lines):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        if indent == child_indent and (
            stripped == f"{map_name}:" or stripped.startswith(f"{map_name}: ")
        ):
            map_idx = idx
            map_indent = indent
            break

    if map_idx is not None:
        # Find the end of the map_name block
        end_idx = len(meta_lines)
        entry_indent = map_indent + 2
        for j in range(map_idx + 1, len(meta_lines)):
            stripped = meta_lines[j].strip()
            if not stripped or stripped.startswith("#"):
                continue
            indent = len(meta_lines[j]) - len(meta_lines[j].lstrip())
            if indent <= map_indent:
                end_idx = j
                break
            entry_indent = indent

        # Check if key already exists in the block
        for j in range(map_idx + 1, end_idx):
            stripped = meta_lines[j].strip()
            if stripped.startswith(f"{key}:"):
                indent = len(meta_lines[j]) - len(meta_lines[j].lstrip())
                current_val = stripped.split(":", 1)[1].strip().strip("\"'")
                if current_val != value:
                    print(
                        f"Warning: Updating existing {key} from '{current_val}' to '{value}'"
                    )
                    meta_lines[j] = " " * indent + f'{key}: "{value}"'
                else:
                    print(f"Info: {key} '{value}' already exists. Skipping update.")
                return meta_lines

        # Key not found inside existing map_name block; insert right after map_name:
        new_line = " " * entry_indent + f'{key}: "{value}"'
        return meta_lines[: map_idx + 1] + [new_line] + meta_lines[map_idx + 1 :]

    # map_name block does not exist; insert before trailing blank lines of metadata
    insert_idx = len(meta_lines)
    for j in range(len(meta_lines) - 1, -1, -1):
        if meta_lines[j].strip():
            insert_idx = j + 1
            break

    new_block = [
        " " * child_indent + f"{map_name}:",
        " " * (child_indent + 2) + f'{key}: "{value}"',
    ]
    return meta_lines[:insert_idx] + new_block + meta_lines[insert_idx:]


def _process_single_doc(doc_lines, functional_type):
    """Processes a single YAML document's lines."""
    is_deployment = any(
        line.strip() in ("kind: Deployment", 'kind: "Deployment"', "kind: 'Deployment'")
        and (len(line) - len(line.lstrip()) == 0)
        for line in doc_lines
    )
    if not is_deployment:
        return doc_lines

    meta_start = None
    metadata_indent = 0
    for idx, line in enumerate(doc_lines):
        stripped = line.strip()
        indent = len(line) - len(line.lstrip())
        if indent == 0 and (stripped == "metadata:" or stripped.startswith("metadata: ")):
            meta_start = idx
            metadata_indent = indent
            break

    if meta_start is None:
        return doc_lines

    meta_end = len(doc_lines)
    for idx in range(meta_start + 1, len(doc_lines)):
        stripped = doc_lines[idx].strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(doc_lines[idx]) - len(doc_lines[idx].lstrip())
        if indent <= metadata_indent:
            meta_end = idx
            break

    meta_body = doc_lines[meta_start + 1 : meta_end]
    meta_body = _upsert_metadata_map_key(
        meta_body,
        metadata_indent,
        "labels",
        "registry.gke.io/functional-type",
        functional_type,
    )
    meta_body = _upsert_metadata_map_key(
        meta_body,
        metadata_indent,
        "annotations",
        "apphub.cloud.google.com/functional-type",
        functional_type,
    )
    return doc_lines[: meta_start + 1] + meta_body + doc_lines[meta_end:]


def process_yaml(content, functional_type):
    lines = content.split("\n")
    result_lines = []
    current_doc = []

    for line in lines:
        if line.startswith("---"):
            if current_doc:
                result_lines.extend(_process_single_doc(current_doc, functional_type))
                current_doc = []
            result_lines.append(line)
        else:
            current_doc.append(line)

    if current_doc:
        result_lines.extend(_process_single_doc(current_doc, functional_type))

    return "\n".join(result_lines)


def process_file(filepath, functional_type):
    try:
        with open(filepath, "r") as f:
            content = f.read()

        if (
            "kind: Deployment" in content
            or 'kind: "Deployment"' in content
            or "kind: 'Deployment'" in content
        ):
            updated_content = process_yaml(content, functional_type)

            if content != updated_content:
                with open(filepath, "w") as f:
                    f.write(updated_content)
                print(f"Successfully updated {filepath}")
            else:
                print(f"No changes needed for {filepath} (Labels/annotations already exist)")
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
            if file.endswith(".yaml") or file.endswith(".yml"):
                filepath = os.path.join(root, file)
                print(f"Processing {filepath}...")
                process_file(filepath, functional_type)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Configure GKE Deployment YAML files for Agent Registry automatic discovery "
            "(sets registry.gke.io/functional-type label and apphub.cloud.google.com/functional-type annotation)."
        )
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="File or directory to process (default: current directory)",
    )
    parser.add_argument(
        "--type",
        "-t",
        choices=["AGENT", "MCP_SERVER"],
        required=True,
        help="The functional type to set (AGENT or MCP_SERVER)",
    )

    args = parser.parse_args()

    path = os.path.abspath(args.path)
    print(f"Setting functional type: {args.type}")

    if os.path.isfile(path):
        if path.endswith(".yaml") or path.endswith(".yml"):
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
