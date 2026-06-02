#!/usr/bin/env python3
"""
UGA Handshake Job Scraper
Logs into UGA Handshake and pulls relevant job listings for Isabella's criminal justice search
"""

import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Load credentials from .env
load_dotenv()
HANDSHAKE_URL = os.getenv('HANDSHAKE_URL')
USERNAME = os.getenv('HANDSHAKE_USERNAME')
PASSWORD = os.getenv('HANDSHAKE_PASSWORD')

# Search keywords for criminal justice positions
SEARCH_KEYWORDS = [
    'criminal justice',
    'forensic',
    'forensic technician',
    'forensic science',
    'crime scene',
    'victim advocate',
    'court clerk',
    'probation',
    'legal assistant',
    'evidence technician',
    'evidence tech'
]

class HandshakeScraper:
    def __init__(self, headless=True):
        """Initialize the scraper with Chrome WebDriver"""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        
        # Use webdriver_manager to automatically get the correct ChromeDriver version
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 15)
        self.jobs = []
    
    def login(self):
        """Login to UGA Handshake via UGA SSO"""
        print(f"Navigating to {HANDSHAKE_URL}")
        self.driver.get(HANDSHAKE_URL)
        time.sleep(5)
        
        try:
            # Handshake uses UGA SSO - click the "University of Georgia Sign On" link
            print("Looking for UGA SSO link...")
            sso_link = None
            
            # Try to find the UGA SSO link
            try:
                sso_link = self.driver.find_element(By.PARTIAL_LINK_TEXT, "University of Georgia")
            except NoSuchElementException:
                try:
                    sso_link = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Sign On")
                except NoSuchElementException:
                    try:
                        sso_link = self.driver.find_element(By.XPATH, "//a[contains(@href, 'sso.uga.edu')]")
                    except NoSuchElementException:
                        pass
            
            if sso_link:
                print("Found UGA SSO link, clicking...")
                sso_link.click()
                time.sleep(5)
            else:
                print("Could not find UGA SSO link - may already be on login page")
            
            # Save screenshot
            self.driver.save_screenshot('sso_page.png')
            print(f"Current URL: {self.driver.current_url}")
            print(f"Page title: {self.driver.title}")
            
            # Now we should be on UGA's CAS login page
            print("Looking for UGA login fields...")
            
            # Try to find username field (UGA CAS uses 'username')
            username_field = None
            selectors = [
                (By.ID, "username"),
                (By.NAME, "username"),
                (By.ID, "userNameInput"),
                (By.NAME, "j_username"),
                (By.CSS_SELECTOR, "input[type='text']"),
                (By.CSS_SELECTOR, "input[name*='user']")
            ]
            
            for by, selector in selectors:
                try:
                    username_field = self.driver.find_element(by, selector)
                    print(f"Found username field: {by}={selector}")
                    break
                except NoSuchElementException:
                    continue
            
            if not username_field:
                print("ERROR: Could not find username field on UGA SSO page")
                self.driver.save_screenshot('no_username_field.png')
                return False
            
            # Find password field
            password_field = None
            password_selectors = [
                (By.ID, "password"),
                (By.NAME, "password"),
                (By.ID, "passwordInput"),
                (By.NAME, "j_password"),
                (By.CSS_SELECTOR, "input[type='password']")
            ]
            
            for by, selector in password_selectors:
                try:
                    password_field = self.driver.find_element(by, selector)
                    print(f"Found password field: {by}={selector}")
                    break
                except NoSuchElementException:
                    continue
            
            if not password_field:
                print("ERROR: Could not find password field")
                self.driver.save_screenshot('no_password_field.png')
                return False
            
            # Enter UGA credentials
            print("Entering credentials...")
            username_field.clear()
            username_field.send_keys(USERNAME)
            time.sleep(1)
            
            password_field.clear()
            password_field.send_keys(PASSWORD)
            time.sleep(1)
            
            # Find and click submit button
            login_button = None
            button_selectors = [
                (By.NAME, "submit"),
                (By.NAME, "submitButton"),
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.CSS_SELECTOR, "input[type='submit']"),
                (By.CSS_SELECTOR, "button[name='submit']"),
                (By.XPATH, "//button[contains(text(), 'LOG') or contains(text(), 'Log') or contains(text(), 'Sign')]"),
                (By.XPATH, "//input[@value='LOGIN' or @value='Login' or @value='Sign in']")
            ]
            
            for by, selector in button_selectors:
                try:
                    login_button = self.driver.find_element(by, selector)
                    print(f"Found login button: {by}={selector}")
                    break
                except NoSuchElementException:
                    continue
            
            if not login_button:
                print("ERROR: Could not find login button")
                self.driver.save_screenshot('no_login_button.png')
                return False
            
            print("Submitting login...")
            login_button.click()
            time.sleep(10)
            
            # Check if we're back on Handshake
            self.driver.save_screenshot('after_login.png')
            print(f"After login URL: {self.driver.current_url}")
            print(f"After login title: {self.driver.title}")
            
            # Check for successful login
            if 'handshake' in self.driver.current_url.lower() and 'login' not in self.driver.current_url.lower():
                print("✓ Login successful!")
                return True
            elif 'duo' in self.driver.current_url.lower() or 'mfa' in self.driver.current_url.lower():
                print("⚠ Two-factor authentication required - cannot automate")
                print("URL:", self.driver.current_url)
                return False
            else:
                print("⚠ Login status unclear - check screenshots")
                print("URL:", self.driver.current_url)
                return False
            
        except TimeoutException:
            print("ERROR: Login timeout")
            self.driver.save_screenshot('timeout_error.png')
            return False
        except Exception as e:
            print(f"ERROR: Login failed - {e}")
            self.driver.save_screenshot('login_error.png')
            import traceback
            traceback.print_exc()
            return False
    
    def navigate_to_jobs(self):
        """Navigate to Jobs section by clicking 'Jobs' in left column"""
        print("\nNavigating to Jobs section...")
        
        try:
            # Look for "Jobs" link in left navigation
            jobs_link = None
            
            # Try different ways to find the Jobs link
            selectors = [
                (By.LINK_TEXT, "Jobs"),
                (By.PARTIAL_LINK_TEXT, "Jobs"),
                (By.XPATH, "//a[contains(text(), 'Jobs')]"),
                (By.XPATH, "//nav//a[contains(text(), 'Jobs')]"),
                (By.CSS_SELECTOR, "a[href*='jobs']"),
                (By.CSS_SELECTOR, "nav a[href*='jobs']")
            ]
            
            for by, selector in selectors:
                try:
                    jobs_link = self.driver.find_element(by, selector)
                    print(f"  Found 'Jobs' link: {by}={selector}")
                    break
                except NoSuchElementException:
                    continue
            
            if not jobs_link:
                print("  ERROR: Could not find 'Jobs' link in navigation")
                self.driver.save_screenshot('no_jobs_link.png')
                return False
            
            # Click the Jobs link
            jobs_link.click()
            print("  Clicked 'Jobs' link")
            time.sleep(3)
            
            # Handle popup - look for OK button
            print("  Looking for popup to dismiss...")
            try:
                # Try to find and click OK/Close button in popup
                ok_button = None
                popup_selectors = [
                    (By.XPATH, "//button[contains(text(), 'OK')]"),
                    (By.XPATH, "//button[contains(text(), 'Ok')]"),
                    (By.XPATH, "//button[contains(text(), 'Close')]"),
                    (By.XPATH, "//button[contains(text(), 'Continue')]"),
                    (By.CSS_SELECTOR, "button[data-hook='dismiss']"),
                    (By.CSS_SELECTOR, "button.close"),
                    (By.CSS_SELECTOR, "button[aria-label='Close']"),
                    (By.CSS_SELECTOR, "[role='dialog'] button"),
                    (By.XPATH, "//div[contains(@class, 'modal')]//button"),
                    (By.XPATH, "//div[contains(@class, 'popup')]//button")
                ]
                
                for by, selector in popup_selectors:
                    try:
                        ok_button = self.driver.find_element(by, selector)
                        print(f"  Found popup button: {by}={selector}")
                        break
                    except NoSuchElementException:
                        continue
                
                if ok_button:
                    ok_button.click()
                    print("  Clicked OK to dismiss popup")
                    time.sleep(2)
                else:
                    print("  No popup found or already dismissed")
                    
            except Exception as e:
                print(f"  Note: Could not dismiss popup (may not exist): {e}")
            
            self.driver.save_screenshot('jobs_page_after_popup.png')
            print(f"  Current URL: {self.driver.current_url}")
            return True
            
        except Exception as e:
            print(f"  ERROR navigating to Jobs: {e}")
            self.driver.save_screenshot('nav_error.png')
            return False
    
    def search_jobs(self, keyword, location="Georgia"):
        """Search for jobs with a specific keyword"""
        print(f"\nSearching for: {keyword}")
        
        try:
            # Find the search input field - "Describe a job you want"
            search_input = None
            
            # Try different selectors for the search field
            selectors = [
                (By.CSS_SELECTOR, "input[placeholder*='Describe a job' i]"),
                (By.CSS_SELECTOR, "input[placeholder*='job you want' i]"),
                (By.XPATH, "//input[@placeholder='Describe a job you want']"),
                (By.CSS_SELECTOR, "input[placeholder*='Search' i]"),
                (By.CSS_SELECTOR, "input[type='search']"),
                (By.CSS_SELECTOR, "input[name*='search' i]"),
                (By.CSS_SELECTOR, "input[aria-label*='search' i]"),
                (By.CSS_SELECTOR, "input[type='text']")
            ]
            
            for by, selector in selectors:
                try:
                    search_input = self.driver.find_element(by, selector)
                    print(f"  Found search input: {by}={selector}")
                    break
                except NoSuchElementException:
                    continue
            
            if not search_input:
                print("  ERROR: Could not find search input field")
                self.driver.save_screenshot('no_search_field.png')
                
                # Show what inputs are available for debugging
                inputs = self.driver.find_elements(By.TAG_NAME, 'input')
                print(f"  Found {len(inputs)} input fields on page")
                for i, inp in enumerate(inputs[:5], 1):
                    print(f"    {i}. type={inp.get_attribute('type')}, placeholder={inp.get_attribute('placeholder')}")
                return
            
            # Try to interact with the search field using JavaScript
            # This often works when Selenium can't interact directly
            print(f"  Attempting to enter search keyword via JavaScript...")
            
            try:
                # Set the value using JavaScript
                self.driver.execute_script("arguments[0].value = arguments[1];", search_input, keyword)
                time.sleep(1)
                
                # Trigger input/change events so the page knows the field changed
                self.driver.execute_script("""
                    var element = arguments[0];
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                """, search_input)
                
                print(f"  Set search value to: {keyword}")
                time.sleep(2)
                
                # Try to submit by pressing Enter via JavaScript
                self.driver.execute_script("""
                    var element = arguments[0];
                    var event = new KeyboardEvent('keydown', {
                        key: 'Enter',
                        code: 'Enter',
                        keyCode: 13,
                        which: 13,
                        bubbles: true
                    });
                    element.dispatchEvent(event);
                """, search_input)
                
                print(f"  Triggered Enter key")
                print(f"  Waiting for results to load...")
                time.sleep(8)  # Give more time for results to load
                
            except Exception as js_error:
                print(f"  JavaScript method failed: {js_error}")
                # Try regular Selenium as fallback
                try:
                    search_input.click()
                    time.sleep(1)
                    search_input.send_keys(keyword)
                    search_input.send_keys(Keys.RETURN)
                    print(f"  Used Selenium method")
                    time.sleep(8)
                except Exception as e:
                    print(f"  Both methods failed: {e}")
                    return
            
            # Save screenshot of results
            self.driver.save_screenshot(f'search_results_{keyword.replace(" ", "_")}.png')
            print(f"  Results page URL: {self.driver.current_url}")
            
            # Extract job listings
            jobs_found = self.extract_jobs(keyword)
            print(f"  ✓ Found {jobs_found} jobs for '{keyword}'")
            
        except Exception as e:
            print(f"  ERROR searching for '{keyword}': {e}")
            self.driver.save_screenshot(f'search_error_{keyword.replace(" ", "_")}.png')
            import traceback
            traceback.print_exc()
    
    def extract_jobs(self, keyword):
        """Extract job details from the current search results page"""
        job_count = 0
        
        try:
            # Find job cards/listings - try multiple Handshake selectors
            job_elements = []
            
            selectors_to_try = [
                "[data-hook='search-result']",
                "[data-hook='posting-card']",
                ".posting-card",
                ".job-card",
                "article[data-hook]",
                "div[data-hook*='job']",
                "div[data-hook*='posting']",
                "[role='article']",
                ".styles_posting",
                "a[href*='/jobs/']",
                "a[href*='/postings/']"
            ]
            
            for selector in selectors_to_try:
                job_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if job_elements:
                    print(f"Found {len(job_elements)} job elements with selector: {selector}")
                    break
            
            if not job_elements:
                print(f"No job elements found. Trying to debug...")
                # Debug: show what's on the page
                page_text = self.driver.find_element(By.TAG_NAME, 'body').text
                if 'no results' in page_text.lower() or 'no jobs' in page_text.lower():
                    print(f"  Page shows 'no results' for keyword: {keyword}")
                else:
                    print(f"  Page has content but no recognizable job cards")
                    # Save page source for debugging
                    with open(f'page_source_{keyword.replace(" ", "_")}.html', 'w', encoding='utf-8') as f:
                        f.write(self.driver.page_source)
                    print(f"  Saved page source to page_source_{keyword.replace(' ', '_')}.html")
                return 0
            
            for idx, job_elem in enumerate(job_elements[:25], 1):  # Limit to first 25 results
                try:
                    # Try to get all text from the job element for debugging
                    job_text = job_elem.text.strip()
                    if not job_text or len(job_text) < 10:
                        continue  # Skip empty or very short elements
                    
                    # Extract job title - try multiple selectors
                    title = None
                    title_selectors = [
                        "h3", "h4", ".job-title", "[data-hook='title']",
                        "a[data-hook]", "div[data-hook*='title']"
                    ]
                    
                    for sel in title_selectors:
                        try:
                            title_elem = job_elem.find_element(By.CSS_SELECTOR, sel)
                            title = title_elem.text.strip()
                            if title and len(title) > 5:
                                break
                        except NoSuchElementException:
                            continue
                    
                    if not title:
                        # Try getting first line of text as title
                        lines = job_text.split('\n')
                        title = lines[0] if lines else None
                    
                    if not title or len(title) < 5:
                        continue  # Skip if no valid title found
                    
                    # Get employer
                    employer = "Not specified"
                    employer_selectors = [
                        ".employer-name", "[data-hook='employer-name']",
                        "[data-hook*='company']", "span[data-hook]"
                    ]
                    
                    for sel in employer_selectors:
                        try:
                            employer_elem = job_elem.find_element(By.CSS_SELECTOR, sel)
                            emp_text = employer_elem.text.strip()
                            if emp_text and len(emp_text) > 2:
                                employer = emp_text
                                break
                        except NoSuchElementException:
                            continue
                    
                    # Get location
                    location = "Georgia"
                    location_selectors = [
                        ".location", "[data-hook='location']",
                        "[data-hook*='location']", "span[data-hook*='location']"
                    ]
                    
                    for sel in location_selectors:
                        try:
                            location_elem = job_elem.find_element(By.CSS_SELECTOR, sel)
                            loc_text = location_elem.text.strip()
                            if loc_text and len(loc_text) > 2:
                                location = loc_text
                                break
                        except NoSuchElementException:
                            continue
                    
                    # Get job URL
                    job_url = self.driver.current_url
                    try:
                        link_elem = job_elem.find_element(By.CSS_SELECTOR, "a[href*='/jobs/'], a[href*='/postings/']")
                        job_url = link_elem.get_attribute('href')
                    except NoSuchElementException:
                        # Try to find any link within the element
                        try:
                            link_elem = job_elem.find_element(By.TAG_NAME, "a")
                            href = link_elem.get_attribute('href')
                            if href and ('job' in href.lower() or 'posting' in href.lower()):
                                job_url = href
                        except:
                            pass
                    
                    # Create job object
                    job = {
                        'title': title,
                        'employer': employer,
                        'location': location,
                        'url': job_url,
                        'source': 'UGA Handshake',
                        'keyword': keyword,
                        'scraped_at': datetime.now().isoformat()
                    }
                    
                    # Check for duplicates
                    if not any(j['title'] == title and j['employer'] == employer for j in self.jobs):
                        self.jobs.append(job)
                        job_count += 1
                        print(f"  ✓ {title} - {employer}")
                
                except Exception as e:
                    # Only show first few errors to avoid spam
                    if idx <= 3:
                        print(f"  Error extracting job #{idx}: {e}")
                    continue
        
        except Exception as e:
            print(f"Error finding job elements: {e}")
        
        return job_count
    
    def categorize_jobs(self):
        """Categorize jobs based on keywords"""
        for job in self.jobs:
            title_lower = job['title'].lower()
            
            if any(word in title_lower for word in ['forensic', 'crime scene', 'lab', 'technician']):
                job['category'] = 'forensics'
                job['icon'] = '🔬'
            elif any(word in title_lower for word in ['court', 'clerk', 'legal', 'paralegal', 'assistant']):
                job['category'] = 'court'
                job['icon'] = '⚖️'
            elif any(word in title_lower for word in ['victim', 'advocate', 'probation', 'government', 'county', 'city']):
                job['category'] = 'govt'
                job['icon'] = '🏛️'
            else:
                job['category'] = 'court'
                job['icon'] = '⚖️'
    
    def save_jobs(self, filename='handshake_jobs.json'):
        """Save jobs to JSON file"""
        self.categorize_jobs()
        
        output = {
            'scraped_at': datetime.now().isoformat(),
            'total_jobs': len(self.jobs),
            'jobs': self.jobs
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Saved {len(self.jobs)} jobs to {filename}")
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()

def main():
    """Main scraper execution"""
    print("=" * 60)
    print("UGA Handshake Job Scraper for Isabella")
    print("=" * 60)
    
    if not all([HANDSHAKE_URL, USERNAME, PASSWORD]):
        print("ERROR: Missing credentials in .env file")
        return
    
    scraper = HandshakeScraper(headless=False)  # Set to True for production
    
    try:
        # Login
        if not scraper.login():
            print("Login failed, exiting...")
            return
        
        # Navigate to Jobs section
        if not scraper.navigate_to_jobs():
            print("Could not navigate to Jobs section, exiting...")
            return
        
        # Search for each keyword
        for keyword in SEARCH_KEYWORDS:
            scraper.search_jobs(keyword)
            time.sleep(3)  # Wait between searches
        
        # Save results
        scraper.save_jobs()
        
        print("\n" + "=" * 60)
        print(f"Scraping complete! Found {len(scraper.jobs)} unique jobs")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
    finally:
        scraper.close()

if __name__ == '__main__':
    main()
