from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
import time
from config.logger import logger

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, 
        app,
        rate_limit_duration: int = 60,  # Duration in seconds
        max_requests: int = 5,  # Max requests per duration
        include_paths: list = None  # List of paths to apply rate limiting
    ):
        super().__init__(app)
        self.rate_limit_duration = rate_limit_duration
        self.max_requests = max_requests
        self.include_paths = include_paths or []
        self.request_counts = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if not self.include_paths or any(path.startswith(p) for p in self.include_paths):
            client_ip = request.client.host
            current_time = time.time()

            # Remove old timestamps
            self.request_counts[client_ip] = [ts for ts in self.request_counts[client_ip] if current_time - ts < self.rate_limit_duration]

            if len(self.request_counts[client_ip]) >= self.max_requests:
                logger.warning(f"Rate limit exceeded for IP {client_ip} on path {path}")
                raise HTTPException(status_code=429, detail="Rate limit exceeded")

            self.request_counts[client_ip].append(current_time)

        response = await call_next(request)
        return response