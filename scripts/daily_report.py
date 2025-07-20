# scripts/daily_report.py
import asyncio
import asyncpg
import redis
import requests
import os
from datetime import datetime, timedelta

async def generate_daily_report():
    """Generate daily system status report"""
    
    report = f"""
🏠 Real Estate CRM - Daily Status Report
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*50}

"""
    
    # Database stats
    try:
        conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
        user_count = await conn.fetchval('SELECT COUNT(*) FROM users')
        company_count = await conn.fetchval('SELECT COUNT(*) FROM companies')
        match_count = await conn.fetchval('SELECT COUNT(*) FROM matches WHERE created_at >= $1', 
                                        datetime.now() - timedelta(days=1))
        await conn.close()
        
        report += f"""📊 Database Statistics:
- Total Users: {user_count}
- Total Companies: {company_count}
- Matches (24h): {match_count}

"""
    except Exception as e:
        report += f"❌ Database error: {e}\n\n"
    
    # Redis stats
    try:
        r = redis.from_url(os.getenv('REDIS_URL'))
        redis_info = r.info()
        report += f"""📈 Redis Statistics:
- Memory Usage: {redis_info['used_memory_
