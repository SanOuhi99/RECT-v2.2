# scripts/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    KV_CORE_API_KEY = os.getenv("KV_CORE_API_KEY")
    MATCHING_THRESHOLD = float(os.getenv("MATCHING_THRESHOLD", 0.8))
    CACHE_EXPIRATION = int(os.getenv("CACHE_EXPIRATION", 3600))  # 1 hour
    
    @property
    def kv_core_headers(self):
        return {
            "Authorization": f"Bearer {self.KV_CORE_API_KEY}",
            "Content-Type": "application/json"
        }