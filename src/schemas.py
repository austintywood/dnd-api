from pydantic import BaseModel



class CharacterBase(BaseModel):
    name: str
    age: int | None = None

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class UserDelete(User):
    pass
