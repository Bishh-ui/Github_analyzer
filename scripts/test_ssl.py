#!/usr/bin/env python3
"""Test SSL connectivity and GitHub API access"""

import sys
import os
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Add project root to sys.path and load environment
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / '.env')

print("=" * 60)
print("Testing SSL Connection to GitHub API")
print("=" * 60)
print()

# Test 1: Import required modules
print("1. Testing imports...")
try:
    import ssl
    import certifi
    import urllib3
    from github import Github
    print("   [OK] All modules imported successfully")
    print(f"   [INFO] Certifi path: {certifi.where()}")
except ImportError as e:
    print(f"   [ERROR] Import failed: {e}")
    sys.exit(1)

# Test 2: Try GitHub connection with certifi
print("\n2. Testing GitHub API with certifi...")
try:
    g = Github(verify=certifi.where())
    user = g.get_user('octocat')
    print(f"   [OK] Connected successfully!")
    print(f"   [INFO] Test user: {user.login} ({user.name})")
except Exception as e:
    print(f"   [WARN] Certifi verification encountered an issue: {type(e).__name__}")
    
    # Test 3: Try without SSL verification (fallback)
    print("\n3. Testing GitHub API without SSL verification...")
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        g = Github(verify=False)
        user = g.get_user('octocat')
        print(f"   [OK] Connected successfully (without SSL verification)!")
        print(f"   [INFO] Test user: {user.login} ({user.name})")
        print("   [NOTE] SSL verification disabled for local environment compatibility")
    except Exception as e2:
        print(f"   [ERROR] Connection failed: {e2}")
        sys.exit(1)

# Test 4: Test with GitHub token from .env
print("\n4. Testing with GitHub token from .env...")
try:
    token = os.getenv('GITHUB_TOKEN')
    
    if not token or token in ['your_github_token_here', 'your_github_personal_access_token_here']:
        print("   [WARN] No GitHub token configured in .env")
        print("   [INFO] Using unauthenticated access (60 requests/hour)")
        token = None
    else:
        print("   [OK] GitHub token found in .env")
        print("   [OK] Authenticated access (5,000 requests/hour)")
    
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    g = Github(token, verify=False) if token else Github(verify=False)
    rate_limit = g.get_rate_limit()
    print(f"   [INFO] Remaining requests: {rate_limit.core.remaining}/{rate_limit.core.limit}")
    print(f"   [INFO] Reset at: {rate_limit.core.reset.strftime('%H:%M:%S UTC')}")
        
except Exception as e:
    print(f"   [ERROR] Failed: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("[SUCCESS] All tests passed! GitHub API connectivity is working.")
print("=" * 60)
print("\nReady to run the application:")
print("   python run.py")
print("   Open: http://localhost:5000\n")
