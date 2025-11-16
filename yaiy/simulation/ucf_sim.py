#!/usr/bin/env python3
"""
Rescaled UCF (Universal Consciousness Function) Simulation

Simulates ethical awareness metrics with reproducible random seeds.
UCF represents a model of consciousness/awareness that can be measured and tracked.
"""
import argparse
import random
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime

from yaiy.utils.canonical_json import canonicalize


@dataclass
class UCFMetrics:
    """Universal Consciousness Function metrics."""
    awareness_level: float  # 0.0 to 1.0
    ethical_alignment: float  # 0.0 to 1.0
    decision_coherence: float  # 0.0 to 1.0
    temporal_consistency: float  # 0.0 to 1.0
    self_reflection: float  # 0.0 to 1.0
    
    def aggregate_score(self) -> float:
        """Calculate aggregate UCF score."""
        weights = {
            'awareness_level': 0.25,
            'ethical_alignment': 0.30,  # Weighted higher
            'decision_coherence': 0.20,
            'temporal_consistency': 0.15,
            'self_reflection': 0.10
        }
        
        return (
            self.awareness_level * weights['awareness_level'] +
            self.ethical_alignment * weights['ethical_alignment'] +
            self.decision_coherence * weights['decision_coherence'] +
            self.temporal_consistency * weights['temporal_consistency'] +
            self.self_reflection * weights['self_reflection']
        )


class UCFSimulator:
    """Simulate UCF metrics with reproducible seeds."""
    
    def __init__(self, seed: int = 42):
        """
        Initialize simulator with random seed.
        
        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        random.seed(seed)
    
    def simulate_step(self, iteration: int, context: Dict[str, Any]) -> UCFMetrics:
        """
        Simulate one step of UCF evolution.
        
        Args:
            iteration: Current iteration number
            context: Simulation context
            
        Returns:
            UCFMetrics for this step
        """
        # Use iteration for deterministic evolution
        step_seed = self.seed + iteration
        random.seed(step_seed)
        
        # Base values with some evolution
        base_awareness = 0.5 + (iteration * 0.01) % 0.5
        
        # Simulate metrics with controlled randomness
        metrics = UCFMetrics(
            awareness_level=min(1.0, base_awareness + random.uniform(-0.1, 0.1)),
            ethical_alignment=min(1.0, 0.7 + random.uniform(-0.15, 0.15)),
            decision_coherence=min(1.0, 0.6 + random.uniform(-0.1, 0.2)),
            temporal_consistency=min(1.0, 0.65 + (iteration * 0.005) % 0.3),
            self_reflection=min(1.0, 0.55 + random.uniform(-0.1, 0.15))
        )
        
        return metrics
    
    def run_simulation(self, iterations: int, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Run full UCF simulation.
        
        Args:
            iterations: Number of iterations to simulate
            context: Simulation context
            
        Returns:
            List of simulation results
        """
        if context is None:
            context = {}
        
        results = []
        
        for i in range(iterations):
            metrics = self.simulate_step(i, context)
            
            result = {
                "iteration": i,
                "timestamp": datetime.utcnow().isoformat(),
                "metrics": asdict(metrics),
                "aggregate_score": metrics.aggregate_score(),
                "seed": self.seed,
                "context": context
            }
            
            results.append(result)
        
        return results


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="UCF Simulation - Reproducible ethical awareness metrics"
    )
    parser.add_argument(
        '--iterations', '-n',
        type=int,
        default=10,
        help='Number of iterations to simulate (default: 10)'
    )
    parser.add_argument(
        '--seed', '-s',
        type=int,
        default=42,
        help='Random seed for reproducibility (default: 42)'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output file for results (default: stdout)'
    )
    
    args = parser.parse_args()
    
    # Run simulation
    simulator = UCFSimulator(seed=args.seed)
    results = simulator.run_simulation(args.iterations)
    
    # Format output
    output = {
        "simulation": "UCF_rescaled",
        "version": "0.1.0",
        "seed": args.seed,
        "iterations": args.iterations,
        "results": results,
        "summary": {
            "avg_awareness": sum(r["metrics"]["awareness_level"] for r in results) / len(results),
            "avg_ethical_alignment": sum(r["metrics"]["ethical_alignment"] for r in results) / len(results),
            "avg_aggregate": sum(r["aggregate_score"] for r in results) / len(results)
        }
    }
    
    # Output results
    canonical_output = canonicalize(output)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(canonical_output)
        print(f"✓ Simulation results written to {args.output}")
    else:
        print(canonical_output)


if __name__ == '__main__':
    main()
