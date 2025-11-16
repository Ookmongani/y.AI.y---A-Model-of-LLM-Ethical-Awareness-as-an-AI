# y.AI.y - Secure Local-First LLM Ethical Awareness Framework

A comprehensive framework for implementing ethical awareness in Large Language Models (LLMs) with security, reproducibility, and offline-first operation as core principles.

## 🔒 Security-First Design

- **Offline-First Operation**: All components designed to work without internet access
- **Manual Approval Required**: No automatic execution of sensitive operations
- **Cryptographic Signing**: Ed25519 signatures for all critical data (ingots)
- **Verified Downloads**: Model weights must be manually verified before use
- **No Bundled Weights**: Security through explicit verification, not convenience

## 📦 Components

### 1. FastAPI Mediator Service
HTTP API for mediating interactions with the ethical awareness system.

```bash
# Start the mediator
python -m yaiy.mediator.api
```

**Endpoints:**
- `GET /` - Service info
- `GET /health` - Health check
- `POST /evaluate` - Evaluate action against policies
- `POST /approve` - Record manual approval
- `POST /validate-ingot` - Validate data ingots
- `GET /policies` - List policy rules
- `GET /offline-status` - Check offline mode status

### 2. Ed25519 Signer CLI
Offline cryptographic signing tool for data integrity.

```bash
# Generate keypair
python -m yaiy.signer.cli generate --output-dir ./keys

# Sign data
echo '{"data": "example"}' | python -m yaiy.signer.cli sign --private-key ./keys/private.key

# Verify signature
python -m yaiy.signer.cli verify \
  --public-key <PUBLIC_KEY_HEX> \
  --signature <SIGNATURE_HEX> \
  --data data.json
```

### 3. Canonical JSON Utilities
Deterministic JSON serialization for reproducibility.

```python
from yaiy.utils import canonicalize, hash_canonical

# Canonicalize data
canonical = canonicalize({"b": 2, "a": 1})  # Always produces: {"a":1,"b":2}

# Generate deterministic hash
hash_value = hash_canonical(data)
```

### 4. UCF Simulation
Rescaled Universal Consciousness Function simulation with reproducible seeds.

```bash
# Run simulation
python -m yaiy.simulation.ucf_sim \
  --iterations 100 \
  --seed 42 \
  --output results.json
```

**Metrics:**
- Awareness Level
- Ethical Alignment (weighted highest)
- Decision Coherence
- Temporal Consistency
- Self-Reflection

### 5. Lightweight Policy Engine
Ethical awareness policy enforcement.

```python
from yaiy.policy import PolicyEngine

engine = PolicyEngine()
evaluation = engine.evaluate("action_name", context={})
# All actions require manual approval by default
```

**Default Policies:**
- Data access control (HIGH risk)
- Model execution approval (MEDIUM risk)
- External communication blocking (CRITICAL risk)
- Parameter modification prevention (HIGH risk)
- Ingot signature verification (CRITICAL risk)

### 6. Plotting & Conversion Tools
Visualization and data export utilities.

```bash
# Generate plots
python -m yaiy.plotting.tools results.json --plot output.png

# Export to CSV
python -m yaiy.plotting.tools results.json --csv output.csv
```

### 7. Model Weight Download Scripts
Secure, verified model weight management (manual download only).

```bash
# Get download instructions
python scripts/download_models.py \
  --model example-model \
  --hash <EXPECTED_SHA256> \
  --source-url <VERIFIED_SOURCE>

# Verify downloaded weights
python scripts/download_models.py \
  --verify weights.bin \
  --hash <EXPECTED_SHA256>
```

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone <repository-url>
cd y.AI.y---A-Model-of-LLM-Ethical-Awareness-as-an-AI

# Run installer
chmod +x scripts/install.sh
./scripts/install.sh

# Activate environment
source venv/bin/activate
```

### Basic Usage

```bash
# 1. Generate signing keys
python -m yaiy.signer.cli generate

# 2. Start the mediator API
python -m yaiy.mediator.api

# 3. In another terminal, run a simulation
python -m yaiy.simulation.ucf_sim --iterations 10 --output sim.json

# 4. Generate visualizations
python -m yaiy.plotting.tools sim.json --plot sim.png --csv sim.csv

# 5. Sign the results
python -m yaiy.signer.cli sign --private-key keys/private.key --data sim.json > sim_signed.json
```

## 📋 Example Ingots

Ingots are signed data packets containing configurations or metadata. See `examples/` for:

- `ingot_policy_config.json` - Policy configuration example
- `ingot_ucf_params.json` - UCF simulation parameters
- `ingot_model_metadata.json` - Model metadata example

**⚠️ All example ingots are UNSIGNED. Sign before production use.**

## 🧪 Testing

```bash
# Run all tests
pytest yaiy/tests/ -v

# Run with coverage
pytest yaiy/tests/ --cov=yaiy --cov-report=html
```

## 🔐 Security Best Practices

1. **Never commit private keys** - Keep signing keys offline and secure
2. **Verify all ingots** - Use Ed25519 signatures for critical data
3. **Manual approval workflow** - Review all actions before execution
4. **Offline operation** - Disable network access for sensitive operations
5. **Reproducible seeds** - Use fixed seeds for reproducibility
6. **Hash verification** - Always verify model weight hashes

## 📊 Reproducibility

All components support reproducible execution:

- Fixed random seeds for simulations
- Canonical JSON for deterministic serialization
- Cryptographic signatures for data integrity
- Full environment documentation in reproducibility packets

See `docs/REPRODUCIBILITY_TEMPLATE.md` for detailed instructions.

## 🏗️ Architecture

```
y.AI.y/
├── yaiy/
│   ├── mediator/        # FastAPI service
│   ├── signer/          # Ed25519 CLI
│   ├── utils/           # Canonical JSON utilities
│   ├── policy/          # Policy engine
│   ├── simulation/      # UCF simulation
│   ├── plotting/        # Visualization tools
│   └── tests/           # Unit tests
├── scripts/
│   ├── install.sh       # Installer
│   └── download_models.py  # Model verification
├── examples/            # Example ingots (unsigned)
└── docs/                # Documentation
```

## 🤝 Contributing

This is a security-focused project. Contributions should maintain:

- Offline-first operation
- Manual approval requirements
- Cryptographic verification
- Reproducibility
- Comprehensive testing

## 📄 License

See LICENSE file for details.

## 🔍 Philosophy

y.AI.y implements a model of ethical awareness in LLMs based on:

1. **Transparency**: All operations are logged and auditable
2. **Consent**: Manual approval required for all actions
3. **Verification**: Cryptographic signatures ensure integrity
4. **Reproducibility**: Fixed seeds and canonical formats
5. **Offline-First**: No dependency on external services
6. **Security**: Defense in depth with multiple verification layers

## 📞 Support

For issues, questions, or contributions:
- GitHub Issues: [Repository issues page]
- Documentation: See `docs/` directory
- Examples: See `examples/` directory

---

**Built with security, ethics, and reproducibility as core principles.**
