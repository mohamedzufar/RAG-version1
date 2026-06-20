import redis
import json
import hashlib
from typing import Optional
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class RedisCache:
    def __init__(self):
        try:
            self.client = redis.from_url(settings.REDIS_URL)
            self.client.ping()
            logger.info("Redis connected")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}")
            self.client = None
        
        self.hits = 0
        self.misses = 0
    
    def get_cache_key(self, query: str) -> str:
        return f"rag:{hashlib.md5(query.encode()).hexdigest()}"
    
    def get(self, query: str) -> Optional[dict]:
        if not self.client:
            return None
        
        try:
            key = self.get_cache_key(query)
            data = self.client.get(key)
            
            if data:
                self.hits += 1
                return json.loads(data)
            
            self.misses += 1
            return None
        except Exception as e:
            logger.error(f"Cache get failed: {e}")
            return None
    
    def set(self, query: str, response: dict):
        if not self.client:
            return
        
        try:
            key = self.get_cache_key(query)
            self.client.setex(
                key,
                settings.REDIS_TTL,
                json.dumps(response)
            )
        except Exception as e:
            logger.error(f"Cache set failed: {e}")
    
    def get_hit_rate(self) -> float:
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return self.hits / total
    
    def clear(self, pattern: str = "rag:*"):
        if not self.client:
            return
        
        try:
            keys = self.client.keys(pattern)
            if keys:
                self.client.delete(*keys)
                logger.info(f"Cleared {len(keys)} cache keys")
        except Exception as e:
            logger.error(f"Cache clear failed: {e}")