# scripts/monitor_api_performance.py
import requests
import time
import statistics
import os

def test_api_performance(base_url, endpoints, num_tests=10):
    """Test API endpoint performance"""
    
    results = {}
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        response_times = []
        
        print(f"🔍 Testing {endpoint}...")
        
        for i in range(num_tests):
            start_time = time.time()
            try:
                response = requests.get(url, timeout=10)
                end_time = time.time()
                
                if response.status_code == 200:
                    response_time = (end_time - start_time) * 1000  # Convert to ms
                    response_times.append(response_time)
                else:
                    print(f"❌ {endpoint} returned {response.status_code}")
                    
            except Exception as e:
                print(f"❌ {endpoint} failed: {e}")
        
        if response_times:
            avg_time = statistics.mean(response_times)
            median_time = statistics.median(response_times)
            max_time = max(response_times)
            
            results[endpoint] = {
                'avg': avg_time,
                'median': median_time,
                'max': max_time,
                'samples': len(response_times)
            }
            
            print(f"✅ {endpoint}:")
            print(f"   Average: {avg_time:.2f}ms")
            print(f"   Median: {median_time:.2f}ms") 
            print(f"   Max: {max_time:.2f}ms")
            
            if avg_time > 1000:
                print(f"⚠️  {endpoint} is slow (>1s average)")
    
    return results

if __name__ == "__main__":
    backend_url = os.getenv('BACKEND_URL', 'https://realestate-backend-production.up.railway.app')
    
    endpoints = [
        "/health",
        "/api/v1/dashboard/stats",
        "/"
    ]
    
    test_api_performance(backend_url, endpoints)