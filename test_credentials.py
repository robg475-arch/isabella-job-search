#!/usr/bin/env python3
"""
Test that credentials are loaded correctly from .env
"""

from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv('HANDSHAKE_URL')
username = os.getenv('HANDSHAKE_USERNAME')
password = os.getenv('HANDSHAKE_PASSWORD')

print('Testing .env file...')
print(f'URL: {url}')
print(f'Username: {username}')
print(f'Password: {"*" * len(password) if password else "NOT SET"}')
print()

if all([url, username, password]):
    print('✓ All credentials loaded successfully!')
    print('\nReady to run:')
    print('  python3 handshake_scraper.py')
else:
    print('✗ Missing credentials in .env file')
