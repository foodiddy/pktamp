#!/usr/bin/env bash
set -euo pipefail

# Minimal smoke test for Pktamp app

echo "=== Pktamp Smoke Test ==="
echo ""

# Check Python
echo "1. Checking Python version..."
python3 --version

# Check Flask can be imported (if installed)
echo ""
echo "2. Checking Flask availability..."
python3 -c "import flask; print(f'Flask version: {flask.__version__}')" 2>/dev/null || echo "Flask not installed (expected)"

# Check tcpreplay
echo ""
echo "3. Checking tcpreplay..."
which tcpreplay || echo "tcpreplay not installed (will be installed by install.sh)"

# Check install script is executable
echo ""
echo "4. Checking install script..."
if [ -x /home/foo/opencode-sessions/pktamp/install.sh ]; then
    echo "  ✓ install.sh is executable"
else
    echo "  ✗ install.sh is not executable"
fi

# Check install script syntax
echo ""
echo "5. Checking install.sh syntax..."
bash -n /home/foo/opencode-sessions/pktamp/install.sh && echo "  ✓ install.sh has valid syntax"

echo ""
echo "=== Smoke test complete ==="
