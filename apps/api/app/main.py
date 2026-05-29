from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import arena, defend, health, trace
from app.settings import get_settings

settings = get_settings()

app = FastAPI(
    title="TripWire Defense Engine",
    description="Multi-layer prompt injection defense for agentic systems.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.environment == "local" else ["https://tripwire-arena.azurewebsites.net"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(defend.router)
app.include_router(trace.router)
app.include_router(arena.router)
