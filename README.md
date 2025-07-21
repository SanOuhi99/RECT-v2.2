# Real Estate CRM Tracker

Automated property matching system for real estate professionals.
## Features

- CRM owner onboarding with company verification
- Property matching automation
- Background task processing
- Dashboard with analytics

- Email notifications

## Development Setup

1. Clone the repository
2. Create `.env` files in each directory based on `.env.example`
3. Run `docker-compose up --build`

## Services

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Deployment

1. Set up production environment variables
2. Run `docker-compose -f docker-compose.prod.yml up --build`

## Environment Variables

See `.env.example` files in each directory for required variables.
