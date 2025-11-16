# Quick Start Guide

Get up and running with y.AI.y in 5 minutes.

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Ookmongani/y.AI.y---A-Model-of-LLM-Ethical-Awareness-as-an-AI.git
cd y.AI.y---A-Model-of-LLM-Ethical-Awareness-as-an-AI
```

### 2. Install Dependencies

**Option A: Using the installer (recommended)**
```bash
chmod +x scripts/install.sh
./scripts/install.sh
source venv/bin/activate
```

**Option B: Manual installation**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Quick Examples

### Example 1: Generate Signing Keys

```bash
# Generate Ed25519 keypair
python -m yaiy.signer.cli generate --output-dir ./my_keys

# Output:
# ✓ Keypair generated successfully
#   Private key: ./my_keys/private.key (KEEP SECURE!)
#   Public key:  ./my_keys/public.key
#   Public key (hex): [hex string]
```

### Example 2: Run UCF Simulation

```bash
# Run a simulation with 20 iterations
python -m yaiy.simulation.ucf_sim \
  --iterations 20 \
  --seed 42 \
  --output simulation_results.json

# Check the results
cat simulation_results.json
```

### Example 3: Sign Data

```bash
# Sign simulation results
python -m yaiy.signer.cli sign \
  --private-key ./my_keys/private.key \
  --data simulation_results.json \
  > simulation_results_signed.json

# The signed output includes:
# - Original data
# - Digital signature
# - Public key for verification
```

### Example 4: Generate Visualizations

```bash
# Create plot and CSV export
python -m yaiy.plotting.tools simulation_results.json \
  --plot ucf_metrics.png \
  --csv ucf_metrics.csv

# View the CSV
head ucf_metrics.csv

# Open ucf_metrics.png to see the visualizations
```

### Example 5: Start the Mediator API

```bash
# Start the FastAPI service
python -m yaiy.mediator.api

# In another terminal, test the API
curl http://localhost:8000/health
curl http://localhost:8000/policies
```

### Example 6: Validate an Ingot

```bash
# Validate an unsigned ingot
curl -X POST http://localhost:8000/validate-ingot \
  -H "Content-Type: application/json" \
  -d @examples/ingot_policy_config.json
```

## Running Tests

```bash
# Run all tests
pytest yaiy/tests/ -v

# Run with coverage
pytest yaiy/tests/ --cov=yaiy --cov-report=html

# Open coverage report
# open htmlcov/index.html  # macOS
# xdg-open htmlcov/index.html  # Linux
```

## Complete Workflow Example

Here's a complete workflow demonstrating the entire system:

```bash
# 1. Setup
./scripts/install.sh
source venv/bin/activate

# 2. Generate keys
python -m yaiy.signer.cli generate --output-dir ./secure_keys

# 3. Run simulation
python -m yaiy.simulation.ucf_sim \
  --iterations 50 \
  --seed 12345 \
  --output results/sim_50.json

# 4. Sign the results
python -m yaiy.signer.cli sign \
  --private-key ./secure_keys/private.key \
  --data results/sim_50.json \
  > results/sim_50_signed.json

# 5. Generate visualizations
python -m yaiy.plotting.tools results/sim_50.json \
  --plot results/sim_50_plot.png \
  --csv results/sim_50_data.csv

# 6. Start the API (in background or separate terminal)
python -m yaiy.mediator.api &

# 7. Test the API
curl http://localhost:8000/health

# 8. Evaluate an action
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "action": "model_inference",
    "context": {"model": "test"},
    "requester": "researcher"
  }'
```

## What's Next?

- Read the full [README_YAIY.md](README_YAIY.md) for detailed documentation
- Review [SECURITY.md](SECURITY.md) for security best practices
- Check [docs/REPRODUCIBILITY_TEMPLATE.md](docs/REPRODUCIBILITY_TEMPLATE.md) for reproducibility guidelines
- Explore the example ingots in `examples/`
- Write custom policy rules using the policy engine
- Integrate with your LLM workflow

## Common Issues

### "Module not found" errors
Make sure you've activated the virtual environment:
```bash
source venv/bin/activate
```

### Permission errors with keys
The private key should have restricted permissions:
```bash
chmod 600 ./my_keys/private.key
```

### Port already in use (8000)
Change the port when starting the mediator:
```bash
python -c "from yaiy.mediator import app; import uvicorn; uvicorn.run(app, host='127.0.0.1', port=8001)"
```

## Getting Help

- Check the documentation in `docs/`
- Look at the example files in `examples/`
- Run tests to understand component behavior
- Review the source code - it's well-documented!

---

**Ready to dive deeper? See README_YAIY.md for the complete documentation.**
