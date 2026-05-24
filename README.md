# Isabella's Job Search - UGA Handshake Scraper

Automated job scraper that pulls criminal justice opportunities from UGA Handshake and integrates them into Isabella's job search website.

## Features

- Automated login to UGA Handshake using Isabella's credentials
- Searches for relevant criminal justice positions using multiple keywords
- Categorizes jobs into Forensics, Court & Office, and Government/Victim Services
- Exports results to JSON
- Integrates Handshake jobs into the existing HTML job board

## Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

You'll also need Chrome and ChromeDriver installed. Install ChromeDriver:

```bash
# On macOS with Homebrew
brew install chromedriver

# Or download from: https://chromedriver.chromium.org/
```

### 2. Configure Credentials

Credentials are stored in `.env` file (already configured):

```
HANDSHAKE_URL=https://uga.joinhandshake.com/
HANDSHAKE_USERNAME=ieg16761
HANDSHAKE_PASSWORD=Lop.bop!2345
```

## Usage

### Step 1: Scrape Jobs from Handshake

Run the scraper to pull jobs from UGA Handshake:

```bash
python3 handshake_scraper.py
```

This will:
- Log into UGA Handshake with Isabella's credentials
- Search for jobs using keywords: criminal justice, forensic, crime scene, victim advocate, court clerk, probation, legal assistant
- Save results to `handshake_jobs.json`

### Step 2: Update the Website

Integrate the Handshake jobs into `index.html`:

```bash
python3 update_jobs.py
```

This will:
- Read jobs from `handshake_jobs.json`
- Add them to the existing job listings in `index.html`
- Update the job count and timestamp

### Step 3: View Results

Open `index.html` in your browser to see the updated job listings with Handshake positions included.

## Files

- **handshake_scraper.py** - Main scraper that logs into Handshake and extracts jobs
- **update_jobs.py** - Integrates Handshake jobs into the HTML website
- **requirements.txt** - Python dependencies
- **.env** - Handshake credentials (never commit to git)
- **handshake_jobs.json** - Output file with scraped jobs
- **index.html** - Job search website

## Customization

### Search Keywords

Edit the `SEARCH_KEYWORDS` list in `handshake_scraper.py`:

```python
SEARCH_KEYWORDS = [
    'criminal justice',
    'forensic',
    'crime scene',
    'victim advocate',
    'court clerk',
    'probation',
    'legal assistant'
]
```

### Job Categories

Jobs are automatically categorized based on title keywords in `handshake_scraper.py:categorize_jobs()`:

- **Forensics** 🔬: forensic, crime scene, lab, technician
- **Court & Office** ⚖️: court, clerk, legal, paralegal, assistant
- **Gov & Victim Services** 🏛️: victim, advocate, probation, government, county, city

## Troubleshooting

### Login Issues

If login fails, try:
1. Check credentials in `.env` file
2. Verify UGA Handshake URL hasn't changed
3. Run with `headless=False` to see the browser: edit `handshake_scraper.py` line 272

### Scraper Not Finding Jobs

Handshake may update their page structure. Check:
1. CSS selectors in `extract_jobs()` method
2. Run with browser visible to inspect the page structure

### ChromeDriver Issues

Make sure ChromeDriver version matches your Chrome browser:
```bash
chromedriver --version
google-chrome --version  # or: /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
```

## Schedule Regular Updates

To automatically refresh jobs daily, set up a cron job:

```bash
crontab -e
```

Add this line to run daily at 9 AM:
```
0 9 * * * cd /Users/robgonzalez/Documents/Claude/Projects/isabella-job-search && python3 handshake_scraper.py && python3 update_jobs.py
```

## Security

- `.env` file is in `.gitignore` and will not be committed
- Never share credentials or commit them to version control
- Handshake login uses Isabella's UGA credentials - keep secure

## Support

Questions? Contact Dad or check the code comments in the Python files.
