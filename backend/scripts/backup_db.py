# backend/scripts/backup_db.py
import os
import datetime
from app.core.config import settings

def backup_database():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backup_{timestamp}.sql"
    
    os.system(
        f"pg_dump {settings.DATABASE_URL} > {backup_file}"
    )
    print(f"Backup created: {backup_file}")

if __name__ == "__main__":
    backup_database()