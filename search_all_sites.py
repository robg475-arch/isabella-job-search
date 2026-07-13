#!/usr/bin/env python3
"""
Search multiple job sites for criminal justice and entry-level positions in Georgia
"""

import time
import json
from datetime import datetime
from urllib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Criminal justice search terms (for local government portals)
CJ_KEYWORDS = [
    'criminal justice',
    'court clerk',
    'probation officer',
    'forensic',
    'crime scene'
]

# Entry-level/new graduate search terms (for general job sites)
ENTRY_LEVEL_KEYWORDS = [
    'entry level',
    'new graduate',
    'recent graduate',
    'junior',
    'associate',
    'coordinator',
    'assistant',
]

# Geographic search areas
SEARCH_LOCATIONS = [
    'Atlanta, GA',
    'Marietta, GA',
    'Alpharetta, GA',
    'Kennesaw, GA',
    'Woodstock, GA',
]

# Counties and cities to search
LOCATIONS = [
    # Counties
    'Cherokee County',
    'Cobb County',
    'Forsyth County',
    'Gwinnett County',
    'Fulton County',
    'Bartow County',
    'Pickens County',
    'Dawson County',
    'Paulding County',
    'Dekalb County',
    'Gordon County',
    # Cities
    'City of Woodstock',
    'City of Canton',
    'City of Marietta',
    'City of Cartersville',
    'City of Kennesaw',
    'City of Acworth',
    'City of Smyrna',
    'City of Roswell',
    'City of Alpharetta',
    'City of Holly Springs',
    'City of Powder Springs',
    'City of Sandy Springs',
    'City of Dunwoody',
    'City of Milton',
    'City of Mableton',
    'City of Austell',
    'City of Johns Creek',
]

class JobSearcher:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        self.new_jobs = []
    
    def search_local_portal(self, location):
        """Search local government job portals"""
        print(f"\n🔍 Searching {location}...")
        
        # Map locations to their job portal URLs
        portal_urls = {
            # Counties
            'Cherokee County': [
                'https://jobs.cherokeega.org/all-jobs/',
                'https://selfservice.cherokeega.com/ess/employmentopportunities/default.aspx',
            ],
            'Cobb County': 'https://www.governmentjobs.com/careers/cobbcounty',
            'Forsyth County': [
                'https://www.governmentjobs.com/careers/forsyth',
                'https://www.forsythsheriffcareers.com/current-jobopenings',
            ],
            'Gwinnett County': 'https://www.governmentjobs.com/careers/gwinnett',
            'Fulton County': 'https://www.governmentjobs.com/careers/fulton',
            'Bartow County': 'https://www.bartowcountyga.gov/departments/human_resources/job_listings.php',
            'Pickens County': [
                'https://pickenscountyga.tylerportico.com/tess/citizen/jobs/job-list/jobs',
                'https://pickensgasheriff.applicantpro.com/jobs/',
            ],
            'Dawson County': 'https://www.dawsoncountyga.gov/Jobs.aspx',
            'Paulding County': 'https://www.paulding.gov/jobs.aspx',
            'Dekalb County': 'https://ertd.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001/jobs',
            'Gordon County': 'https://workforcenow.adp.com/mascsr/default/mdf/recruitment/recruitment.html?cid=66ddf5e5-04e8-4d83-b99d-06166b4c87aa&ccId=19000101_000001&lang=en_US&selectedMenuKey=CurrentOpenings',
            # Cities
            'City of Woodstock': 'https://secure6.saashr.com/ta/6195271.careers?CareersSearch=&lang=en-US',
            'City of Canton': 'https://www.cantonga.gov/government/careers',
            'City of Marietta': 'https://cityofmariettaga.applytojob.com/apply',
            'City of Cartersville': 'https://www.cartersvillega.gov/Jobs.aspx',
            'City of Kennesaw': 'https://kennesaw-ga.zohorecruit.com/jobs/Careers',
            'City of Acworth': 'https://acworth.applicantstack.com/x/openings',
            'City of Smyrna': 'https://www.smyrnaga.gov/departments/departments/human-resources/employment',
            'City of Roswell': 'https://workforcenow.adp.com/mascsr/default/mdf/recruitment/recruitment.html?cid=8312d029-992c-42a9-9f74-c83d7699e08a&ccId=19000101_000001&lang=en_US&selectedMenuKey=CurrentOpenings',
            'City of Alpharetta': 'https://www.governmentjobs.com/careers/alpharetta',
            'City of Holly Springs': 'https://hollyspringsga.applicantpro.com/jobs/',
            'City of Powder Springs': 'https://cityofpowderspringsga.tylerportico.com/tess/citizen/jobs/job-list/jobs',
            'City of Sandy Springs': 'https://workforcenow.adp.com/mascsr/default/mdf/recruitment/recruitment.html?cid=ab980e35-8aa1-4f79-ae5a-4622356af318&ccId=19000101_000001&selectedMenuKey=CurrentOpenings',
            'City of Dunwoody': 'https://dunwoodyga.applicantstack.com/x/openings',
            'City of Milton': 'https://www.governmentjobs.com/careers/miltonga',
            'City of Mableton': 'https://www.paycomonline.net/v4/ats/web.php/portal/E54FCB8F055F8032413DEFB37467C99F/career-page',
            'City of Austell': 'https://www.austellga.gov/AvailablePositions.aspx',
            'City of Johns Creek': 'https://johnscreekga.gov/departments/human-resources/current-openings/',
        }
        
        urls = portal_urls.get(location)
        if not urls:
            return
        
        # Handle single URL or list of URLs
        if isinstance(urls, str):
            urls = [urls]
        
        for url in urls:
            try:
                self.driver.get(url)
                time.sleep(3)
                
                # Look for job listings
                page_text = self.driver.page_source.lower()
                
                # Check for relevant keywords
                relevant_keywords = ['court', 'clerk', 'probation', 'criminal', 'justice', 'forensic', 'crime scene']
                
                if any(keyword in page_text for keyword in relevant_keywords):
                    print(f"  ✓ {location} has potential jobs")
                    
                    # Try to extract job links
                    job_links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="/jobs/"], a[href*="job"], a[href*="career"], a[href*="position"]')
                    
                    for link in job_links[:10]:  # Check first 10 links
                        try:
                            job_title = link.text.strip()
                            job_url = link.get_attribute('href')
                            
                            if job_title and any(kw in job_title.lower() for kw in relevant_keywords):
                                print(f"    • {job_title}")
                                self.new_jobs.append({
                                    'title': job_title,
                                    'employer': location,
                                    'location': f'{location}, GA',
                                    'url': job_url,
                                    'source': 'Local Portal',
                                    'found_date': datetime.now().strftime('%Y-%m-%d')
                                })
                        except:
                            continue
                
            except Exception as e:
                print(f"  ✗ Error searching {location}: {e}")
    
    def search_indeed(self, keyword, location='Atlanta, GA'):
        """Search Indeed for entry-level jobs"""
        print(f"\n🔍 Searching Indeed - '{keyword}' in {location}...")
        
        try:
            # Indeed URL with entry-level filter (explvl=entry_level)
            search_query = quote_plus(keyword)
            location_query = quote_plus(location)
            search_url = f"https://www.indeed.com/jobs?q={search_query}&l={location_query}&sc=0kf%3Aexplvl%28ENTRY_LEVEL%29%3B&radius=35"
            
            self.driver.get(search_url)
            time.sleep(4)
            
            # Find job cards
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, 'div.job_seen_beacon, div.jobsearch-ResultsList > div')
            
            jobs_found = 0
            for card in job_cards[:10]:
                try:
                    # Try to find job title
                    title_elem = card.find_element(By.CSS_SELECTOR, 'h2.jobTitle a, a[data-jk]')
                    job_title = title_elem.text.strip()
                    job_url = title_elem.get_attribute('href')
                    
                    # Try to find company name
                    try:
                        company_elem = card.find_element(By.CSS_SELECTOR, 'span[data-testid="company-name"], span.companyName')
                        company = company_elem.text.strip()
                    except:
                        company = 'Unknown'
                    
                    # Try to find location
                    try:
                        loc_elem = card.find_element(By.CSS_SELECTOR, 'div[data-testid="text-location"], div.companyLocation')
                        job_location = loc_elem.text.strip()
                    except:
                        job_location = location
                    
                    if job_title:
                        print(f"    • {job_title} - {company}")
                        self.new_jobs.append({
                            'title': job_title,
                            'employer': company,
                            'location': job_location,
                            'url': job_url if job_url else search_url,
                            'source': 'Indeed',
                            'keyword': keyword,
                            'found_date': datetime.now().strftime('%Y-%m-%d')
                        })
                        jobs_found += 1
                except:
                    continue
            
            if jobs_found > 0:
                print(f"  ✓ Found {jobs_found} jobs")
            else:
                print(f"  ✗ No jobs found for '{keyword}'")
                
        except Exception as e:
            print(f"  ✗ Error searching Indeed: {e}")
    
    def search_linkedin(self, keyword, location='Atlanta, GA'):
        """Search LinkedIn for entry-level jobs"""
        print(f"\n🔍 Searching LinkedIn - '{keyword}' in {location}...")
        
        try:
            # LinkedIn URL with entry-level filter (f_E=2 is entry level)
            search_query = quote_plus(keyword)
            location_query = quote_plus(location)
            # f_E=2 = Entry level, f_TPR=r604800 = past week
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={search_query}&location={location_query}&f_E=2&f_TPR=r604800"
            
            self.driver.get(search_url)
            time.sleep(4)
            
            # Find job cards (LinkedIn public job search)
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, 'div.base-card, li.jobs-search-results__list-item')
            
            jobs_found = 0
            for card in job_cards[:10]:
                try:
                    # Try to find job title
                    title_elem = card.find_element(By.CSS_SELECTOR, 'h3.base-search-card__title, a.base-card__full-link')
                    job_title = title_elem.text.strip()
                    
                    # Try to get URL
                    try:
                        link_elem = card.find_element(By.CSS_SELECTOR, 'a.base-card__full-link')
                        job_url = link_elem.get_attribute('href')
                    except:
                        job_url = search_url
                    
                    # Try to find company name
                    try:
                        company_elem = card.find_element(By.CSS_SELECTOR, 'h4.base-search-card__subtitle, a.hidden-nested-link')
                        company = company_elem.text.strip()
                    except:
                        company = 'Unknown'
                    
                    # Try to find location
                    try:
                        loc_elem = card.find_element(By.CSS_SELECTOR, 'span.job-search-card__location')
                        job_location = loc_elem.text.strip()
                    except:
                        job_location = location
                    
                    if job_title:
                        print(f"    • {job_title} - {company}")
                        self.new_jobs.append({
                            'title': job_title,
                            'employer': company,
                            'location': job_location,
                            'url': job_url,
                            'source': 'LinkedIn',
                            'keyword': keyword,
                            'found_date': datetime.now().strftime('%Y-%m-%d')
                        })
                        jobs_found += 1
                except:
                    continue
            
            if jobs_found > 0:
                print(f"  ✓ Found {jobs_found} jobs")
            else:
                print(f"  ✗ No jobs found for '{keyword}'")
                
        except Exception as e:
            print(f"  ✗ Error searching LinkedIn: {e}")
    
    def search_ziprecruiter(self, keyword, location='Atlanta, GA'):
        """Search ZipRecruiter for entry-level jobs"""
        print(f"\n🔍 Searching ZipRecruiter - '{keyword}' in {location}...")
        
        try:
            search_query = quote_plus(keyword)
            location_query = quote_plus(location)
            # refine_by_employment=employment_type%3Apart_time adds filters
            search_url = f"https://www.ziprecruiter.com/jobs-search?search={search_query}&location={location_query}&radius=35&refine_by_salary=&refine_by_employment=&days=7"
            
            self.driver.get(search_url)
            time.sleep(4)
            
            # Find job cards
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, 'article.job_result, div.job_content')
            
            jobs_found = 0
            for card in job_cards[:10]:
                try:
                    # Try to find job title
                    title_elem = card.find_element(By.CSS_SELECTOR, 'h2.job_title a, a.job_link')
                    job_title = title_elem.text.strip()
                    job_url = title_elem.get_attribute('href')
                    
                    # Try to find company name
                    try:
                        company_elem = card.find_element(By.CSS_SELECTOR, 'a.company_name, p.company_name')
                        company = company_elem.text.strip()
                    except:
                        company = 'Unknown'
                    
                    # Try to find location
                    try:
                        loc_elem = card.find_element(By.CSS_SELECTOR, 'p.job_location, span.job_location')
                        job_location = loc_elem.text.strip()
                    except:
                        job_location = location
                    
                    if job_title:
                        print(f"    • {job_title} - {company}")
                        self.new_jobs.append({
                            'title': job_title,
                            'employer': company,
                            'location': job_location,
                            'url': job_url if job_url else search_url,
                            'source': 'ZipRecruiter',
                            'keyword': keyword,
                            'found_date': datetime.now().strftime('%Y-%m-%d')
                        })
                        jobs_found += 1
                except:
                    continue
            
            if jobs_found > 0:
                print(f"  ✓ Found {jobs_found} jobs")
            else:
                print(f"  ✗ No jobs found for '{keyword}'")
                
        except Exception as e:
            print(f"  ✗ Error searching ZipRecruiter: {e}")
    
    def search_team_georgia(self, keyword):
        """Search Team Georgia Careers"""
        print(f"\n🔍 Searching Team Georgia - '{keyword}'...")
        
        try:
            # Search URL format
            search_url = f"https://ga.referrals.selectminds.com/jobs/search/45859777?q={keyword.replace(' ', '+')}"
            self.driver.get(search_url)
            time.sleep(4)
            
            page_text = self.driver.page_source
            
            # Check if there are results
            if 'results' in page_text.lower() or 'job' in page_text.lower():
                print(f"  ✓ Found results for '{keyword}'")
                
                # Try to find job titles (this is simplified - would need better selectors)
                job_elements = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="/jobs/"]')
                
                for job_elem in job_elements[:5]:
                    try:
                        job_title = job_elem.text.strip()
                        job_url = job_elem.get_attribute('href')
                        
                        if job_title and len(job_title) > 5:
                            print(f"    • {job_title}")
                            self.new_jobs.append({
                                'title': job_title,
                                'employer': 'State of Georgia',
                                'location': 'Georgia',
                                'url': job_url,
                                'source': 'Team Georgia',
                                'keyword': keyword,
                                'found_date': datetime.now().strftime('%Y-%m-%d')
                            })
                    except:
                        continue
            else:
                print(f"  ✗ No results for '{keyword}'")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    def close(self):
        self.driver.quit()
    
    def save_results(self):
        """Save new jobs to file"""
        if self.new_jobs:
            with open('new_jobs_found.json', 'w') as f:
                json.dump(self.new_jobs, f, indent=2)
            print(f"\n✓ Saved {len(self.new_jobs)} new jobs to new_jobs_found.json")
        else:
            print("\n✗ No new jobs found")

def main():
    print("="*60)
    print("Multi-Site Job Search")
    print("Criminal Justice + Entry-Level Positions in Georgia")
    print("="*60)
    
    searcher = JobSearcher()
    
    try:
        # ===== CRIMINAL JUSTICE SEARCHES =====
        print("\n" + "-"*40)
        print("CRIMINAL JUSTICE JOB SEARCH")
        print("-"*40)
        
        # Search local government portals (counties and cities)
        for location in LOCATIONS:
            searcher.search_local_portal(location)
            time.sleep(2)
        
        # Search Team Georgia for criminal justice keywords
        for keyword in CJ_KEYWORDS:
            searcher.search_team_georgia(keyword)
            time.sleep(2)
        
        # ===== ENTRY-LEVEL / NEW GRADUATE SEARCHES =====
        print("\n" + "-"*40)
        print("ENTRY-LEVEL / NEW GRADUATE JOB SEARCH")
        print("-"*40)
        
        # Search general job sites for entry-level positions
        entry_level_searches = [
            'entry level',
            'new graduate',
            'recent college graduate',
            'junior coordinator',
            'administrative assistant',
            'program coordinator',
            'office assistant',
        ]
        
        for keyword in entry_level_searches:
            # Search Indeed
            searcher.search_indeed(keyword, 'Atlanta, GA')
            time.sleep(3)
            
            # Search LinkedIn
            searcher.search_linkedin(keyword, 'Atlanta, GA')
            time.sleep(3)
            
            # Search ZipRecruiter
            searcher.search_ziprecruiter(keyword, 'Atlanta, GA')
            time.sleep(3)
        
    finally:
        searcher.save_results()
        searcher.close()
    
    print("\n" + "="*60)
    print("Search complete!")
    print("="*60)

if __name__ == '__main__':
    main()
