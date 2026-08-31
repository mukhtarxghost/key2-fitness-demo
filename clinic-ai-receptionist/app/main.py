"""
Key 2 Fitness — AI Receptionist Backend
========================================

FastAPI application for the WhatsApp-based AI receptionist.
"""

from fastapi import FastAPI

from app.database.database import Base, engine
from app.models.lead import Lead

from app.routes import (
    health,
    conversations,
    leads,
    business,
    webhook,
)

app = FastAPI(
    title="Key 2 Fitness AI Receptionist",
    description=(
        "Backend API for the Key 2 Fitness WhatsApp AI receptionist. "
        "Handles conversations, lead capture, and webhook integration."
    ),
    version="1.0.0",
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(health.router)
app.include_router(conversations.router)
app.include_router(leads.router)
app.include_router(business.router)
app.include_router(webhook.router)
