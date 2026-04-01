from fastapi import APIRouter, Depends
from app.schemas.joke import JokeResponse
from app.services.joke_service import fetch_random_joke
from app.utils.dependencies import require_roles

router = APIRouter(prefix="/jokes", tags=["Jokes"])


@router.get("/random", response_model=JokeResponse)
def random_joke(_current_user=Depends(require_roles(["viewer", "analyst", "admin"]))):
    return fetch_random_joke()