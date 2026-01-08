#!/bin/bash
# Trial Setup Script - Run this once before the demo

set -e

echo "============================================"
echo "FAILURE-DRIVEN LOOP - INTERNAL TRIAL SETUP"
echo "============================================"
echo ""

# Navigate to package
cd "$(dirname "$0")"

# Install package
echo "1. Installing package..."
pip install -e . > /dev/null 2>&1
echo "   ✅ Package installed"
echo ""

# Run verification
echo "2. Running verification tests..."
pytest tests/ -v --tb=short 2>&1 | head -30
echo ""

# Verify CLI commands
echo "3. Checking CLI commands..."
for cmd in fdl-validate-naming fdl-validate-links fdl-log-feedback fdl-analyze-patterns fdl-tree-analyzer; do
    if command -v $cmd > /dev/null 2>&1; then
        echo "   ✅ $cmd"
    else
        echo "   ❌ $cmd NOT FOUND"
    fi
done
echo ""

echo "============================================"
echo "SETUP COMPLETE - Ready for trial"
echo "============================================"
echo ""
echo "Next: Run demo with team using TRIAL_GUIDE.md"
