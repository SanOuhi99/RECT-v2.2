# scripts/check_db_health.py
import asyncio
import asyncpg
import os

async def check_database():
    try:
        conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
        result = await conn.fetchval('SELECT version()')
        await conn.close()
        print(f"✅ Database healthy: {result}")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(check_database())