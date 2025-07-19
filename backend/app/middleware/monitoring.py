from fastapi import Request
import time

async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Log to Prometheus or similar
    print(f"{request.method} {request.url.path} - {process_time:.2f}s")
    return response
