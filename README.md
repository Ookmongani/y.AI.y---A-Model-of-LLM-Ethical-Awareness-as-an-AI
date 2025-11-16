# y.AI.y - A Model of LLM Ethical Awareness as an AI

This is a working model of Ethical Awareness in LLMs, featuring a secure, local-first architecture for ethical AI anchoring. The project includes tools for ingot signing, policy enforcement, and event simulation with reproducible seeds.

## Features

- **Local-First Security**: No network calls by default, all operations offline
- **Ed25519 Signing**: Cryptographic signing of ingots with offline key management
- **Policy Engine**: Ethical rule enforcement based on ethics_spec.json
- **Event Simulation**: Reproducible event generation with log10 suppression
- **Canonical JSON**: Deterministic byte representation for signing
- **FastAPI Mediator**: Localhost-only API for ingesting and exporting ingots

## Installation

```bash
# Run the installer
bash installer/installer.sh

# Or install manually
pip install -r requirements.txt
```

## Usage

### 1. Generate Keypair (Offline)

```bash
python3 signer/sign_ingot.py generate --output-dir keys
```

**WARNING**: Keep `keys/private_key.pem` offline and secure!

### 2. Start the Mediator (Localhost Only)

```bash
python3 mediator/main.py
# Server runs on http://127.0.0.1:8000
```

### 3. Run the Simulator

```bash
python3 sim/rescaled_sim_events_fixed.py
```

### 4. Sign an Ingot (Offline, Manual Approval)

```bash
python3 signer/sign_ingot.py sign packet/ingot_001_unsigned.json --key keys/private_key.pem
```

### 5. Verify a Signature

```bash
python3 signer/sign_ingot.py verify packet/ingot_001_signed.json --pubkey keys/public_key.pem
```

### 6. Run Tests

```bash
python3 unit/unit_check.py
```

### 7. Convert and Plot Ingots

```bash
# Convert to canonical format
python3 tools/convert_ingot.py packet/ingot_001_unsigned.json

# Plot ingot data
python3 tools/plot_ingot.py packet/ingot_001_unsigned.json --output plot.png
```

## Architecture

```
├── mediator/          # FastAPI server (localhost only)
├── signer/            # Ed25519 signing CLI (offline)
├── utils/             # Canonical JSON utilities
├── policy_engine/     # Ethical rule enforcement
├── sim/               # Event-driven simulator
├── tools/             # Ingot conversion and plotting
├── unit/              # Unit tests
├── packet/            # Ingot templates and test vectors
├── ethics/            # Ethics specification
└── installer/         # Installation script
```

## Safe Defaults

- ✓ No network calls
- ✓ Manual approval for forwarding
- ✓ Private keys kept offline
- ✓ Reproducible seeds (seed=42)
- ✓ Canonical JSON bytes
- ✓ Unit tests included

## License

Apache 2.0 - See LICENSE file

## Patent Non-Assertion

See PATENT_NONASSERTION.md for patent pledge details.
