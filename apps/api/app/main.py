from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.deps import startup as build_state
from app.routes import arena, defend, health, trace
from app.settings import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await build_state()
    yield


app = FastAPI(
    title="TripWire Defense Engine",
    description="Multi-layer prompt injection defense for agentic systems.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tightened per-env at the edge / Front Door
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(defend.router)
app.include_router(trace.router)
app.include_router(arena.router)
