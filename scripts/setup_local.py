#!/usr/bin/env python3
"""
Local Setup Script for GitHub Analytics Pro
This script verifies dependencies, checks .env token configuration, and initializes the local database.
"""

import os
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Set up project root in sys.path and resolve paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

def print_banner():
    print("=" * 60)
    print("  GitHub Analytics Pro - Local Setup")
    print("=" * 60)
    print()

def check_env_file():
    """Check if .env file exists and has GitHub token"""
    env_path = PROJECT_ROOT / '.env'
    
    if not env_path.exists():
        print("[X] .env file not found!")
        print("    Creating .env file from template...")
        example_path = PROJECT_ROOT / '.env.example'
        if example_path.exists():
            import shutil
            shutil.copyfile(example_path, env_path)
            print("    [OK] Created .env from .env.example")
        return False
    
    print("[OK] .env file found")
    
    # Check if token is set
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if 'your_github_token_here' in content or 'your_github_personal_access_token_here' in content:
            print("[WARN] GitHub token not configured in .env file")
            print("       Get your token from: https://github.com/settings/tokens")
            return False
        else:
            print("[OK] GitHub token is configured")
            return True

def test_imports():
    """Test if all required packages are installed"""
    print("\nChecking dependencies...")
    
    required = [
        ('flask', 'Flask'),
        ('github', 'PyGithub'),
        ('dotenv', 'python-dotenv'),
        ('flask_caching', 'Flask-Caching'),
        ('flask_cors', 'Flask-CORS'),
        ('flask_limiter', 'Flask-Limiter'),
        ('sqlalchemy', 'SQLAlchemy'),
        ('flask_sqlalchemy', 'Flask-SQLAlchemy'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
    ]
    
    missing = []
    for module, package in required:
        try:
            __import__(module)
            print(f"   [OK] {package}")
        except ImportError:
            print(f"   [X] {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n[ERROR] Missing packages: {', '.join(missing)}")
        print("        Run: pip install -r requirements.txt")
        return False
    
    print("[OK] All dependencies installed")
    return True

def create_database():
    """Create database tables"""
    print("\nSetting up database...")
    try:
        from app import create_app
        from app.models.user_analytics import db
        
        app = create_app()
        with app.app_context():
            db.create_all()
        
        print("[OK] Database initialized")
        return True
    except Exception as e:
        print(f"[ERROR] Database setup failed: {str(e)}")
        return False

def main():
    print_banner()
    
    # Check environment file
    token_set = check_env_file()
    
    # Check dependencies
    deps_ok = test_imports()
    
    if not deps_ok:
        print("\n[WARN] Please install dependencies first:")
        print("       pip install -r requirements.txt")
        sys.exit(1)
    
    # Create database
    db_ok = create_database()
    
    # Final instructions
    print("\n" + "=" * 60)
    if token_set and db_ok:
        print("[SUCCESS] Setup complete! Ready to run the application.")
        print("\nTo start the server, run:")
        print("   python run.py")
        print("\nThen open your browser to:")
        print("   http://localhost:5000")
    else:
        print("[INFO] Setup incomplete:")
        if not token_set:
            print("   - Please configure your GITHUB_TOKEN in .env")
        print("\nAfter configuration, run: python run.py")
    
    print("=" * 60)

if __name__ == '__main__':
    main()
