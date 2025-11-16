#!/bin/bash
# y.AI.y Installer
# Secure local-first installation script

set -e

echo "======================================"
echo "y.AI.y - Secure Local-First Installer"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Found Python $PYTHON_VERSION"

# Check minimum version (3.9+)
if [ "$(printf '%s\n' "3.9" "$PYTHON_VERSION" | sort -V | head -n1)" != "3.9" ]; then
    echo "❌ Python 3.9 or higher required (found $PYTHON_VERSION)"
    exit 1
fi

echo ""
echo "Installing dependencies..."

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

echo ""
echo "======================================"
echo "✓ Installation Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Start mediator API: python -m yaiy.mediator.api"
echo "  3. Generate signing keys: python -m yaiy.signer.cli generate"
echo "  4. Run UCF simulation: python -m yaiy.simulation.ucf_sim"
echo ""
echo "Documentation: See README.md"
echo "Security: Review SECURITY.md for best practices"
echo ""
