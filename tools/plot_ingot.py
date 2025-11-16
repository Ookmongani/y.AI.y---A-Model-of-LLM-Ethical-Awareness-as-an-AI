#!/usr/bin/env python3
import argparse
import json
import matplotlib.pyplot as plt
from pathlib import Path
from typing import List, Dict, Any

def load_events(filepath: Path) -> List[Dict[str, Any]]:
    with open(filepath, 'r') as f:
        return json.load(f)

def plot_ingot_data(ingot_path: Path, output_path: Path):
    with open(ingot_path, 'r') as f:
        data = json.load(f)
    
    if "events" in data:
        events = data["events"]
        timestamps = [e["timestamp"] for e in events]
        magnitudes = [e.get("magnitude", 0) for e in events]
        suppressed = [e.get("suppressed_magnitude", 0) for e in events]
        
        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.plot(timestamps, magnitudes, 'b-', label='Original')
        plt.ylabel('Magnitude')
        plt.legend()
        plt.grid(True)
        
        plt.subplot(2, 1, 2)
        plt.plot(timestamps, suppressed, 'r-', label='Log10 Suppressed')
        plt.xlabel('Timestamp')
        plt.ylabel('Suppressed Magnitude')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig(output_path)
        print(f"Plot saved to {output_path}")
    else:
        print("No events data found in ingot")

def plot_summary(ingot_path: Path, output_path: Path):
    with open(ingot_path, 'r') as f:
        data = json.load(f)
    
    fields = list(data.keys())
    values = [len(str(v)) for v in data.values()]
    
    plt.figure(figsize=(8, 6))
    plt.bar(fields, values)
    plt.xlabel('Fields')
    plt.ylabel('Value Length (chars)')
    plt.title('Ingot Field Summary')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Summary plot saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Plot ingot data")
    parser.add_argument("ingot", type=Path, help="Path to ingot file")
    parser.add_argument("--output", type=Path, help="Output plot file (default: ingot_plot.png)")
    parser.add_argument("--type", choices=["events", "summary"], default="summary", help="Plot type")
    
    args = parser.parse_args()
    output = args.output or Path("ingot_plot.png")
    
    if args.type == "events":
        plot_ingot_data(args.ingot, output)
    else:
        plot_summary(args.ingot, output)

if __name__ == "__main__":
    main()
