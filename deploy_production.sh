#!/bin/bash

# Production Deployment Script for Railway
# Real Estate CRM Tracker

set -e  # Exit on any error

echo "🚀 Starting Production Deployment for Real Estate CRM..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Railway CLI is installed
check_railway_cli() {
    if ! command -v railway &> /dev/null; then
        print_error "Railway CLI is not installed!"
        echo "Please install it from: https://docs.railway.app/cli/quick-start"
        exit 1
    fi
    print_success "Railway CLI is installed"
}

# Generate secure secret key
generate_secret_key() {
    python3 -c "import secrets; print(secrets.token_urlsafe(32))"
}

# Create production environment files
create_env_files() {
    print_status "Creating production environment files..."
    
    # Generate secret key
    SECRET_KEY=$(generate_secret_key)
    
    # Backend .env.production
    cat > backend/.env.production << EOF
# === PRODUCTION ENVIRONMENT VARIABLES ===
# Generated on $(date)

# Security
SECRET_KEY=$SECRET_KEY
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Application
PROJECT_NAME=Real Estate CRM Tracker
API_V1_STR=/api/v1
ENVIRONMENT=production

# Database (Railway will override these)
DATABASE_URL=postgresql://user:pass@host:5432/db
POSTGRES_SERVER=host
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=railway

# Redis (Railway will override this)
REDIS_URL=redis://default:password@host:6379

# External APIs (UPDATE THESE WITH YOUR CREDENTIALS)
DATATREE_CLIENT_ID=your_production_datatree_client_id
DATATREE_CLIENT_SECRET=your_production_datatree_client_secret

# Email (UPDATE THESE WITH YOUR EMAIL SERVICE)
SMTP_SERVER=smtp.mailgun.org
SMTP_PORT=587
SENDER_EMAIL=noreply@yourdomain.com
SMTP_USERNAME=noreply@yourdomain.com
SMTP_PASSWORD=your_production_email_password

# Monitoring (Optional - sign up at sentry.io)
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
EOF

    # Frontend .env.production
    cat > frontend/.env.production << EOF
# === FRONTEND PRODUCTION ENVIRONMENT ===
# Generated on $(date)

# Environment
NODE_ENV=production
ENVIRONMENT=production

# API Configuration (UPDATE WITH YOUR BACKEND URL)
NEXT_PUBLIC_API_URL=https://realestate-backend-production.up.railway.app

# Monitoring (Optional)
NEXT_PUBLIC_SENTRY_DSN=https://your-frontend-sentry-dsn@sentry.io/project-id

# Custom Domain (Optional)
NEXT_PUBLIC_APP_URL=https://app.yourdomain.com
EOF

    # Worker .env.production  
    cat > worker/.env.production << EOF
# === WORKER PRODUCTION ENVIRONMENT ===
# Generated on $(date)

# Environment
ENVIRONMENT=production

# Database (Railway will override this)
DATABASE_URL=postgresql://user:pass@host:5432/db

# Redis (Railway will override this)
REDIS_URL=redis://default:password@host:6379

# External APIs (UPDATE THESE - SAME AS BACKEND)
DATATREE_CLIENT_ID=your_production_datatree_client_id
DATATREE_CLIENT_SECRET=your_production_datatree_client_secret

# Email (UPDATE THESE - SAME AS BACKEND)
SMTP_SERVER=smtp.mailgun.org
SMTP_PORT=587
SENDER_EMAIL=noreply@yourdomain.com
SMTP_USERNAME=noreply@yourdomain.com
SMTP_PASSWORD=your_production_email_password

# Monitoring (Optional)
SENTRY_DSN=https://your-worker-sentry-dsn@sentry.io/project-id
EOF

    print_success "Environment files created!"
    print_warning "⚠️  IMPORTANT: Update the API credentials in the .env.production files!"
}

# Create nixpacks.toml files
create_nixpacks_configs() {
    print_status "Creating nixpacks.toml configuration files..."
    
    # Backend nixpacks.toml
    mkdir -p backend
    cat > backend/nixpacks.toml << 'EOF'
[phases.setup]
nixPkgs = ["python311", "postgresql_15"]

[phases.install]
cmds = [
  "pip install --upgrade pip",
  "pip install --no-cache-dir -r requirements.txt"
]

[phases.build]
cmds = [
  "python -m compileall -b .",
  "find . -name '*.py' -delete",
  "find . -name '__pycache__' -exec rm -rf {} +"
]

[start]
cmd = "gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --timeout 120 --access-logfile - --error-logfile -"

[variables]
PYTHONPATH = "/app"
PYTHONUNBUFFERED = "1"
PYTHONDONTWRITEBYTECODE = "1"
EOF

    # Frontend nixpacks.toml
    mkdir -p frontend
    cat > frontend/nixpacks.toml << 'EOF'
[phases.setup]
nixPkgs = ["nodejs_20", "npm"]

[phases.install]
cmds = ["npm ci --only=production"]

[phases.build]
cmds = [
  "npm run build",
  "npm prune --production"
]

[start]
cmd = "npm start"

[variables]
NODE_ENV = "production"
EOF

    # Worker nixpacks.toml
    mkdir -p worker
    cat > worker/nixpacks.toml << 'EOF'
[phases.setup]
nixPkgs = ["python311"]

[phases.install]
cmds = [
  "pip install --upgrade pip",
  "pip install --no-cache-dir -r requirements.txt"
]

[phases.build]
cmds = [
  "python -m compileall -b .",
  "find . -name '*.py' -delete",
  "find . -name '__pycache__' -exec rm -rf {} +"
]

[start]
cmd = "celery -A worker worker --loglevel=info --concurrency=4 --max-tasks-per-child=100"

[variables]
PYTHONPATH = "/app"
PYTHONUNBUFFERED = "1"
PYTHONDONTWRITEBYTECODE = "1"
EOF

    print_success "nixpacks.toml files created!"
}

# Create railway.json
create_railway_config() {
    print_status "Creating railway.json configuration..."
    
    cat > railway.json << 'EOF'
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "numReplicas": 2,
    "restartPolicyType": "ON_FAILURE", 
    "restartPolicyMaxRetries": 5,
    "healthcheck": {
      "enabled": true
    }
  }
}
EOF

    print_success "railway.json created!"
}

# Update package.json for production
update_package_json() {
    print_status "Updating frontend package.json for production..."
    
    if [ -f "frontend/package.json" ]; then
        # Backup original
        cp frontend/package.json frontend/package.json.backup
        
        # Update start script to use PORT variable
        python3 << 'EOF'
import json
import sys

try:
    with open('frontend/package.json', 'r') as f:
        package = json.load(f)
    
    # Update scripts
    if 'scripts' not in package:
        package['scripts'] = {}
    
    package['scripts']['start'] = 'next start -p $PORT'
    
    # Add production dependencies if not present
    if '@next/bundle-analyzer' not in package.get('devDependencies', {}):
        if 'devDependencies' not in package:
            package['devDependencies'] = {}
        package['devDependencies']['@next/bundle-analyzer'] = '^14.0.4'
        package['devDependencies']['cross-env'] = '^7.0.3'
    
    with open('frontend/package.json', 'w') as f:
        json.dump(package, f, indent=2)
    
    print("✅ package.json updated successfully")
    
except Exception as e:
    print(f"❌ Error updating package.json: {e}")
    sys.exit(1)
EOF
        
        print_success "Frontend package.json updated!"
    else
        print_warning "frontend/package.json not found, skipping..."
    fi
}

# Add gunicorn to backend requirements if not present
update_backend_requirements() {
    print_status "Updating backend requirements.txt for production..."
    
    if [ -f "backend/requirements.txt" ]; then
        # Check if gunicorn is already present
        if ! grep -q "gunicorn" backend/requirements.txt; then
            echo "gunicorn==21.2.0" >> backend/requirements.txt
            print_success "Added gunicorn to requirements.txt"
        fi
        
        # Check if sentry-sdk is present for error monitoring
        if ! grep -q "sentry-sdk" backend/requirements.txt; then
            echo "sentry-sdk[fastapi]==1.38.0" >> backend/requirements.txt
            print_success "Added sentry-sdk to requirements.txt"
        fi
    else
        print_warning "backend/requirements.txt not found, skipping..."
    fi
}

# Create production deployment checklist
create_deployment_checklist() {
    print_status "Creating deployment checklist..."
    
    cat > DEPLOYMENT_CHECKLIST.md << 'EOF'
# 🚀 Production Deployment Checklist

## Pre-Deployment Setup

### 1. External Services Setup
- [ ] **DataTree API**: Get production credentials
  - Client ID: `DATATREE_CLIENT_ID`
  - Client Secret: `DATATREE_CLIENT_SECRET`
  
- [ ] **Email Service**: Set up production email (Mailgun, SendGrid, etc.)
  - SMTP Server: `SMTP_SERVER`
  - SMTP Port: `SMTP_PORT`
  - Email: `SENDER_EMAIL`
  - Username: `SMTP_USERNAME` 
  - Password: `SMTP_PASSWORD`

- [ ] **Sentry** (Optional but recommended): Set up error monitoring
  - Backend DSN: `SENTRY_DSN`
  - Frontend DSN: `NEXT_PUBLIC_SENTRY_DSN`
  - Worker DSN: `SENTRY_DSN`

### 2. Update Environment Files
- [ ] Update `backend/.env.production` with real API credentials
- [ ] Update `frontend/.env.production` with backend URL
- [ ] Update `worker/.env.production` with real API credentials
- [ ] Verify SECRET_KEY is secure (generated automatically)

## Railway Deployment Steps

### 1. Create Railway Project
```bash
railway login
railway new
```

### 2. Deploy Services (in order)

#### Backend Service
```bash
railway service create realestate-backend
railway service use realestate-backend
railway up --detach
```

#### Worker Service  
```bash
railway service create realestate-worker
railway service use realestate-worker
railway up --detach
```

#### Frontend Service
```bash
railway service create realestate-frontend
railway service use realestate-frontend
railway up --detach
```

### 3. Add Database Services
```bash
# Add PostgreSQL
railway add postgresql

# Add Redis
railway add redis
```

### 4. Set Environment Variables
Copy variables from `.env.production` files to Railway dashboard:
- Backend service: Use `backend/.env.production`
- Frontend service: Use `frontend/.env.production` 
- Worker service: Use `worker/.env.production`

**Important**: Railway auto-generates `DATABASE_URL` and `REDIS_URL`

### 5. Post-Deployment Tasks

#### Database Setup
```bash
# Connect to backend service
railway shell realestate-backend

# Run migrations
alembic upgrade head

# Create admin user (optional)
python scripts/create_admin.py
```

#### Upload Data Files
```bash
# Upload CRM configuration files
# Place in /app/data/ directory:
# - crm_owners.json
# - companies.json
# - state_county.csv
```

## Testing Checklist

### Backend Health Check
- [ ] Visit: `https://your-backend.up.railway.app/health`
- [ ] Check API docs: `https://your-backend.up.railway.app/docs`
- [ ] Test authentication endpoint

### Frontend Access
- [ ] Visit: `https://your-frontend.up.railway.app`
- [ ] Test user registration
- [ ] Test login functionality
- [ ] Test dashboard access

### Worker Functionality
- [ ] Check Railway logs for worker service
- [ ] Test background job creation
- [ ] Verify task processing

### Integration Tests
- [ ] Test property matching workflow
- [ ] Test email notifications
- [ ] Test data processing pipeline

## Security Checklist

- [ ] All environment variables are set securely
- [ ] No credentials in source code
- [ ] CORS is configured for production domains only
- [ ] HTTPS is enabled (Railway default)
- [ ] Database connections are encrypted
- [ ] Rate limiting is enabled

## Monitoring Setup

- [ ] Set up Sentry error tracking
- [ ] Monitor Railway service metrics
- [ ] Set up uptime monitoring
- [ ] Configure alerting for critical issues

## Performance Optimization

- [ ] Enable Railway auto-scaling if needed
- [ ] Monitor CPU and memory usage
- [ ] Optimize database queries
- [ ] Configure caching if necessary

## Backup Strategy

- [ ] Set up automated database backups
- [ ] Back up configuration files
- [ ] Document recovery procedures
- [ ] Test backup restoration

## Custom Domain (Optional)

- [ ] Purchase domain
- [ ] Configure DNS records
- [ ] Set up SSL certificates
- [ ] Update CORS settings

## Go-Live Checklist

- [ ] All services are healthy
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Team is trained on production system
- [ ] Support procedures are in place
- [ ] Monitoring is active

---
Generated by deployment script on $(date)
EOF

    print_success "Deployment checklist created: DEPLOYMENT_CHECKLIST.md"
}

# Create production health check script
create_health_check_script() {
    print_status "Creating production health check script..."
    
    cat > scripts/health_check.py << 'EOF'
#!/usr/bin/env python3
"""
Production Health Check Script
Checks all services are running properly
"""
import requests
import sys
import os
from urllib.parse import urljoin

def check_service(name, url, expected_status=200):
    """Check if a service is healthy"""
    try:
        print(f"🔍 Checking {name}...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == expected_status:
            print(f"✅ {name} is healthy (status: {response.status_code})")
            return True
        else:
            print(f"❌ {name} returned status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ {name} connection failed: {e}")
        return False

def main():
    """Run health checks on all services"""
    
    # Get URLs from environment or use defaults
    backend_url = os.getenv('BACKEND_URL', 'https://realestate-backend-production.up.railway.app')
    frontend_url = os.getenv('FRONTEND_URL', 'https://realestate-frontend-production.up.railway.app')
    
    print("🏥 Running Production Health Checks...")
    print("=" * 50)
    
    services = [
        ("Backend API", urljoin(backend_url, "/health")),
        ("Backend Root", backend_url),
        ("Frontend", frontend_url),
    ]
    
    all_healthy = True
    
    for service_name, service_url in services:
        if not check_service(service_name, service_url):
            all_healthy = False
    
    print("=" * 50)
    
    if all_healthy:
        print("🎉 All services are healthy!")
        sys.exit(0)
    else:
        print("💥 Some services are unhealthy!")
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF

    chmod +x scripts/health_check.py
    print_success "Health check script created: scripts/health_check.py"
}

# Main deployment function
main() {
    echo "🏗️  Real Estate CRM - Production Deployment Setup"
    echo "=================================================="
    
    # Run all setup functions
    check_railway_cli
    create_env_files
    create_nixpacks_configs
    create_railway_config
    update_package_json
    update_backend_requirements
    create_deployment_checklist
    
    # Create scripts directory if it doesn't exist
    mkdir -p scripts
    create_health_check_script
    
    print_success "🎉 Production deployment setup complete!"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Update API credentials in .env.production files"
    echo "2. Commit and push to GitHub"
    echo "3. Follow DEPLOYMENT_CHECKLIST.md for Railway deployment"
    echo "4. Run 'python scripts/health_check.py' after deployment"
    echo ""
    print_warning "⚠️  IMPORTANT: Review and update all .env.production files with real credentials!"
}

# Run main function
main "$@"