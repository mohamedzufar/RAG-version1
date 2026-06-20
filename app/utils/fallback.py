import time
from functools import wraps
from typing import Any, Callable
import logging

logger = logging.getLogger(__name__)

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_time: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.failures = 0
        self.last_failure_time = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.state == "OPEN":
                if time.time() - self.last_failure_time > self.recovery_time:
                    self.state = "HALF_OPEN"
                    logger.info("Circuit half-open, testing")
                else:
                    return {
                        "error": "Circuit breaker is OPEN",
                        "fallback": True,
                        "answer": "Service temporarily unavailable. Please try again in a moment."
                    }
            
            try:
                result = func(*args, **kwargs)
                if self.state == "HALF_OPEN":
                    self.state = "CLOSED"
                    self.failures = 0
                    logger.info("Circuit closed, service recovered")
                return result
            
            except Exception as e:
                self.failures += 1
                self.last_failure_time = time.time()
                logger.error(f"Function failed: {e}")
                
                if self.failures >= self.failure_threshold:
                    self.state = "OPEN"
                    logger.warning(f"Circuit OPEN after {self.failures} failures")
                
                return {
                    "error": str(e),
                    "fallback": True,
                    "answer": "I encountered an error. Please try again."
                }
        
        return wrapper