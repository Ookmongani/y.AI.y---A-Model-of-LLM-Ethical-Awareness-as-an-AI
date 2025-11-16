#!/bin/bash
set -e

echo "=== y.AI.y Ethical Anchor Installer ==="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

echo "Python 3 found: $(python3 --version)"
echo ""

echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo ""
echo "Creating necessary directories..."
mkdir -p packet keys

echo ""
echo "Running unit tests..."
python3 unit/unit_check.py

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Next steps:"
echo "1. Generate keypair: python3 signer/sign_ingot.py generate"
echo "2. Start mediator: python3 mediator/main.py"
echo "3. Run simulator: python3 sim/rescaled_sim_events_fixed.py"
echo "4. Run tests: python3 unit/unit_check.py"
echo ""
echo "WARNING: Keep private keys offline and secure!"
echo "         No network calls by default - all local-first."
