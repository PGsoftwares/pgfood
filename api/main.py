"""PG Partner App API - FastAPI Application

Comprehensive API backend implementing all 13 sections of the PG Partner App documentation:
1. Auth & Password Reset
2. Partner Onboarding & Registration
3. Dashboard & Outlet Availability
4. Orders Management Pipeline
5. Food Menu & Customizations
6. Offers & Discounts
7. Restaurant Timing & Working Hours
8. Financials, Earnings & Settlements
9. Customer Reviews & Ratings
10. Notifications
11. Restaurant & Owner Profile
12. Help & Support Tickets
13. Settings & Security
"""

import os
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Ensure Django is initialized
import api  # triggers django.setup() in api/__init__.py

from api.routers import (
    auth,
    registration,
    dashboard,
    orders,
    menu,
    offers,
    timings,
    earnings,
    reviews,
    notifications,
    profile,
    support,
    settings,
)

app = FastAPI(
    title="PG Partner App API",
    version="1.0.0",
    description=(
        "Production-grade FastAPI backend for PG Food Delivery Partner App & Merchant Portal. "
        "Supports all 13 partner operational sections with PostgreSQL integration and JWT authentication."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Enable CORS for cross-origin mobile app and frontend web requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# V1 API Router (Standard prefix per documentation: https://api.pgpartner.com/v1)
v1_router = APIRouter(prefix="/v1")

routers = [
    auth.router,
    registration.router,
    dashboard.router,
    orders.router,
    menu.router,
    offers.router,
    timings.router,
    earnings.router,
    reviews.router,
    notifications.router,
    profile.router,
    support.router,
    settings.router,
]

for r in routers:
    v1_router.include_router(r)
    # Also mount directly on app for clients requesting /orders, /menu, etc.
    app.include_router(r)

app.include_router(v1_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "status": "online",
        "service": "PG Partner App API",
        "version": "1.0.0",
        "docsUrl": "/docs",
        "redocUrl": "/redoc",
        "endpointsPrefix": "/v1",
        "message": "Welcome to PG Partner App API Backend. Visit /docs for the interactive Swagger documentation.",
    }


@app.get("/health", tags=["Root"])
def health():
    return {"status": "healthy"}
