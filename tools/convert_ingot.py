#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from typing import Dict, Any

def convert_to_canonical(input_path: Path, output_path: Path):
    with open(input_path, 'r') as f:
        data = json.load(f)
    
    canonical = json.dumps(data, sort_keys=True, indent=2)
    
    with open(output_path, 'w') as f:
        f.write(canonical)
    
    print(f"Converted {input_path} to canonical format at {output_path}")

def extract_metadata(ingot_path: Path) -> Dict[str, Any]:
    with open(ingot_path, 'r') as f:
        data = json.load(f)
    
    metadata = {
        "has_signature": "signature" in data,
        "fields": list(data.get("ingot", data).keys()) if "ingot" in data else list(data.keys()),
        "size_bytes": ingot_path.stat().st_size
    }
    
    return metadata

def main():
    parser = argparse.ArgumentParser(description="Convert and manipulate ingot files")
    parser.add_argument("input", type=Path, help="Input ingot file")
    parser.add_argument("--output", type=Path, help="Output file (default: input_canonical.json)")
    parser.add_argument("--metadata", action="store_true", help="Extract metadata only")
    
    args = parser.parse_args()
    
    if args.metadata:
        metadata = extract_metadata(args.input)
        print(json.dumps(metadata, indent=2))
    else:
        output = args.output or args.input.with_name(args.input.stem + "_canonical.json")
        convert_to_canonical(args.input, output)

if __name__ == "__main__":
    main()
