# Makefile
.PHONY: up down build test migrate

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

test:
	docker-compose exec backend pytest tests/

migrate:
	docker-compose exec backend alembic upgrade head

create-admin:
	docker-compose exec backend python scripts/create_admin.py

backup-db:
	docker-compose exec backend python scripts/backup_db.py