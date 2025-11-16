#!/usr/bin/env python3
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.canonicalize import canonicalize_json, canonicalize_bytes
from policy_engine.policy_engine import PolicyEngine
from sim.rescaled_sim_events_fixed import RescaledSimulator

class TestCanonicalize(unittest.TestCase):
    def test_canonicalize_json(self):
        data = {"b": 2, "a": 1}
        result = canonicalize_json(data)
        self.assertEqual(result, '{"a":1,"b":2}')
    
    def test_canonicalize_bytes(self):
        data = {"x": "test"}
        result = canonicalize_bytes(data)
        self.assertIsInstance(result, bytes)
        self.assertEqual(result, b'{"x":"test"}')

class TestPolicyEngine(unittest.TestCase):
    def test_evaluate_valid_action(self):
        engine = PolicyEngine()
        action = {"network_access": False, "approved": True}
        result = engine.evaluate(action)
        self.assertIn("approved", result)
    
    def test_no_network_rule(self):
        engine = PolicyEngine()
        action = {"network_access": True, "approved": True}
        result = engine.evaluate(action)
        self.assertIsInstance(result["violations"], list)

class TestSimulator(unittest.TestCase):
    def test_reproducible_seed(self):
        sim1 = RescaledSimulator(seed=42)
        sim1.run_simulation(5)
        
        sim2 = RescaledSimulator(seed=42)
        sim2.run_simulation(5)
        
        self.assertEqual(len(sim1.events), len(sim2.events))
        self.assertEqual(sim1.events[0].magnitude, sim2.events[0].magnitude)
    
    def test_log10_suppression(self):
        sim = RescaledSimulator()
        result = sim.apply_log10_suppression(100.0)
        self.assertAlmostEqual(result, 2.004, places=2)
    
    def test_event_generation(self):
        sim = RescaledSimulator()
        event = sim.generate_event(0.0, "test", 10.0)
        self.assertIsNotNone(event)
        self.assertEqual(event.event_type, "test")

def run_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestCanonicalize))
    suite.addTests(loader.loadTestsFromTestCase(TestPolicyEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestSimulator))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
