# backend/scripts/create_admin.py
import sys
from app.db.session import SessionLocal
from app.db.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.core.config import settings

def create_admin():
    db = SessionLocal()
    repo = UserRepository(db)
    
    admin = UserCreate(
        email=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        is_superuser=True,
        full_name="Admin User"
    )
    
    try:
        existing_user = repo.get_by_email(admin.email)
        if existing_user:
            print("Admin user already exists")
            return
        
        repo.create(admin)
        print("Admin user created successfully")
    except Exception as e:
        print(f"Error creating admin user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()