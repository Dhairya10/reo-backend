import os
from fastapi import FastAPI
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from routers import videos, keywords
from supabase import create_client
from utils.middleware import RateLimitMiddleware
from config.logger import logger
from config.settings import RATE_LIMIT_DURATION, RATE_LIMIT_MAX_REQUESTS

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.supabase = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )
    logger.info("Supabase client initialized")
    yield
    logger.info("Shutting down")

app = FastAPI(
    title="Reo API",
    description="API for managing reo app",
    version="1.0.0",
    lifespan=lifespan
)

# Include the routers
app.include_router(videos.router)
app.include_router(keywords.router)

# Add middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Apply rate limiting only to stories routes
app.add_middleware(
    RateLimitMiddleware,
    rate_limit_duration=RATE_LIMIT_DURATION,  # 1 minute
    max_requests=RATE_LIMIT_MAX_REQUESTS,  # 10 requests per minute
    include_paths=["/stories"]  # Apply only to paths starting with /stories
)

logger.info("Application startup complete")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)