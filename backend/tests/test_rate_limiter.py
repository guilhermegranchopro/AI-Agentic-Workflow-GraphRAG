"""
Tests for rate limiter functionality.
"""

import pytest
import asyncio
import time
from unittest.mock import Mock, patch
from app.utils.rate_limiter import RateLimiter


@pytest.fixture
def rate_limiter():
    """Create rate limiter instance."""
    return RateLimiter(max_requests=10, time_window=60)


@pytest.fixture
def fast_rate_limiter():
    """Create rate limiter with fast time window for testing."""
    return RateLimiter(max_requests=5, time_window=1)


class TestRateLimiter:
    """Test rate limiter functionality."""

    def test_rate_limiter_initialization(self):
        """Test rate limiter initialization."""
        limiter = RateLimiter(max_requests=10, time_window=60)
        assert limiter.max_requests == 10
        assert limiter.time_window == 60
        assert len(limiter.requests) == 0

    def test_rate_limiter_default_values(self):
        """Test rate limiter with default values."""
        limiter = RateLimiter()
        assert limiter.max_requests == 100
        assert limiter.time_window == 60

    def test_is_allowed_with_no_requests(self, rate_limiter):
        """Test is_allowed when no requests have been made."""
        assert rate_limiter.is_allowed() is True

    def test_is_allowed_within_limit(self, rate_limiter):
        """Test is_allowed when within request limit."""
        # Add some requests
        for i in range(5):
            rate_limiter.requests.append(time.time())
        
        assert rate_limiter.is_allowed() is True

    def test_is_allowed_at_limit(self, rate_limiter):
        """Test is_allowed when at request limit."""
        # Add requests up to the limit
        for i in range(10):
            rate_limiter.requests.append(time.time())
        
        assert rate_limiter.is_allowed() is False

    def test_is_allowed_over_limit(self, rate_limiter):
        """Test is_allowed when over request limit."""
        # Add more requests than the limit
        for i in range(15):
            rate_limiter.requests.append(time.time())
        
        assert rate_limiter.is_allowed() is False

    def test_cleanup_old_requests(self, rate_limiter):
        """Test cleanup of old requests outside time window."""
        current_time = time.time()
        
        # Add old requests (outside time window)
        rate_limiter.requests.extend([
            current_time - 70,  # 70 seconds ago
            current_time - 65,  # 65 seconds ago
        ])
        
        # Add recent requests (within time window)
        rate_limiter.requests.extend([
            current_time - 30,  # 30 seconds ago
            current_time - 10,  # 10 seconds ago
        ])
        
        # Should allow new request after cleanup
        assert rate_limiter.is_allowed() is True
        assert len(rate_limiter.requests) == 2  # Only recent requests remain

    def test_add_request(self, rate_limiter):
        """Test adding a new request."""
        initial_count = len(rate_limiter.requests)
        rate_limiter.add_request()
        
        assert len(rate_limiter.requests) == initial_count + 1

    def test_add_request_with_timestamp(self, rate_limiter):
        """Test adding a request with specific timestamp."""
        timestamp = time.time()
        rate_limiter.add_request(timestamp)
        
        assert len(rate_limiter.requests) == 1
        assert rate_limiter.requests[0] == timestamp

    def test_reset(self, rate_limiter):
        """Test resetting the rate limiter."""
        # Add some requests
        for i in range(5):
            rate_limiter.add_request()
        
        assert len(rate_limiter.requests) == 5
        
        # Reset
        rate_limiter.reset()
        assert len(rate_limiter.requests) == 0

    def test_get_current_count(self, rate_limiter):
        """Test getting current request count."""
        assert rate_limiter.get_current_count() == 0
        
        # Add some requests
        for i in range(3):
            rate_limiter.add_request()
        
        assert rate_limiter.get_current_count() == 3

    def test_get_current_count_with_cleanup(self, rate_limiter):
        """Test getting current count with cleanup of old requests."""
        current_time = time.time()
        
        # Add old and recent requests
        rate_limiter.requests.extend([
            current_time - 70,  # Old
            current_time - 30,  # Recent
            current_time - 10,  # Recent
        ])
        
        # Should return only recent requests
        assert rate_limiter.get_current_count() == 2

    def test_get_remaining_requests(self, rate_limiter):
        """Test getting remaining requests."""
        assert rate_limiter.get_remaining_requests() == 10
        
        # Add some requests
        for i in range(3):
            rate_limiter.add_request()
        
        assert rate_limiter.get_remaining_requests() == 7

    def test_get_remaining_requests_zero(self, rate_limiter):
        """Test getting remaining requests when at limit."""
        # Add requests up to the limit
        for i in range(10):
            rate_limiter.add_request()
        
        assert rate_limiter.get_remaining_requests() == 0

    def test_get_remaining_requests_negative(self, rate_limiter):
        """Test getting remaining requests when over limit."""
        # Add more requests than the limit
        for i in range(15):
            rate_limiter.add_request()
        
        assert rate_limiter.get_remaining_requests() == -5

    def test_time_window_expiration(self, fast_rate_limiter):
        """Test that requests expire after time window."""
        # Add requests up to the limit
        for i in range(5):
            fast_rate_limiter.add_request()
        
        # Should be at limit
        assert fast_rate_limiter.is_allowed() is False
        
        # Wait for time window to expire
        time.sleep(1.1)
        
        # Should allow new requests after expiration
        assert fast_rate_limiter.is_allowed() is True

    def test_concurrent_requests(self, rate_limiter):
        """Test handling of concurrent requests."""
        # Simulate concurrent requests
        requests = []
        for i in range(10):
            requests.append(rate_limiter.is_allowed())
            rate_limiter.add_request()
        
        # All should be allowed initially
        assert all(requests) is True
        
        # Next request should be denied
        assert rate_limiter.is_allowed() is False

    def test_edge_case_zero_requests(self):
        """Test rate limiter with zero max requests."""
        limiter = RateLimiter(max_requests=0, time_window=60)
        assert limiter.is_allowed() is False

    def test_edge_case_zero_time_window(self):
        """Test rate limiter with zero time window."""
        limiter = RateLimiter(max_requests=10, time_window=0)
        # Should still work, but all requests would be considered old
        assert limiter.is_allowed() is True

    def test_edge_case_negative_requests(self):
        """Test rate limiter with negative max requests."""
        limiter = RateLimiter(max_requests=-5, time_window=60)
        assert limiter.is_allowed() is False

    def test_edge_case_negative_time_window(self):
        """Test rate limiter with negative time window."""
        limiter = RateLimiter(max_requests=10, time_window=-10)
        # Should still work, but all requests would be considered old
        assert limiter.is_allowed() is True


class TestRateLimiterAsync:
    """Test rate limiter in async context."""

    @pytest.mark.asyncio
    async def test_async_rate_limiting(self, fast_rate_limiter):
        """Test rate limiting in async context."""
        # Add requests up to the limit
        for i in range(5):
            fast_rate_limiter.add_request()
        
        # Should be at limit
        assert fast_rate_limiter.is_allowed() is False
        
        # Wait for time window to expire
        await asyncio.sleep(1.1)
        
        # Should allow new requests after expiration
        assert fast_rate_limiter.is_allowed() is True

    @pytest.mark.asyncio
    async def test_async_concurrent_requests(self, rate_limiter):
        """Test concurrent async requests."""
        async def make_request():
            if rate_limiter.is_allowed():
                rate_limiter.add_request()
                return True
            return False
        
        # Make concurrent requests
        tasks = [make_request() for _ in range(15)]
        results = await asyncio.gather(*tasks)
        
        # First 10 should succeed, rest should fail
        assert sum(results) == 10
        assert results[:10] == [True] * 10
        assert results[10:] == [False] * 5


class TestRateLimiterIntegration:
    """Integration tests for rate limiter."""

    def test_rate_limiter_with_real_time(self):
        """Test rate limiter with real time progression."""
        limiter = RateLimiter(max_requests=3, time_window=2)
        
        # Add 3 requests
        for i in range(3):
            limiter.add_request()
        
        # Should be at limit
        assert limiter.is_allowed() is False
        
        # Wait for expiration
        time.sleep(2.1)
        
        # Should allow new requests
        assert limiter.is_allowed() is True

    def test_rate_limiter_persistence(self):
        """Test that rate limiter maintains state."""
        limiter = RateLimiter(max_requests=5, time_window=10)
        
        # Add some requests
        for i in range(3):
            limiter.add_request()
        
        # Check state
        assert limiter.get_current_count() == 3
        assert limiter.get_remaining_requests() == 2
        
        # Add more requests
        for i in range(2):
            limiter.add_request()
        
        # Should be at limit
        assert limiter.get_current_count() == 5
        assert limiter.get_remaining_requests() == 0
        assert limiter.is_allowed() is False
