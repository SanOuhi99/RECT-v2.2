#!/bin/bash
# scripts/rollback.sh

set -e

echo "🔄 Starting rollback..."

# Get previous deployment ID
BACKEND_DEPLOYMENT=$(railway deployments --service realestate-backend --json | jq -r '.[1].id')
WORKER_DEPLOYMENT=$(railway deployments --service realestate-worker --json | jq -r '.[1].id')
FRONTEND_DEPLOYMENT=$(railway deployments --service realestate-frontend --json | jq -r '.[1].id')

# Rollback services
railway deployment rollback $BACKEND_DEPLOYMENT --service realestate-backend
railway deployment rollback $WORKER_DEPLOYMENT --service realestate-worker
railway deployment rollback $FRONTEND_DEPLOYMENT --service realestate-frontend

echo "✅ Rollback complete!"
