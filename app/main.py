from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import create_indexes
from app.routes import auth, users, records, dashboard, jokes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_indexes()
    yield
    # Shutdown (reserved)


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan
)

# CORS for deployment (frontend can connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # production me frontend domain lagao
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(records.router)
app.include_router(dashboard.router)
app.include_router(jokes.router)


@app.get("/", tags=["default"])
def health_check():
    return {
        "message": "Finance Dashboard Backend is running",
        "docs": "/docs",
        "version": "0.1.0"
    }
