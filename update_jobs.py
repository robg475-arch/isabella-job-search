#!/usr/bin/env python3
"""
Update index.html with jobs from handshake_jobs.json
Merges Handshake jobs with existing hardcoded jobs
"""

import json
import re
from datetime import datetime

def load_handshake_jobs():
    """Load jobs from handshake_jobs.json"""
    try:
        with open('handshake_jobs.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('jobs', [])
    except FileNotFoundError:
        print("No handshake_jobs.json found. Run handshake_scraper.py first.")
        return []

def convert_to_js_format(jobs):
    """Convert Python jobs to JavaScript format"""
    js_jobs = []
    
    for job in jobs:
        # Map to expected format
        js_job = {
            'cat': job.get('category', 'court'),
            'icon': job.get('icon', '⚖️'),
            'catLabel': get_category_label(job.get('category', 'court')),
            'title': job['title'],
            'employer': job['employer'],
            'location': job['location'],
            'source': 'UGA Handshake',
            'url': job['url'],
            'hot': False,
            'note': 'From Handshake'
        }
        js_jobs.append(js_job)
    
    return js_jobs

def get_category_label(cat):
    """Get category label from category ID"""
    labels = {
        'forensics': 'Forensics & Crime Scene',
        'court': 'Court & Office',
        'govt': 'Gov & Victim Services'
    }
    return labels.get(cat, 'Court & Office')

def format_js_job(job):
    """Format a single job as JavaScript object"""
    return f"""  {{ cat: '{job['cat']}', icon: '{job['icon']}', catLabel: '{job['catLabel']}',
    title: '{escape_js(job['title'])}',
    employer: '{escape_js(job['employer'])}',
    location: '{escape_js(job['location'])}', source: '{job['source']}',
    url: '{job['url']}',
    hot: {str(job['hot']).lower()}, note: {f"'{job['note']}'" if job['note'] else 'null'} }}"""

def escape_js(text):
    """Escape text for JavaScript strings"""
    return text.replace("'", "\\'").replace('\n', ' ').replace('\r', '')

def update_html(handshake_jobs):
    """Update index.html with Handshake jobs"""
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Convert to JS format
    js_jobs = convert_to_js_format(handshake_jobs)
    
    # Find the JOBS array in the HTML
    jobs_pattern = r'const JOBS = \[(.*?)\];'
    match = re.search(jobs_pattern, html, re.DOTALL)
    
    if not match:
        print("ERROR: Could not find JOBS array in index.html")
        return False
    
    # Extract existing jobs
    existing_jobs_str = match.group(1)
    
    # Parse existing jobs (simple parsing)
    # For safety, we'll append Handshake jobs rather than replacing
    
    # Format new jobs
    new_jobs_str = ',\n'.join(format_js_job(job) for job in js_jobs)
    
    # Combine existing and new jobs
    combined_jobs = existing_jobs_str.rstrip().rstrip(',') + ',\n' + new_jobs_str
    
    # Replace in HTML
    new_html = html.replace(
        f'const JOBS = [{existing_jobs_str}];',
        f'const JOBS = [\n{combined_jobs}\n];'
    )
    
    # Update the "last updated" timestamp
    today = datetime.now().strftime('%B %d, %Y')
    new_html = re.sub(
        r'Updated Apr 28, 2026',
        f'Updated {today}',
        new_html
    )
    new_html = re.sub(
        r'Listings last updated April 28, 2026',
        f'Listings last updated {today}',
        new_html
    )
    
    # Update job count in badge
    total_jobs = len(js_jobs) + len(re.findall(r'\{ cat:', existing_jobs_str))
    new_html = re.sub(
        r'<span class="new-badge">\d+</span>',
        f'<span class="new-badge">{total_jobs}</span>',
        new_html
    )
    
    # Write updated HTML
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"✓ Updated index.html with {len(js_jobs)} Handshake jobs")
    print(f"✓ Total jobs now: {total_jobs}")
    return True

def main():
    print("=" * 60)
    print("Updating index.html with Handshake jobs")
    print("=" * 60)
    
    # Load Handshake jobs
    handshake_jobs = load_handshake_jobs()
    
    if not handshake_jobs:
        print("No Handshake jobs to add.")
        return
    
    print(f"Found {len(handshake_jobs)} jobs from Handshake")
    
    # Update HTML
    if update_html(handshake_jobs):
        print("\n✓ Successfully updated index.html!")
        print("Open index.html in a browser to see the updated listings.")
    else:
        print("\n✗ Failed to update index.html")

if __name__ == '__main__':
    main()
