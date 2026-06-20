import time
from collections import deque
from typing import Dict, List
import statistics
from app.config import settings

class MetricsTracker:
    def __init__(self):
        self.query_latencies = deque(maxlen=1000)
        self.query_confidences = deque(maxlen=1000)
        self.cache_hits = 0
        self.cache_misses = 0
        self.total_queries = 0
        self.total_cost = 0.0
    
    def record_query(self, latency_ms: float, confidence: float, cached: bool = False):
        self.query_latencies.append(latency_ms)
        self.query_confidences.append(confidence)
        self.total_queries += 1
        self.total_cost += settings.COST_PER_QUERY
        
        if cached:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
    
    def get_metrics(self) -> Dict:
        latencies = list(self.query_latencies)
        
        return {
            "total_queries": self.total_queries,
            "avg_latency_ms": statistics.mean(latencies) if latencies else 0,
            "p95_latency_ms": self._percentile(latencies, 95) if latencies else 0,
            "cache_hit_rate": (
                self.cache_hits / (self.cache_hits + self.cache_misses)
                if (self.cache_hits + self.cache_misses) > 0 else 0
            ),
            "avg_confidence": statistics.mean(self.query_confidences) if self.query_confidences else 0,
            "total_cost": self.total_cost
        }
    
    def _percentile(self, data: List[float], percentile: int) -> float:
        if not data:
            return 0.0
        
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        return sorted_data[min(index, len(sorted_data)-1)]