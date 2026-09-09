import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# GitHub API Token
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Application Settings
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
MAX_WORKERS = int(os.getenv('MAX_WORKERS', '10'))

# Cache settings
CACHE_TYPE = os.getenv('CACHE_TYPE', 'simple')  # simple, redis, filesystem
CACHE_REDIS_URL = os.getenv('CACHE_REDIS_URL', 'redis://localhost:6379/0')
CACHE_TIMEOUT = int(os.getenv('CACHE_TIMEOUT', '3600'))  # 1 hour
MAX_CACHE_ITEMS = int(os.getenv('MAX_CACHE_ITEMS', '100'))

# Database settings
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///github_analytics.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Rate Limiting
RATELIMIT_STORAGE_URL = os.getenv('RATELIMIT_STORAGE_URL', 'memory://')
RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT', '100 per hour')

# Security
SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24).hex())
CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')

# Advanced Features
ENABLE_ANALYTICS_EXPORT = os.getenv('ENABLE_ANALYTICS_EXPORT', 'True').lower() == 'true'
ENABLE_COMPARISON_MODE = os.getenv('ENABLE_COMPARISON_MODE', 'True').lower() == 'true'
ENABLE_HISTORICAL_TRACKING = os.getenv('ENABLE_HISTORICAL_TRACKING', 'True').lower() == 'true'
MAX_COMPARISON_USERS = int(os.getenv('MAX_COMPARISON_USERS', '5'))

# Chart and Visualization Settings
DEFAULT_CHART_THEME = os.getenv('DEFAULT_CHART_THEME', 'dark')
ENABLE_ADVANCED_CHARTS = os.getenv('ENABLE_ADVANCED_CHARTS', 'True').lower() == 'true'
