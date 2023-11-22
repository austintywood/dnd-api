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

class Race(str, Enum):
    dwarf = 'dwarf'
    elf = 'elf'
    halfling = 'halfling'
    human = 'human'
    dragonborn = 'dragonborn'
    gnome = 'gnome'
    half_elf = 'half_elf'
    half_orc = 'half_orc'
    tiefling = 'tiefling'

    class Config():
        from_attributes = True

class CharacterBase(BaseModel):
    name: str
    age: int | None = None
    race: Race | None = None

class CharacterCreate(CharacterBase):
    pass

class CharacterUpdate(CharacterBase):
    pass

class Character(CharacterBase):
    id: int
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
