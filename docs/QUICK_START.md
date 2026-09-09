# 🚀 Quick Start Guide - Local Hosting

## ✅ Setup Status

Your GitHub Analytics Pro is **almost ready**! All dependencies are installed.

## 📋 What You Need

### Get Your GitHub Personal Access Token

1. **Go to GitHub Settings:**
   - Visit: https://github.com/settings/tokens
   - Or: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)

2. **Generate New Token:**
   - Click "Generate new token (classic)"
   - Give it a name: `GitHub Analytics Pro`
   - Set expiration: 90 days (or No expiration)

3. **Select Permissions (Scopes):**
   - ✅ `read:user` - Read user profile data
   - ✅ `public_repo` - Access public repositories
   - ✅ `read:org` - Read organization data (optional)

4. **Generate and Copy Token:**
   - Click "Generate token" at the bottom
   - **IMPORTANT:** Copy the token immediately (you won't see it again!)

5. **Add Token to .env File:**
   - Open `.env` file in the project root
   - Replace `your_github_token_here` with your actual token:
   ```
   GITHUB_TOKEN=ghp_YourActualTokenHere123456789
   ```
   - Save the file

## 🚀 Starting the Application

### Option 1: Using the Setup Script (Recommended)
```cmd
python setup_local.py
python run.py
```

### Option 2: Direct Start
```cmd
python run.py
```

## 🌐 Access the Application

Once the server starts, you'll see:
```
 * Running on http://127.0.0.1:5000
```

Open your browser and go to:
- **Main App:** http://localhost:5000
- **API Docs:** http://localhost:5000/docs
- **Comparison:** http://localhost:5000/compare
- **About:** http://localhost:5000/about

## 🎯 Testing the Application

### Test with Your Own Username
1. Enter your GitHub username in the search box
2. Click "Analyze"
3. View your comprehensive GitHub analytics!

### Try These Demo Users
- `octocat` - GitHub's mascot
- `torvalds` - Linux creator
- `gvanrossum` - Python creator
- `defunkt` - GitHub co-founder

### Test the Comparison Feature
1. Go to: http://localhost:5000/compare
2. Enter: `octocat, torvalds, gvanrossum`
3. Click "Compare Users"

### Test the API
```cmd
# In a new terminal
curl http://localhost:5000/api/user/octocat
curl http://localhost:5000/api/rate-limit
```

## 🔧 Troubleshooting

### Issue: "GitHub token not found"
**Solution:** Add your token to `.env` file (see above)

### Issue: "Rate limit exceeded"
**Solution:** You need a GitHub token for higher rate limits
- Without token: 60 requests/hour
- With token: 5,000 requests/hour

### Issue: Port 5000 already in use
**Solution:** Change the port in `run.py`:
```python
app.run(debug=True, port=5001)
```

### Issue: Module not found
**Solution:** Install missing packages:
```cmd
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### Issue: SSL Certificate Error
**Solution:** Use trusted hosts flag:
```cmd
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org [package-name]
```

## 📊 What You Can Do

### Analytics Features
- ✅ View comprehensive user statistics
- ✅ See top repositories by stars/forks/activity
- ✅ Analyze language distribution
- ✅ Track contribution patterns
- ✅ View advanced metrics (Impact, Consistency, Diversity scores)

### Export Features
- ✅ Export as JSON
- ✅ Export as CSV
- ✅ Export as Markdown

### Comparison Features
- ✅ Compare up to 5 users
- ✅ Side-by-side visualizations
- ✅ Metric comparisons

### API Features
- ✅ RESTful API endpoints
- ✅ User search
- ✅ Historical data
- ✅ Rate limit info

## 🎨 Customization

### Change Theme
Click the theme toggle button in the top-right corner to switch between dark/light themes.

### Adjust Cache Timeout
Edit `.env`:
```
CACHE_TIMEOUT=7200  # 2 hours
```

### Change Rate Limits
Edit `.env`:
```
RATELIMIT_DEFAULT=200 per hour
```

## 📚 Next Steps

1. ✅ Add GitHub token
2. ✅ Test with your username
3. ✅ Try the comparison feature
4. ✅ Explore the API
5. ✅ Check the documentation at `/docs`
6. Read FEATURES.md for complete feature list
7. Read DEPLOYMENT.md for production deployment

## 🆘 Need Help?

- Check the main README.md
- Review FEATURES.md for all capabilities
- Read the API docs at http://localhost:5000/docs
- Check TROUBLESHOOTING section above

---

**You're all set! Just add your GitHub token and run `python run.py`** 🎉
