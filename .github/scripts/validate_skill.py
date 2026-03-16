#!/usr/bin/env python3
import sys
import yaml
import os

def validate_skill(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return False

    try:
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Extract YAML frontmatter
        if not content.startswith('---\n'):
            print("Error: SKILL.md must start with ---")
            return False
            
        parts = content.split('---\n', 2)
        if len(parts) < 3:
            print("Error: Could not find YAML frontmatter closing ---")
            return False
            
        yaml_content = parts[1]
        data = yaml.safe_load(yaml_content)
        
        required_fields = ['name', 'description', 'metadata']
        metadata_required_fields = ['author', 'version']
        
        missing = []
        for field in required_fields:
            if field not in data or not data[field]:
                missing.append(field)
        
        if 'metadata' in data:
            for field in metadata_required_fields:
                if field not in data['metadata'] or not data['metadata'][field]:
                    missing.append(f"metadata.{field}")
        
        if missing:
            print(f"Error: Missing or empty required fields: {', '.join(missing)}")
            return False
            
        print("SKILL.md frontmatter validation successful!")
        return True

    except Exception as e:
        print(f"Error parsing YAML: {e}")
        return False

if __name__ == "__main__":
    skill_file = "SKILL.md"
    if len(sys.argv) > 1:
        skill_file = sys.argv[1]
        
    if validate_skill(skill_file):
        sys.exit(0)
    else:
        sys.exit(1)
