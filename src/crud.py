from sqlalchemy.orm import Session

from . import models, schemas


def get_user(
    db: Session,
    user_id: int,
) -> schemas.User:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(
    db: Session,
    email: str | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[schemas.User]:
    query = db.query(models.User)

    if email:
        query = query.filter(models.User.email == email)

    db_users = query.offset(skip).limit(limit).all()
    return db_users

def create_user(
    db: Session, user: schemas.User
) -> schemas.User:
    fake_hashed_password = f"{user.password}not_really_hashed"
    db_user = models.User(
        email=user.email,
        hashed_password=fake_hashed_password,
    )
    try:
        db.add(db_user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

    db.refresh(db_user)
    return db_user

def delete_user(
    db: Session, user_id: int
) -> schemas.User:
    db_user = get_user(db, user_id=user_id)
    try:
        db.delete(db_user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

    return db_user

def get_characters(
    db: Session,
    name: str | None = None,
    age: int | None = None,
    skip: int=0,
    limit: int=100,
) -> list[schemas.Character]:
    query = db.query(models.Character)
    if name:
        query = query.filter(models.Character.name == name)
    if age:
        query = query.filter(models.Character.age == age)

    return query.offset(skip).limit(limit).all()

def get_character(
    db: Session, character_id: int
) -> schemas.Character:
    return (
        db.query(models.Character)
        .filter(models.Character.id == character_id)
        .first()
    )

def update_character(
    db: Session,
    db_character: models.Character,
    character_update: dict,
) -> schemas.Character:
    for k, v in character_update.items():
        setattr(db_character, k, v)

    try:
        db.commit()
        db.refresh(db_character)
    except Exception as e:
        raise e

    return db_character