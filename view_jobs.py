#!/usr/bin/env python3
"""
Quick viewer for scraped Handshake jobs
"""

import json
import os
from datetime import datetime

def view_jobs():
    """Display jobs from handshake_jobs.json"""
    
    if not os.path.exists('handshake_jobs.json'):
        print("No jobs file found. Run handshake_scraper.py first.")
        return
    
    with open('handshake_jobs.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    jobs = data.get('jobs', [])
    scraped_at = data.get('scraped_at', 'Unknown')
    
    print("=" * 70)
    print(f"Handshake Jobs - {len(jobs)} listings")
    print(f"Scraped: {scraped_at}")
    print("=" * 70)
    print()
    
    # Group by category
    categories = {}
    for job in jobs:
        cat = job.get('category', 'other')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(job)
    
    # Display by category
    cat_icons = {
        'forensics': '🔬',
        'court': '⚖️',
        'govt': '🏛️'
    }
    
    cat_names = {
        'forensics': 'Forensics & Crime Scene',
        'court': 'Court & Office',
        'govt': 'Government & Victim Services'
    }
    
    for cat_id in ['forensics', 'court', 'govt']:
        if cat_id in categories:
            cat_jobs = categories[cat_id]
            icon = cat_icons.get(cat_id, '📋')
            name = cat_names.get(cat_id, cat_id.title())
            
            print(f"{icon} {name} ({len(cat_jobs)} jobs)")
            print("-" * 70)
            
            for i, job in enumerate(cat_jobs, 1):
                print(f"{i}. {job['title']}")
                print(f"   {job['employer']} - {job['location']}")
                print(f"   {job['url']}")
                print()
            
            print()
    
    print("=" * 70)
    print(f"Total: {len(jobs)} jobs found")
    print("=" * 70)

if __name__ == '__main__':
    view_jobs()
