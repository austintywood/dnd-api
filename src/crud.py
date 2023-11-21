from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int) -> schemas.User:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> schemas.User:
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int=0, limit: int=100) -> list[schemas.User]:
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.User) -> schemas.User:
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

def delete_user(db: Session, user_id: int) -> schemas.User:
    db_user = get_user(db, user_id=user_id)
    try:
        db.delete(db_user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

    return db_user
