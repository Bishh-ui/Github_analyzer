# 🚀 Deployment Guide - GitHub Analytics Pro

This guide covers deploying GitHub Analytics Pro to various platforms.

## Table of Contents
- [Vercel (Serverless)](#vercel-serverless)
- [Local Development](#local-development)
- [Production Preparation](#production-preparation)
- [Deployment Platforms](#deployment-platforms)
  - [Vercel](#vercel-serverless)
  - [Heroku](#heroku)
  - [Railway](#railway)
  - [PythonAnywhere](#pythonanywhere)
  - [Docker](#docker)
  - [Traditional VPS](#traditional-vps)

---

## Local Development

### Prerequisites
- Python 3.8+
- pip
- Git
- GitHub Personal Access Token

### Setup
```bash
# Clone repository
git clone https://github.com/yourusername/github-analytics-pro.git
cd github-analytics-pro

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run application
python run.py
```

---

## Production Preparation

### 1. Security Checklist

```env
# .env for production
DEBUG=False
SECRET_KEY=<generate_strong_random_key>
GITHUB_TOKEN=<your_github_token>
DATABASE_URL=<production_database_url>
CACHE_TYPE=redis
CACHE_REDIS_URL=<redis_url>
```

Generate a secure secret key:
```bash
python -c "import os; print(os.urandom(24).hex())"
```

### 2. Database Setup

**PostgreSQL (Recommended):**
```bash
# Install PostgreSQL
# Create database
createdb github_analytics_prod

# Update .env
DATABASE_URL=postgresql://user:password@localhost/github_analytics_prod
```

### 3. Dependencies

Create `requirements-prod.txt`:
```txt
Flask==3.0.0
PyGithub==2.2.0
python-dotenv==1.0.0
requests==2.31.0
python-dateutil==2.8.2
redis==5.0.1
Flask-Caching==2.1.0
Flask-CORS==4.0.0
Flask-Limiter==3.5.0
numpy==1.26.2
pandas==2.1.4
SQLAlchemy==2.0.23
Flask-SQLAlchemy==3.1.1
gunicorn==21.2.0
psycopg2-binary==2.9.9
```

---

## Deployment Platforms

### Vercel (Serverless)

GitHub Analytics Pro is pre-configured for Vercel using `@vercel/python` serverless functions.

#### Pre-configured Files
- **`vercel.json`**: Configures serverless rewrites to route requests through `api/index.py`.
- **`api/index.py`**: WSGI serverless entry point exposing the Flask `app`.

#### Deploy Steps

1. **Push your code to GitHub** (already configured):
   ```bash
   git push origin main
   ```

2. **Import into Vercel**:
   - Go to [vercel.com](https://vercel.com) and log in.
   - Click **"Add New..." → "Project"**.
   - Import your repository: **`Bishh-ui/Github_analyzer`**.

3. **Configure Environment Variables**:
   In the Vercel deployment wizard, expand **Environment Variables** and add:
   - `GITHUB_TOKEN`: `ghp_YourPersonalAccessToken`
   - `SECRET_KEY`: `any_random_secret_string` (generate with `python -c "import secrets; print(secrets.token_hex(24))"`)
   - `DEBUG`: `False`

4. **Deploy**:
   - Click **Deploy**! Vercel will install packages from `requirements.txt` and launch your project in ~1-2 minutes.

---

### Heroku

#### Prerequisites
- Heroku account
- Heroku CLI installed

#### Files Needed

**`Procfile`:**
```
web: gunicorn run:app
```

**`runtime.txt`:**
```
python-3.11.5
```

#### Deploy Steps

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Add Redis
heroku addons:create heroku-redis:mini

# Set environment variables
heroku config:set GITHUB_TOKEN=your_token_here
heroku config:set SECRET_KEY=$(python -c "import os; print(os.urandom(24).hex())")
heroku config:set DEBUG=False
heroku config:set CACHE_TYPE=redis

# Deploy
git push heroku main

# Open app
heroku open

# View logs
heroku logs --tail
```

#### Heroku Config

The database URL and Redis URL are automatically set by Heroku addons.

---

### Railway

#### Prerequisites
- Railway account
- Railway CLI (optional)

#### Deploy Steps

**Option 1: GitHub Integration**
1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Add PostgreSQL and Redis services
6. Set environment variables in Railway dashboard

**Option 2: Railway CLI**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize
railway init

# Deploy
railway up

# Add PostgreSQL
railway add postgresql

# Add Redis
railway add redis

# Set environment variables
railway variables set GITHUB_TOKEN=your_token
railway variables set DEBUG=False
```

#### Railway Config

Railway automatically provides `DATABASE_URL` and `REDIS_URL`.

---

### PythonAnywhere

#### Prerequisites
- PythonAnywhere account (free or paid)

#### Deploy Steps

1. **Upload Code:**
```bash
# In PythonAnywhere Bash console
git clone https://github.com/yourusername/github-analytics-pro.git
cd github-analytics-pro
```

2. **Create Virtual Environment:**
```bash
mkvirtualenv --python=/usr/bin/python3.10 myenv
pip install -r requirements.txt
```

3. **Configure WSGI:**

Create `/var/www/yourusername_pythonanywhere_com_wsgi.py`:
```python
import sys
import os

# Add your project directory
project_home = '/home/yourusername/github-analytics-pro'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load environment variables
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

# Import Flask app
from run import app as application
```

4. **Web App Configuration:**
- Go to Web tab
- Set source code directory: `/home/yourusername/github-analytics-pro`
- Set working directory: `/home/yourusername/github-analytics-pro`
- Set virtualenv: `/home/yourusername/.virtualenvs/myenv`
- Reload web app

---

### Docker

#### Dockerfile

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=run.py
ENV PYTHONUNBUFFERED=1

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "run:app"]
```

#### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://postgres:password@db:5432/github_analytics
      - CACHE_TYPE=redis
      - CACHE_REDIS_URL=redis://redis:6379/0
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
      - redis
    volumes:
      - .:/app
    command: gunicorn --bind 0.0.0.0:5000 --workers 4 run:app

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=github_analytics
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

#### Deploy with Docker

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

### Traditional VPS (Ubuntu)

#### Prerequisites
- Ubuntu 20.04+ server
- SSH access
- Domain name (optional)

#### Setup Steps

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3-pip python3-venv nginx postgresql redis-server -y

# Create user
sudo useradd -m -s /bin/bash ghanalytics
sudo su - ghanalytics

# Clone repository
git clone https://github.com/yourusername/github-analytics-pro.git
cd github-analytics-pro

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Configure environment
cp .env.example .env
nano .env
# Set your configuration

# Setup PostgreSQL
sudo -u postgres createuser ghanalytics
sudo -u postgres createdb github_analytics
sudo -u postgres psql -c "ALTER USER ghanalytics WITH PASSWORD 'your_password';"

# Test application
gunicorn --bind 0.0.0.0:8000 run:app
```

#### Systemd Service

Create `/etc/systemd/system/ghanalytics.service`:

```ini
[Unit]
Description=GitHub Analytics Pro
After=network.target

[Service]
User=ghanalytics
Group=ghanalytics
WorkingDirectory=/home/ghanalytics/github-analytics-pro
Environment="PATH=/home/ghanalytics/github-analytics-pro/venv/bin"
ExecStart=/home/ghanalytics/github-analytics-pro/venv/bin/gunicorn --workers 4 --bind unix:ghanalytics.sock -m 007 run:app

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable ghanalytics
sudo systemctl start ghanalytics
sudo systemctl status ghanalytics
```

#### Nginx Configuration

Create `/etc/nginx/sites-available/ghanalytics`:

```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ghanalytics/github-analytics-pro/ghanalytics.sock;
    }

    location /static {
        alias /home/ghanalytics/github-analytics-pro/static;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/ghanalytics /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

#### SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your_domain.com
```

---

## Post-Deployment

### Monitoring

**Check Application Logs:**
```bash
# Heroku
heroku logs --tail

# Docker
docker-compose logs -f web

# Systemd
sudo journalctl -u ghanalytics -f
```

**Check Database:**
```bash
# PostgreSQL
psql -d github_analytics -c "SELECT COUNT(*) FROM user_analytics;"
```

**Check Redis:**
```bash
redis-cli ping
redis-cli INFO stats
```

### Performance Optimization

1. **Enable caching:**
   - Use Redis for caching
   - Increase cache timeout for stable data

2. **Database optimization:**
   - Create indexes on frequently queried columns
   - Use connection pooling

3. **CDN for static files:**
   - Use Cloudflare or similar
   - Enable gzip compression

4. **Worker processes:**
   - Adjust gunicorn workers: `--workers (2 * CPU_cores + 1)`

### Backup Strategy

**Database Backup:**
```bash
# PostgreSQL
pg_dump github_analytics > backup_$(date +%Y%m%d).sql

# Automated backup (cron)
0 2 * * * pg_dump github_analytics > /backups/db_$(date +\%Y\%m\%d).sql
```

**Application Backup:**
```bash
# Backup application files
tar -czf app_backup_$(date +%Y%m%d).tar.gz github-analytics-pro/
```

---

## Troubleshooting

### Common Issues

**Issue: Application won't start**
```bash
# Check logs
# Check environment variables
# Verify database connectivity
```

**Issue: Database connection errors**
```bash
# Test database connection
psql $DATABASE_URL

# Check credentials
# Verify network access
```

**Issue: Rate limit exceeded**
```bash
# Check GitHub token
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/rate_limit

# Increase cache timeout
# Implement request throttling
```

---

## Security Best Practices

1. **Never commit `.env` file**
2. **Use strong SECRET_KEY**
3. **Enable HTTPS in production**
4. **Implement rate limiting**
5. **Regular security updates**
6. **Monitor for suspicious activity**
7. **Use environment-specific configs**
8. **Backup data regularly**

---

## Support

For deployment help:
- [GitHub Issues](https://github.com/yourusername/github-analytics-pro/issues)
- [Documentation](README.md)
- [API Docs](/docs)

---

**Happy Deploying! 🚀**
