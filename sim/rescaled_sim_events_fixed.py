import random
import math
import json
from typing import List, Dict, Any
from dataclasses import dataclass, asdict

@dataclass
class SimEvent:
    timestamp: float
    event_type: str
    magnitude: float
    suppressed_magnitude: float
    metadata: Dict[str, Any]

class RescaledSimulator:
    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.events: List[SimEvent] = []
        self.seed = seed
    
    def apply_log10_suppression(self, magnitude: float) -> float:
        if magnitude <= 0:
            return 0.0
        return math.log10(magnitude + 1)
    
    def generate_event(self, timestamp: float, event_type: str, base_magnitude: float) -> SimEvent:
        magnitude = base_magnitude * random.uniform(0.8, 1.2)
        suppressed = self.apply_log10_suppression(magnitude)
        
        event = SimEvent(
            timestamp=timestamp,
            event_type=event_type,
            magnitude=magnitude,
            suppressed_magnitude=suppressed,
            metadata={"seed": self.seed}
        )
        self.events.append(event)
        return event
    
    def run_simulation(self, num_events: int = 10) -> List[SimEvent]:
        for i in range(num_events):
            timestamp = i * 1.0
            event_type = random.choice(["ethical_query", "policy_check", "ingot_sign"])
            base_magnitude = random.uniform(1.0, 100.0)
            self.generate_event(timestamp, event_type, base_magnitude)
        
        return self.events
    
    def export_events(self, filepath: str):
        events_data = [asdict(e) for e in self.events]
        with open(filepath, 'w') as f:
            json.dump(events_data, f, indent=2)
        print(f"Exported {len(self.events)} events to {filepath}")
    
    def get_summary(self) -> Dict[str, Any]:
        if not self.events:
            return {"total_events": 0}
        
        return {
            "total_events": len(self.events),
            "avg_magnitude": sum(e.magnitude for e in self.events) / len(self.events),
            "avg_suppressed": sum(e.suppressed_magnitude for e in self.events) / len(self.events),
            "event_types": list(set(e.event_type for e in self.events))
        }

if __name__ == "__main__":
    sim = RescaledSimulator(seed=42)
    sim.run_simulation(num_events=20)
    print(f"Simulation summary: {sim.get_summary()}")
    sim.export_events("sim_events_output.json")
