# scripts/verify_backups.py
import os
import asyncpg
import asyncio
from datetime import datetime

async def verify_database_backup():
    """Verify database can be accessed and basic queries work"""
    
    try:
        conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
        
        # Test basic connectivity
        version = await conn.fetchval('SELECT version()')
        print(f"✅ Database connection: {version}")
        
        # Test basic queries on main tables
        tables = ['users', 'companies', 'matches']  # Adjust to your table names
        
        for table in tables:
            try:
                count = await conn.fetchval(f'SELECT COUNT(*) FROM {table}')
                print(f"✅ Table {table}: {count} records")
            except Exception as e:
                print(f"❌ Table {table}: {e}")
        
        await conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database verification failed: {e}")
        return False

def verify_file_backups():
    """Verify important files are backed up"""
    
    important_files = [
        'app/data/crm_owners.json',
        'app/data/companies.json',
        'app/data/state_county.csv'
    ]
    
    for file_path in important_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            print(f"✅ {file_path}: {size} bytes, modified {mod_time}")
        else:
            print(f"❌ Missing: {file_path}")

if __name__ == "__main__":
    print("🔍 Verifying backups...")
    asyncio.run(verify_database_backup())
    verify_file_backups()
