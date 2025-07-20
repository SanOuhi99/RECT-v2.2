# scripts/cleanup_logs.py
import os
import gzip
import shutil
from datetime import datetime, timedelta

def cleanup_logs(log_dir="/var/log", days_to_keep=30):
    """Clean up old log files"""
    
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    
    for root, dirs, files in os.walk(log_dir):
        for file in files:
            if file.endswith('.log'):
                file_path = os.path.join(root, file)
                
                # Get file modification time
                mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                if mod_time < cutoff_date:
                    # Compress before deletion
                    compressed_path = f"{file_path}.gz"
                    with open(file_path, 'rb') as f_in:
                        with gzip.open(compressed_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    
                    os.remove(file_path)
                    print(f"🗑️  Compressed and removed: {file}")

if __name__ == "__main__":
    cleanup_logs()
