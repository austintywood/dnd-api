from pydantic import BaseModel


class CharacterBase(BaseModel):
    name: str
    age: int | None = None
