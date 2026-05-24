#!/bin/bash
# Setup script for Isabella's Handshake job scraper

echo "=========================================="
echo "Isabella's Handshake Scraper Setup"
echo "=========================================="
echo ""

# Check Python
echo "Checking Python installation..."
python3 --version || { echo "ERROR: Python 3 not found"; exit 1; }
echo "✓ Python installed"
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt || { echo "ERROR: Failed to install dependencies"; exit 1; }
echo "✓ Dependencies installed"
echo ""

# Check for ChromeDriver
echo "Checking for ChromeDriver..."
if command -v chromedriver &> /dev/null; then
    echo "✓ ChromeDriver found: $(chromedriver --version)"
else
    echo "⚠ ChromeDriver not found"
    echo ""
    echo "Please install ChromeDriver:"
    echo "  macOS: brew install chromedriver"
    echo "  Or download from: https://chromedriver.chromium.org/"
    echo ""
fi

# Check .env file
if [ -f .env ]; then
    echo "✓ .env file found"
else
    echo "⚠ .env file not found - credentials needed"
fi

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Usage:"
echo "  1. Run scraper:     python3 handshake_scraper.py"
echo "  2. Update website:  python3 update_jobs.py"
echo "  3. Open index.html in your browser"
echo ""
