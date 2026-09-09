# 🚀 Upgrade Guide: From GHAnalyzer to GitHub Analytics Pro

This guide will help you upgrade from the basic GHAnalyzer to the advanced GitHub Analytics Pro version.

## What's New?

### 🎯 Major Features
- ✅ Advanced metrics (Impact, Consistency, Diversity scores)
- ✅ Historical data tracking with database storage
- ✅ User comparison (up to 5 users)
- ✅ Multiple export formats (JSON, CSV, Markdown)
- ✅ RESTful API with comprehensive endpoints
- ✅ Redis caching support
- ✅ Rate limiting
- ✅ Dark/Light theme toggle
- ✅ Enhanced visualizations
- ✅ Auto-complete user search
- ✅ Real-time rate limit monitoring

### 🔧 Technical Improvements
- SQLAlchemy database integration
- Flask-Caching for performance
- Flask-Limiter for rate limiting
- Flask-CORS for API access
- Improved error handling
- Better code organization
- Comprehensive API documentation

## Step-by-Step Upgrade

### 1. Backup Your Current Setup

```bash
# Backup your current .env file
cp .env .env.backup

# If you have any custom changes, note them down
```

### 2. Update Dependencies

```bash
# Install new dependencies
pip install -r requirements.txt
```

### 3. Update Environment Configuration

The `.env` file has new variables. Update your `.env`:

```env
# Your existing token
GITHUB_TOKEN=your_token_here

# New required settings
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///github_analytics.db

# New optional settings
CACHE_TYPE=simple
ENABLE_ANALYTICS_EXPORT=True
ENABLE_COMPARISON_MODE=True
ENABLE_HISTORICAL_TRACKING=True
```

See `.env.example` for all available options.

### 4. Database Setup

The new version uses a database to track historical data:

```bash
# The database will be created automatically on first run
python run.py
```

### 5. Update Your Code (if you have custom modifications)

#### Old GitHub Service → New Advanced Service

**Before:**
```python
from app.services.github_service import GitHubService
service = GitHubService()
stats, error = service.get_user_stats(username)
```

**After:**
```python
from app.services.advanced_github_service import AdvancedGitHubService
service = AdvancedGitHubService()
stats, error = service.get_comprehensive_user_stats(username)
```

#### Template Changes

If you customized `index.html`, you may want to:
- Use the new `index_enhanced.html` as a base
- Or keep your old template (both are compatible)

### 6. Test the Upgrade

1. **Start the application:**
```bash
python run.py
```

2. **Test basic functionality:**
   - Visit http://localhost:5000
   - Search for a GitHub user
   - Verify charts and statistics load

3. **Test new features:**
   - Try the comparison feature at `/compare`
   - Export data using the export buttons
   - Check API at `/docs`

4. **Test API endpoints:**
```bash
# Test user stats
curl http://localhost:5000/api/user/octocat

# Test rate limit
curl http://localhost:5000/api/rate-limit
```

## Configuration Options

### Caching

**Simple Cache (Default - No setup required):**
```env
CACHE_TYPE=simple
```

**Redis Cache (Recommended for production):**
```env
CACHE_TYPE=redis
CACHE_REDIS_URL=redis://localhost:6379/0
```

Install and start Redis:
```bash
# Windows (using Chocolatey)
choco install redis-64

# Or download from: https://github.com/microsoftarchive/redis/releases

# Start Redis
redis-server
```

**Filesystem Cache:**
```env
CACHE_TYPE=filesystem
```

### Database Options

**SQLite (Default - Good for small to medium usage):**
```env
DATABASE_URL=sqlite:///github_analytics.db
```

**PostgreSQL (Recommended for production):**
```env
DATABASE_URL=postgresql://user:password@localhost/github_analytics
```

**MySQL:**
```env
DATABASE_URL=mysql://user:password@localhost/github_analytics
```

## Optional Enhancements

### 1. Setup Redis (Recommended)

Redis improves caching performance significantly.

**Installation:**
```bash
# Download Redis for Windows
# Visit: https://github.com/microsoftarchive/redis/releases

# Or use Windows Subsystem for Linux (WSL)
sudo apt-get install redis-server
sudo service redis-server start
```

**Configure:**
```env
CACHE_TYPE=redis
CACHE_REDIS_URL=redis://localhost:6379/0
RATELIMIT_STORAGE_URL=redis://localhost:6379/1
```

### 2. Setup PostgreSQL (For Production)

**Installation:**
```bash
# Download from: https://www.postgresql.org/download/

# Create database
createdb github_analytics
```

**Configure:**
```env
DATABASE_URL=postgresql://username:password@localhost/github_analytics
```

### 3. Enable Advanced Features

```env
# Historical tracking (stores snapshots over time)
ENABLE_HISTORICAL_TRACKING=True

# User comparison
ENABLE_COMPARISON_MODE=True

# Data export
ENABLE_ANALYTICS_EXPORT=True

# Advanced charts
ENABLE_ADVANCED_CHARTS=True
```

## Migration Checklist

- [ ] Backed up `.env` file
- [ ] Installed new dependencies
- [ ] Updated `.env` configuration
- [ ] Tested basic functionality
- [ ] Tested new features (comparison, export)
- [ ] Tested API endpoints
- [ ] (Optional) Configured Redis
- [ ] (Optional) Configured production database
- [ ] Verified all charts load correctly
- [ ] Checked error handling

## Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution:** Install missing dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Issue: Database errors
**Solution:** Delete old database and let it recreate
```bash
# Backup first if needed
rm github_analytics.db
python run.py
```

### Issue: Cache not working
**Solution:** Check Redis is running
```bash
redis-cli ping
# Should respond: PONG
```

### Issue: Rate limit errors
**Solution:** Verify GitHub token
```bash
# Test token
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/rate_limit
```

### Issue: Charts not displaying
**Solution:** Clear browser cache and reload

### Issue: Export not working
**Solution:** Check permissions on directory
```bash
# Ensure write permissions
chmod 755 .
```

## Rollback Plan

If you need to rollback to the original version:

1. **Restore backup:**
```bash
cp .env.backup .env
```

2. **Reinstall old dependencies:**
```bash
pip uninstall -r requirements.txt -y
pip install Flask==3.0.0 PyGithub==2.2.0 python-dotenv==1.0.0 requests==2.31.0 python-dateutil==2.8.2
```

3. **Use original template:**
   - Rename `index.html` to use the original version

## Performance Tips

1. **Enable Redis caching** - Reduces API calls dramatically
2. **Increase cache timeout** - For data that doesn't change often
3. **Use PostgreSQL** - Better performance for large datasets
4. **Enable rate limiting** - Prevents abuse
5. **Monitor rate limits** - Use `/api/rate-limit` endpoint

## Getting Help

If you encounter issues:

1. Check the [documentation](docs.html)
2. Review [GitHub Issues](https://github.com/yourusername/github-analytics-pro/issues)
3. Check application logs for errors
4. Verify `.env` configuration

## Next Steps

After successful upgrade:

1. ✅ Explore the comparison feature
2. ✅ Try exporting data in different formats
3. ✅ Check out the API documentation
4. ✅ Customize the theme (dark/light)
5. ✅ Monitor historical data tracking
6. ✅ Test API integrations

---

**Congratulations! You're now running GitHub Analytics Pro** 🎉

For questions or feedback, please open an issue on GitHub.
