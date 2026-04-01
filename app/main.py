from fastapi import FastAPI
from app.config import settings
from app.database import create_indexes
from app.routes import auth, users, records, dashboard, jokes

app = FastAPI(title=settings.app_name)


@app.on_event("startup")
def on_startup():
    create_indexes()


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(records.router)
app.include_router(dashboard.router)
app.include_router(jokes.router)


@app.get("/")
def health_check():
    return {"message": "Finance Dashboard Backend is running"}