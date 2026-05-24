#!/bin/bash
# Run the complete Handshake scraping workflow

echo "=========================================="
echo "Isabella's Handshake Job Scraper"
echo "=========================================="
echo ""

# Check dependencies
if ! python3 -c "import selenium; from dotenv import load_dotenv" 2>/dev/null; then
    echo "ERROR: Dependencies not installed"
    echo "Run: pip3 install -r requirements.txt"
    exit 1
fi

# Check for ChromeDriver
if ! command -v chromedriver &> /dev/null; then
    echo "ERROR: ChromeDriver not found"
    echo ""
    echo "Install ChromeDriver:"
    echo "  macOS: brew install chromedriver"
    echo "  Or: https://chromedriver.chromium.org/"
    exit 1
fi

# Check .env
if [ ! -f .env ]; then
    echo "ERROR: .env file not found"
    echo "Create .env with Handshake credentials"
    exit 1
fi

echo "Step 1: Scraping jobs from UGA Handshake..."
echo ""
python3 handshake_scraper.py

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Scraper failed"
    exit 1
fi

echo ""
echo "Step 2: Updating index.html with new jobs..."
echo ""
python3 update_jobs.py

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Update failed"
    exit 1
fi

echo ""
echo "=========================================="
echo "✓ Complete! Open index.html to view jobs"
echo "=========================================="
