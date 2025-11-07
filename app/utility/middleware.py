import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log request
        logger.info(f"Request started: {request.method} {request.url.path}")

        # Process request
        response = await call_next(request)

        # Calculate latency
        process_time = time.time() - start_time

        # Log response with latency
        logger.info(
            f"Request completed: {request.method} {request.url.path} | "
            f"Status: {response.status_code} | "
            f"Latency: {process_time:.4f}s"
        )

        # Add latency header
        response.headers["X-Process-Time"] = str(process_time)

        return response

