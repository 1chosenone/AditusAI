"""Aditus AI Backend API.

Provides endpoints for candidate resume parsing and management.
"""

import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.routes import candidate
from config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle events.

    Handles startup and shutdown logging for the application.
    """
    logger.info("Starting app...")
    yield
    logger.info("Shutting down app...")


app = FastAPI(title="Aditus AI Backend", lifespan=lifespan)

app.include_router(candidate.router)


@app.get("/")
async def root():
    """Root endpoint returning a welcome message."""
    return {"message": "Welcome to the Aditus AI Backend!"}
