# scripts/optimize_redis.py
import redis
import os

def optimize_redis():
    """Optimize Redis memory usage"""
    
    r = redis.from_url(os.getenv('REDIS_URL'))
    
    # Get memory info
    info = r.info('memory')
    print(f"📊 Redis memory usage: {info['used_memory_human']}")
    print(f"📊 Peak memory: {info['used_memory_peak_human']}")
    
    # Clean expired keys
    expired_count = r.eval("return #redis.call('keys', 'celery*')", 0)
    print(f"🧹 Found {expired_count} Celery keys")
    
    # Set memory policy if not set
    try:
        r.config_set('maxmemory-policy', 'allkeys-lru')
        print("✅ Set Redis memory policy to allkeys-lru")
    except Exception as e:
        print(f"⚠️  Could not set memory policy: {e}")

if __name__ == "__main__":
    optimize_redis()
