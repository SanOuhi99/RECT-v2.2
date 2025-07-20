#!/bin/bash
# scripts/rolling_update.sh

set -e

echo "🚀 Starting rolling update..."

# Deploy backend first
echo "📡 Updating backend..."
railway service use realestate-backend
railway up --detach

# Wait for backend health check
echo "🔍 Checking backend health..."
sleep 30
python scripts/health_check.py

# Deploy worker
echo "⚙️ Updating worker..."
railway service use realestate-worker  
railway up --detach

# Deploy frontend last
echo "🎨 Updating frontend..."
railway service use realestate-frontend
railway up --detach

echo "✅ Rolling update complete!"
