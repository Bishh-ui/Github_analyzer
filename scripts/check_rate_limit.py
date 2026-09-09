#!/usr/bin/env python3
"""Check GitHub API Rate Limit Status"""

import os
import sys
from pathlib import Path
from datetime import datetime
import urllib3
from github import Github
from dotenv import load_dotenv

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Suppress insecure request warnings for local development
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Resolve project root and load .env
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
load_dotenv(PROJECT_ROOT / '.env')

token = os.getenv('GITHUB_TOKEN')

print("=" * 70)
print("GitHub API Rate Limit Status")
print("=" * 70)

if token and token != 'your_github_token_here':
    masked_token = f"{token[:4]}...{token[-4:]}"
    print(f"[AUTH] Using configured GITHUB_TOKEN ({masked_token})")
    g = Github(token, verify=False)
else:
    print("[WARN] No GITHUB_TOKEN configured in .env; using anonymous access")
    g = Github(verify=False)

try:
    rate_limit = g.get_rate_limit()
    
    print("\n[INFO] Current Rate Limits:")
    print("-" * 70)
    
    core = rate_limit.core
    print(f"\nCore API:")
    print(f"   Limit:     {core.limit} requests/hour")
    print(f"   Used:      {core.limit - core.remaining} requests")
    print(f"   Remaining: {core.remaining} requests")
    print(f"   Reset at:  {core.reset.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    now = datetime.now(core.reset.tzinfo)
    time_until_reset = core.reset - now
    minutes = max(0, int(time_until_reset.total_seconds() / 60))
    
    if core.remaining == 0:
        print(f"\n[ALERT] RATE LIMIT EXCEEDED! Resets in {minutes} minutes.")
    elif core.remaining < 100:
        print(f"\n[WARN] Low remaining limit: {core.remaining} requests. Resets in {minutes} minutes.")
    else:
        print(f"\n[OK] Healthy: {core.remaining} / {core.limit} requests available.")
    
    print("=" * 70)

except Exception as e:
    print(f"\n[ERROR] Error checking rate limit: {e}")
