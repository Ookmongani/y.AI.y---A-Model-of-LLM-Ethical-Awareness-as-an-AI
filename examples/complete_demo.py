#!/usr/bin/env python3
"""
Complete Usage Example for y.AI.y

This script demonstrates a full workflow using all components:
1. Generate keys
2. Run simulation
3. Sign results
4. Validate policies
5. Generate visualizations
"""

import sys
from pathlib import Path
import json

# Add yaiy to path
sys.path.insert(0, str(Path(__file__).parent))

from yaiy.signer.cli import generate_keypair, sign_data
from yaiy.simulation import UCFSimulator
from yaiy.policy import PolicyEngine, PolicyRule, RiskLevel
from yaiy.utils import canonicalize, hash_canonical
from yaiy.plotting.tools import convert_to_csv

print("=" * 70)
print("y.AI.y - Complete Usage Example")
print("=" * 70)
print()

# 1. Generate cryptographic keys
print("Step 1: Generating Ed25519 keypair...")
keys_dir = Path("./demo_keys")
if not keys_dir.exists():
    generate_keypair(keys_dir)
else:
    print("  ✓ Keys already exist, skipping generation")
print()

# 2. Initialize policy engine
print("Step 2: Initializing policy engine...")
engine = PolicyEngine()

# Add custom policy
custom_rule = PolicyRule(
    name="demo_safety_check",
    description="Demo safety validation",
    risk_level=RiskLevel.MEDIUM,
    auto_approve=False
)
engine.add_rule(custom_rule)
print(f"  ✓ Loaded {len(engine.rules)} policy rules")
print()

# 3. Run UCF simulation
print("Step 3: Running UCF simulation...")
simulator = UCFSimulator(seed=42)
results = simulator.run_simulation(iterations=10, context={"demo": True})
print(f"  ✓ Completed {len(results)} simulation iterations")
print(f"  ✓ Average ethical alignment: {sum(r['metrics']['ethical_alignment'] for r in results) / len(results):.3f}")
print()

# 4. Canonicalize results
print("Step 4: Canonicalizing simulation results...")
sim_data = {
    "simulation": "ucf_demo",
    "iterations": 10,
    "seed": 42,
    "results": results[:3]  # First 3 for demo
}
canonical = canonicalize(sim_data)
data_hash = hash_canonical(sim_data)
print(f"  ✓ Canonical hash: {data_hash[:16]}...")
print()

# 5. Evaluate action with policy engine
print("Step 5: Evaluating action with policy engine...")
evaluation = engine.evaluate(
    "run_simulation",
    {"seed": 42, "iterations": 10}
)
print(f"  ✓ Decision: {evaluation.decision.value}")
print(f"  ✓ Risk level: {evaluation.risk_level.value}")
print(f"  ✓ Requires approval: {evaluation.requires_approval}")
print()

# 6. Manual approval
print("Step 6: Recording manual approval...")
approval = engine.approve_action(
    "run_simulation",
    "demo_operator",
    {"note": "approved for demonstration"}
)
print(f"  ✓ Approval recorded at {approval['timestamp']}")
print()

# 7. Save results
print("Step 7: Saving results...")
output_dir = Path("./demo_output")
output_dir.mkdir(exist_ok=True)

# Save simulation data
sim_file = output_dir / "simulation.json"
with open(sim_file, 'w') as f:
    f.write(canonicalize(sim_data))
print(f"  ✓ Saved simulation to {sim_file}")

# Save approval record
approval_file = output_dir / "approval.json"
with open(approval_file, 'w') as f:
    f.write(canonicalize(approval))
print(f"  ✓ Saved approval to {approval_file}")

# Convert to CSV (full results)
full_sim_data = {
    "simulation": "ucf_demo",
    "seed": 42,
    "iterations": 10,
    "results": results
}
csv_file = output_dir / "simulation.csv"
convert_to_csv(full_sim_data, csv_file)
print(f"  ✓ Saved CSV to {csv_file}")
print()

# 8. Display summary
print("=" * 70)
print("Demo Complete! Summary:")
print("=" * 70)
print()
print(f"Keys generated:      {keys_dir}/")
print(f"Policy rules loaded: {len(engine.rules)}")
print(f"Simulation runs:     {len(results)}")
print(f"Results hash:        {data_hash[:32]}...")
print(f"Output directory:    {output_dir}/")
print()
print("Next steps:")
print("  1. Sign the results:")
print(f"     python -m yaiy.signer.cli sign \\")
print(f"       --private-key {keys_dir}/private.key \\")
print(f"       --data {sim_file}")
print()
print("  2. Generate visualizations:")
print(f"     python -m yaiy.plotting.tools {output_dir}/simulation.csv \\")
print(f"       --plot {output_dir}/plot.png")
print()
print("  3. Start the mediator API:")
print("     python -m yaiy.mediator.api")
print()
print("=" * 70)
