"""Tests for UCF simulation."""
import pytest
from yaiy.simulation import UCFSimulator, UCFMetrics


def test_ucf_metrics_aggregate():
    """Test UCF metrics aggregation."""
    metrics = UCFMetrics(
        awareness_level=0.8,
        ethical_alignment=0.9,
        decision_coherence=0.7,
        temporal_consistency=0.6,
        self_reflection=0.5
    )
    
    score = metrics.aggregate_score()
    assert 0.0 <= score <= 1.0
    # Ethical alignment is weighted highest, should influence score
    assert score > 0.6


def test_simulator_reproducibility():
    """Test that same seed produces same results."""
    sim1 = UCFSimulator(seed=42)
    sim2 = UCFSimulator(seed=42)
    
    results1 = sim1.run_simulation(5)
    results2 = sim2.run_simulation(5)
    
    # Same seed should produce identical results
    for r1, r2 in zip(results1, results2):
        assert r1["metrics"] == r2["metrics"]


def test_simulator_different_seeds():
    """Test that different seeds produce different results."""
    sim1 = UCFSimulator(seed=42)
    sim2 = UCFSimulator(seed=99)
    
    results1 = sim1.run_simulation(5)
    results2 = sim2.run_simulation(5)
    
    # Different seeds should produce different results
    # At least one metric should differ
    different = False
    for r1, r2 in zip(results1, results2):
        if r1["metrics"] != r2["metrics"]:
            different = True
            break
    
    assert different


def test_simulation_iterations():
    """Test simulation produces correct number of iterations."""
    sim = UCFSimulator(seed=42)
    iterations = 10
    results = sim.run_simulation(iterations)
    
    assert len(results) == iterations


def test_metrics_in_range():
    """Test that all metrics are in valid range [0, 1]."""
    sim = UCFSimulator(seed=42)
    results = sim.run_simulation(10)
    
    for result in results:
        metrics = result["metrics"]
        for key, value in metrics.items():
            assert 0.0 <= value <= 1.0, f"{key} out of range: {value}"


def test_simulation_step():
    """Test individual simulation step."""
    sim = UCFSimulator(seed=42)
    metrics = sim.simulate_step(0, {})
    
    assert isinstance(metrics, UCFMetrics)
    assert 0.0 <= metrics.awareness_level <= 1.0
    assert 0.0 <= metrics.ethical_alignment <= 1.0
