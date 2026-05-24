# Quick Start Guide - UGA Handshake Scraper

## Prerequisites

1. **Install ChromeDriver** (required for web scraping):
   ```bash
   brew install chromedriver
   ```
   
   Or download from: https://chromedriver.chromium.org/

2. **Install Python dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

## Running the Scraper

### Option 1: Automatic (Recommended)

Run the complete workflow with one command:

```bash
./run_scraper.sh
```

This will:
1. Scrape jobs from UGA Handshake
2. Update `index.html` with new listings
3. Show you the results

### Option 2: Manual Steps

**Step 1:** Scrape jobs from Handshake
```bash
python3 handshake_scraper.py
```

**Step 2:** Update the website
```bash
python3 update_jobs.py
```

**Step 3:** Open `index.html` in your browser

## Testing

Test that credentials are working:
```bash
python3 test_credentials.py
```

## What Gets Scraped

The scraper searches for jobs using these keywords:
- Criminal justice
- Forensic
- Crime scene
- Victim advocate
- Court clerk
- Probation
- Legal assistant

Jobs are automatically categorized into:
- 🔬 Forensics & Crime Scene
- ⚖️ Court & Office
- 🏛️ Government & Victim Services

## Files Created

After running the scraper:
- `handshake_jobs.json` - Raw job data from Handshake
- `index.html` - Updated with new listings

## Troubleshooting

### "ChromeDriver not found"
Install ChromeDriver with: `brew install chromedriver`

### "Login failed"
1. Check that `.env` file has correct credentials
2. Try running with browser visible: edit `handshake_scraper.py` line 272, change `headless=False`

### "No jobs found"
- Handshake may have changed their page structure
- Jobs may not match your search keywords
- Try running with browser visible to see what's happening

## Scheduling Automatic Updates

To run daily at 9 AM:

```bash
crontab -e
```

Add this line:
```
0 9 * * * cd /Users/robgonzalez/Documents/Claude/Projects/isabella-job-search && ./run_scraper.sh
```

## Security Note

The `.env` file contains Isabella's Handshake credentials and is already in `.gitignore`. Never commit credentials to version control.

## Need Help?

Check the full README.md for detailed documentation.
