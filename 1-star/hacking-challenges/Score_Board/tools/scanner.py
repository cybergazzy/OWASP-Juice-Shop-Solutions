import os
import re
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright

BANNER = r"""
=========================================================
  _______  __/ /_  ___  _________ _____ _________  __  __
 / ___/ / / / __ \/ _ \/ ___/ __ `/ __ `/_  /_  / / / / /
/ /__/ /_/ / /_/ /  __/ /  / /_/ / /_/ / / /_/ /_/ /_/ /
\___/\__, /_.___/\___/_/   \__, /\__,_/ /___/___/\__, /
    /____/                /____/                /____/
=========================================================
"""

def extract_endpoints(url):
    print(f"[*] Scanning targets at: {url}")
    endpoints = set()
    try:
        response = requests.get(url, timeout=10, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        script_srcs = [script.get('src') for script in soup.find_all('script') if script.get('src')]
        pattern = r'["\']((?:\/[a-zA-Z0-9_\-\.]+)+)["\']'
        inline_paths = re.findall(pattern, response.text)
        for path in inline_paths:
            endpoints.add(path)

        for src in script_srcs:
            js_url = urljoin(url, src)
            try:
                js_res = requests.get(js_url, timeout=5, verify=False)
                js_paths = re.findall(pattern, js_res.text)
                for path in js_paths:
                    endpoints.add(path)
            except Exception:
                continue
    except Exception as e:
        print(f"[-] Error connecting to target: {e}")

    return sorted(list(endpoints))

if __name__ == "__main__":
    print(BANNER)
    
    if len(sys.argv) < 2:
        print("Usage: python scanner.py <target_url>")
        print("Example: python scanner.py http://localhost:3000")
        sys.exit(1)
        
    target = sys.argv[1].rstrip('/')
    found_paths = extract_endpoints(target)
    
    print(f"\n[+] Found {len(found_paths)} potential paths/endpoints:")
    scoreboard_path = None
    
    for path in found_paths:
        print(f"  {path}")
        if "score-board" in path.lower() or "scoreboard" in path.lower():
            scoreboard_path = path

    print("\n" + "="*50)
