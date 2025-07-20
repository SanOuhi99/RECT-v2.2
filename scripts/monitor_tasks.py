# scripts/monitor_tasks.py
from celery import Celery
import os
import json

app = Celery('worker', broker=os.getenv('REDIS_URL'))

def monitor_tasks():
    """Monitor Celery task status"""
    
    # Get active tasks
    active = app.control.inspect().active()
    scheduled = app.control.inspect().scheduled()
    stats = app.control.inspect().stats()
    
    print("📋 Celery Worker Status")
    print("=" * 50)
    
    if active:
        print(f"🔄 Active tasks: {len(list(active.values())[0])}")
        for worker, tasks in active.items():
            print(f"Worker {worker}: {len(tasks)} active tasks")
    else:
        print("✅ No active tasks")
    
    if scheduled:
        print(f"⏰ Scheduled tasks: {len(list(scheduled.values())[0])}")
    
    if stats:
        for worker, stat in stats.items():
            print(f"📊 {worker} stats:")
            print(f"  - Total tasks: {stat.get('total', 0)}")
            print(f"  - Pool: {stat.get('pool', 'N/A')}")

if __name__ == "__main__":
    monitor_tasks()