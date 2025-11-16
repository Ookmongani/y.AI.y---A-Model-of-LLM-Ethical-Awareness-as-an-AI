#!/usr/bin/env python3
"""
Plotting and Conversion Tools for y.AI.y

Generate visualizations of UCF metrics and ethical awareness data.
"""
import argparse
import json
from pathlib import Path
from typing import List, Dict, Any

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for offline use
import matplotlib.pyplot as plt
import numpy as np


def plot_ucf_metrics(data: Dict[str, Any], output_path: Path):
    """
    Plot UCF simulation metrics.
    
    Args:
        data: Simulation data with results
        output_path: Path to save plot
    """
    results = data.get('results', [])
    
    if not results:
        raise ValueError("No results to plot")
    
    # Extract data
    iterations = [r['iteration'] for r in results]
    awareness = [r['metrics']['awareness_level'] for r in results]
    ethical = [r['metrics']['ethical_alignment'] for r in results]
    coherence = [r['metrics']['decision_coherence'] for r in results]
    temporal = [r['metrics']['temporal_consistency'] for r in results]
    reflection = [r['metrics']['self_reflection'] for r in results]
    aggregate = [r['aggregate_score'] for r in results]
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f'UCF Metrics Simulation (seed={data.get("seed", "?")})', fontsize=16)
    
    # Plot 1: All metrics over time
    ax1 = axes[0, 0]
    ax1.plot(iterations, awareness, label='Awareness', marker='o')
    ax1.plot(iterations, ethical, label='Ethical Alignment', marker='s')
    ax1.plot(iterations, coherence, label='Coherence', marker='^')
    ax1.plot(iterations, temporal, label='Temporal', marker='d')
    ax1.plot(iterations, reflection, label='Self-Reflection', marker='*')
    ax1.set_xlabel('Iteration')
    ax1.set_ylabel('Metric Value')
    ax1.set_title('Individual Metrics')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Aggregate score
    ax2 = axes[0, 1]
    ax2.plot(iterations, aggregate, color='purple', linewidth=2, marker='o')
    ax2.fill_between(iterations, aggregate, alpha=0.3, color='purple')
    ax2.set_xlabel('Iteration')
    ax2.set_ylabel('Aggregate Score')
    ax2.set_title('UCF Aggregate Score')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Metric distribution (final state)
    ax3 = axes[1, 0]
    final_metrics = {
        'Awareness': awareness[-1],
        'Ethical': ethical[-1],
        'Coherence': coherence[-1],
        'Temporal': temporal[-1],
        'Reflection': reflection[-1]
    }
    bars = ax3.bar(final_metrics.keys(), final_metrics.values())
    ax3.set_ylabel('Value')
    ax3.set_title('Final Metric Values')
    ax3.set_ylim(0, 1.0)
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Color bars by value
    colors = ['green' if v > 0.7 else 'orange' if v > 0.5 else 'red' for v in final_metrics.values()]
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    
    # Plot 4: Statistics
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    stats_text = f"""
    Simulation Statistics
    ───────────────────
    Iterations: {len(iterations)}
    Seed: {data.get('seed', 'N/A')}
    
    Average Values:
    • Awareness: {np.mean(awareness):.3f}
    • Ethical: {np.mean(ethical):.3f}
    • Coherence: {np.mean(coherence):.3f}
    • Temporal: {np.mean(temporal):.3f}
    • Reflection: {np.mean(reflection):.3f}
    
    Aggregate Score:
    • Mean: {np.mean(aggregate):.3f}
    • Min: {np.min(aggregate):.3f}
    • Max: {np.max(aggregate):.3f}
    """
    
    ax4.text(0.1, 0.5, stats_text, fontsize=10, family='monospace',
             verticalalignment='center')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✓ Plot saved to {output_path}")


def convert_to_csv(data: Dict[str, Any], output_path: Path):
    """
    Convert simulation data to CSV format.
    
    Args:
        data: Simulation data
        output_path: Path to save CSV
    """
    results = data.get('results', [])
    
    if not results:
        raise ValueError("No results to convert")
    
    # Create CSV
    with open(output_path, 'w') as f:
        # Header
        f.write("iteration,timestamp,awareness_level,ethical_alignment,decision_coherence,")
        f.write("temporal_consistency,self_reflection,aggregate_score\n")
        
        # Data rows
        for r in results:
            m = r['metrics']
            f.write(f"{r['iteration']},{r['timestamp']},")
            f.write(f"{m['awareness_level']},{m['ethical_alignment']},{m['decision_coherence']},")
            f.write(f"{m['temporal_consistency']},{m['self_reflection']},{r['aggregate_score']}\n")
    
    print(f"✓ CSV saved to {output_path}")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Plotting and conversion tools for y.AI.y"
    )
    parser.add_argument(
        'input',
        type=Path,
        help='Input JSON file with simulation data'
    )
    parser.add_argument(
        '--plot', '-p',
        type=Path,
        help='Generate plot and save to file'
    )
    parser.add_argument(
        '--csv', '-c',
        type=Path,
        help='Convert to CSV and save to file'
    )
    
    args = parser.parse_args()
    
    # Load data
    with open(args.input, 'r') as f:
        data = json.load(f)
    
    # Generate outputs
    if args.plot:
        plot_ucf_metrics(data, args.plot)
    
    if args.csv:
        convert_to_csv(data, args.csv)
    
    if not args.plot and not args.csv:
        print("No output specified. Use --plot or --csv")


if __name__ == '__main__':
    main()
