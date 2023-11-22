from typing import List
from enum import Enum
from pydantic import BaseModel


class CharacterLevelBase(BaseModel):
    level: int

class CharacterLevelCreate(CharacterLevelBase):
    pass

class CharacterLevel(CharacterLevelBase):
    id: int
    character_id: int
    character_class_id: int

    class Config():
        from_attributes = True

class CharacterClassName(str, Enum):
    barbarian = 'barbarian'
    bard = 'bard'
    cleric = 'cleric'
    druid = 'druid'
    fighter = 'fighter'
    monk = 'monk'
    paladin = 'paladin'
    ranger = 'ranger'
    rogue = 'rogue'
    sorcerer = 'sorcerer'
    warlock = 'warlock'
    wizard = 'wizard'

class CharacterClassBase(BaseModel):
    name: CharacterClassName

class CharacterClassCreate(CharacterClassBase):
    pass

class CharacterClass(CharacterClassBase):
    id: int

    class Config():
        from_attributes = True

class CharacterBase(BaseModel):
    name: str

class CharacterCreate(CharacterBase):
    pass

class Character(CharacterBase):
    id: int
    age: int | None = None
    classes: List[CharacterLevel] = []

    class Config():
        from_attributes = True

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
