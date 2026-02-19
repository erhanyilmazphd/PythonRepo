#!/bin/bash

# Phone Book Web App - Quick Setup Script

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  📱 Phone Book Manager - Web Application Setup                 ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python
echo "✓ Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 not found. Please install Python 3.6+"
    exit 1
fi
python_version=$(python3 --version | cut -d' ' -f2)
echo "  Python $python_version found ✓"
echo ""

# Install Flask
echo "✓ Installing Flask..."
pip install -q Flask 2>/dev/null || pip3 install -q Flask 2>/dev/null
if [ $? -eq 0 ]; then
    echo "  Flask installed ✓"
else
    echo "✗ Failed to install Flask"
    exit 1
fi
echo ""

# Verify Flask
echo "✓ Verifying Flask..."
python3 -c "import flask; print(f'  Flask {flask.__version__} ready ✓')" 2>/dev/null
echo ""

# Check files
echo "✓ Checking files..."
if [ -f "app.py" ]; then
    echo "  app.py found ✓"
else
    echo "✗ app.py not found"
    exit 1
fi

if [ -d "templates" ] && [ -f "templates/index.html" ]; then
    echo "  templates/index.html found ✓"
else
    echo "✗ templates/index.html not found"
    exit 1
fi

if [ -f "phonebook.py" ]; then
    echo "  phonebook.py found ✓"
else
    echo "✗ phonebook.py not found"
    exit 1
fi
echo ""

# Ready to launch
echo "════════════════════════════════════════════════════════════════"
echo "✅ Everything is ready!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "🚀 Starting Phone Book Web Application..."
echo ""
echo "📍 Your app will open at: http://127.0.0.1:5000"
echo "📝 Press Ctrl+C to stop"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""

# Launch app
python3 app.py
