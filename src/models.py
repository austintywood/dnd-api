from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship

from .database import Base
from .schemas import CharacterClassName, Race


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    characters = relationship('Character', back_populates='owner')

class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    age = Column(Integer, nullable=True)
    race = Column(Enum(Race))
    owner_id = Column(Integer, ForeignKey('users.id'))

    levels = relationship('CharacterLevel', back_populates='character')
    owner = relationship('User', back_populates='characters')

class CharacterClass(Base):
    __tablename__ = 'character_classes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Enum(CharacterClassName), index=True)

    levels = relationship('CharacterLevel', back_populates='character_class')

class CharacterLevel(Base):
    __tablename__ = 'character_levels'

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer)

    character_id = Column(Integer, ForeignKey('characters.id'))
    character = relationship('Character', back_populates='levels')

    character_class_id = Column(Integer, ForeignKey('character_classes.id'))
    character_class = relationship('CharacterClass', back_populates='levels')
