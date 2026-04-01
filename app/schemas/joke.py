from pydantic import BaseModel


class JokeResponse(BaseModel):
    id: int | None = None
    type: str | None = None
    setup: str
    punchline: str
    source: str