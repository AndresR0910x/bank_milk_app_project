from fastapi import HTTPException
from datetime import datetime, timedelta
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
    
    def check_rate_limit(self, key: str):
        now = time.time()
        window_start = now - self.window_seconds
        
        # Clean old requests
        self.requests[key] = [req_time for req_time in self.requests[key] 
                            if req_time > window_start]
        
        if len(self.requests[key]) >= self.max_requests:
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later."
            )
        
        self.requests[key].append(now)

password_reset_limiter = RateLimiter(max_requests=3, window_seconds=3600)  # 3 requests per hour