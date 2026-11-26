#!/bin/bash

echo "🚀 Setting up SecScanner..."

python3 -m venv .venv

source .venv/bin/activate

python -m pip install --upgrade pip

pip install -r requirements.txt

echo ""
echo "✅ SecScanner setup complete!"
echo ""
echo "Next steps:"
echo "  source .venv/bin/activate"
echo "  python scanner.py vulnerable.py"