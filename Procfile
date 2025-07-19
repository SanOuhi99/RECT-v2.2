web: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
frontend: cd frontend && npm run build && npm run start
worker: cd worker && celery -A worker worker --loglevel=info
