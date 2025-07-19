from celery import Celery
from kombu import Queue
import os

app = Celery('worker',
             broker=os.getenv('REDIS_URL', 'redis://redis:6379/0'),
             backend=os.getenv('REDIS_URL', 'redis://redis:6379/0'),
             include=['worker.tasks'])

# Configure task queues
app.conf.task_queues = (
    Queue('default', routing_key='task.default'),
    Queue('matching', routing_key='task.matching'),
)

app.conf.task_routes = {
    'worker.tasks.run_property_matching': {'queue': 'matching'},
}

# Optional configuration
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_max_tasks_per_child=100,
    worker_prefetch_multiplier=1,
)

if __name__ == '__main__':
    app.start()