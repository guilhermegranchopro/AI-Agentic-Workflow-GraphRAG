import time
import asyncio
from typing import Dict, Optional
from dataclasses import dataclass
from loguru import logger


@dataclass
class TokenBucket:
    """Token bucket for rate limiting."""
    capacity: int
    tokens: int
    last_refill: float
    refill_rate: float  # tokens per second


class RateLimiter:
    """Rate limiter using token bucket algorithm."""
    
    def __init__(self, requests_per_window: int, window_seconds: int):
        """Initialize rate limiter."""
        self.requests_per_window = requests_per_window
        self.window_seconds = window_seconds
        self.refill_rate = requests_per_window / window_seconds
        self.buckets: Dict[str, TokenBucket] = {}
        self.cleanup_task: Optional[asyncio.Task] = None
        
    def _get_bucket(self, key: str) -> TokenBucket:
        """Get or create token bucket for a key."""
        now = time.time()
        
        if key not in self.buckets:
            self.buckets[key] = TokenBucket(
                capacity=self.requests_per_window,
                tokens=self.requests_per_window,
                last_refill=now,
                refill_rate=self.refill_rate
            )
            return self.buckets[key]
            
        bucket = self.buckets[key]
        
        # Refill tokens
        time_passed = now - bucket.last_refill
        tokens_to_add = time_passed * bucket.refill_rate
        bucket.tokens = min(bucket.capacity, bucket.tokens + tokens_to_add)
        bucket.last_refill = now
        
        return bucket
        
    def is_allowed(self, key: str) -> bool:
        """Check if request is allowed."""
        bucket = self._get_bucket(key)
        if bucket.tokens >= 1:
            bucket.tokens -= 1
            return True
        return False
        
    def get_remaining_tokens(self, key: str) -> int:
        """Get remaining tokens for a key."""
        bucket = self._get_bucket(key)
        return max(0, int(bucket.tokens))
        
    def reset_bucket(self, key: str):
        """Reset bucket for a key."""
        if key in self.buckets:
            del self.buckets[key]
            
    def start_cleanup(self):
        """Start cleanup task for expired buckets."""
        if self.cleanup_task is None or self.cleanup_task.done():
            self.cleanup_task = asyncio.create_task(self._cleanup_loop())
            
    def stop_cleanup(self):
        """Stop cleanup task."""
        if self.cleanup_task and not self.cleanup_task.done():
            self.cleanup_task.cancel()
            
    async def _cleanup_loop(self):
        """Cleanup loop for expired buckets."""
        while True:
            try:
                await asyncio.sleep(300)  # Cleanup every 5 minutes
                await self._cleanup_expired_buckets()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Rate limiter cleanup error: {e}")
                
    async def _cleanup_expired_buckets(self):
        """Remove expired buckets."""
        now = time.time()
        expired_keys = []
        
        for key, bucket in self.buckets.items():
            # Remove buckets that haven't been used for 2x window duration
            if now - bucket.last_refill > self.window_seconds * 2:
                expired_keys.append(key)
                
        for key in expired_keys:
            del self.buckets[key]
            
        if expired_keys:
            logger.debug(f"Cleaned up {len(expired_keys)} expired rate limit buckets")


# Global rate limiter instance
rate_limiter = RateLimiter(100, 3600)  # 100 requests per hour


def get_client_ip(request) -> str:
    """Get client IP address from request."""
    # Try to get real IP from headers (for proxy scenarios)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
        
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
        
    # Fallback to direct connection
    return request.client.host if request.client else "unknown"


async def check_rate_limit(request) -> bool:
    """Check rate limit for a request."""
    client_ip = get_client_ip(request)
    return rate_limiter.is_allowed(client_ip)


def get_rate_limit_info(request) -> Dict[str, int]:
    """Get rate limit information for a request."""
    client_ip = get_client_ip(request)
    return {
        "remaining": rate_limiter.get_remaining_tokens(client_ip),
        "limit": rate_limiter.requests_per_window,
        "window_seconds": rate_limiter.window_seconds
    }
