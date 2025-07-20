# backend/app/performance.py
from functools import wraps
import time
import logging

logger = logging.getLogger(__name__)

def monitor_performance(func):
    """Decorator to monitor function performance"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            
            if duration > 1.0:  # Log slow operations
                logger.warning(f"Slow operation: {func.__name__} took {duration:.2f}s")
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Operation failed: {func.__name__} after {duration:.2f}s: {e}")
            raise
    
    return wrapper
