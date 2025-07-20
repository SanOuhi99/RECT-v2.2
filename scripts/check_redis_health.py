# scripts/check_redis_health.py
import redis
import os

def check_redis():
    try:
        r = redis.from_url(os.getenv('REDIS_URL'))
        r.ping()
        info = r.info()
        print(f"✅ Redis healthy: {info['redis_version']}")
        print(f"📊 Memory usage: {info['used_memory_human']}")
        return True
    except Exception as e:
        print(f"❌ Redis error: {e}")
        return False

if __name__ == "__main__":
    check_redis()