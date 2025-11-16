# Reproducibility Packet

## Overview
This document provides complete instructions for reproducing the y.AI.y ethical awareness system setup and results.

## System Information

**Recording Date:** [YYYY-MM-DD]  
**Operator:** [Name/ID]  
**System Version:** 0.1.0

## Environment Setup

### Python Environment
- Python Version: [e.g., 3.11.5]
- Operating System: [e.g., Ubuntu 22.04]
- Architecture: [e.g., x86_64]

### Dependencies
All dependencies are specified in `requirements.txt`:
```bash
pip install -r requirements.txt
```

Version snapshot:
```
[Include pip freeze output here]
```

## Random Seeds

For reproducible simulation results:

- **UCF Simulation Seed:** `42`
- **Additional Seeds:** [List any other seeds used]

## Cryptographic Keys

### Key Generation
```bash
python -m yaiy.signer.cli generate --output-dir ./keys
```

**Public Key (for verification):**
```
[Include hex-encoded public key here]
```

⚠️ **Private key is NOT included - keep secure and offline**

## Simulation Parameters

### UCF Simulation Configuration
```json
{
  "iterations": 100,
  "seed": 42,
  "context": {
    "note": "reproducibility_test"
  }
}
```

### Policy Configuration
[List all policy rules and settings used]

## Execution Steps

### 1. Setup Environment
```bash
./scripts/install.sh
source venv/bin/activate
```

### 2. Run UCF Simulation
```bash
python -m yaiy.simulation.ucf_sim \
  --iterations 100 \
  --seed 42 \
  --output results/ucf_simulation.json
```

### 3. Generate Plots
```bash
python -m yaiy.plotting.tools \
  results/ucf_simulation.json \
  --plot results/ucf_plot.png \
  --csv results/ucf_data.csv
```

### 4. Sign Results
```bash
python -m yaiy.signer.cli sign \
  --private-key keys/private.key \
  --data results/ucf_simulation.json \
  > results/ucf_simulation_signed.json
```

## Expected Results

### UCF Metrics Summary
- Average Awareness Level: [value]
- Average Ethical Alignment: [value]
- Average Aggregate Score: [value]

### Verification Hashes

**UCF Simulation Output:**
```
SHA256: [hash of ucf_simulation.json]
```

**Signed Results:**
```
Signature: [hex signature]
Public Key: [hex public key]
```

## Verification Instructions

To verify these results:

1. Set up identical environment (same Python version, dependencies)
2. Use the same random seed: `42`
3. Run simulation with identical parameters
4. Compare output hashes
5. Verify signature using public key:
```bash
python -m yaiy.signer.cli verify \
  --public-key [PUBLIC_KEY] \
  --signature [SIGNATURE] \
  --data results/ucf_simulation.json
```

## Notes

- All operations performed offline
- Manual approval required for all actions
- No external network access during execution
- Keys generated using cryptographically secure methods

## Appendix

### Full Configuration Files
[Attach or reference all configuration files]

### System Logs
[Include relevant logs if needed]

### Contact
For questions about this reproducibility packet:
- Email: [contact email]
- Issue tracker: [GitHub issues URL]
