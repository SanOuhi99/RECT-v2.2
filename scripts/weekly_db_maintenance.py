# scripts/weekly_db_maintenance.py
import asyncio
import asyncpg
import os
from datetime import datetime, timedelta

async def database_maintenance():
    """Run weekly database maintenance"""
    
    conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
    
    try:
        # Check database size
        size_result = await conn.fetchval("""
            SELECT pg_size_pretty(pg_database_size(current_database()))
        """)
        print(f"📊 Database size: {size_result}")
        
        # Check for long-running queries
        long_queries = await conn.fetch("""
            SELECT query, state, query_start, now() - query_start as duration
            FROM pg_stat_activity 
            WHERE now() - query_start > interval '1 hour'
            AND state != 'idle'
        """)
        
        if long_queries:
            print(f"⚠️  {len(long_queries)} long-running queries found")
            for query in long_queries:
                print(f"   Duration: {query['duration']}")
        else:
            print("✅ No long-running queries")
        
        # Update table statistics
        await conn.execute("ANALYZE;")
        print("✅ Database statistics updated")
        
        # Clean up old data (customize based on your needs)
        cutoff_date = datetime.now() - timedelta(days=90)
        
        # Example: Clean old logs (adjust table names as needed)
        # deleted = await conn.fetchval("""
        #     DELETE FROM logs WHERE created_at < $1
        # """, cutoff_date)
        # print(f"🗑️  Deleted {deleted} old log entries")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(database_maintenance())
