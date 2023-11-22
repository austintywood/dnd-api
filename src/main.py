from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import schemas, crud, models


# models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get to the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
async def root():
    return {'message': 'RealmRoster API'}

@app.post(path='/users/', response_model=schemas.User)
def create_user(
    user: schemas.UserCreate, db: Session=Depends(get_db)
) -> schemas.User:
    try:
        db_user = crud.create_user(db=db, user=user)
    except IntegrityError as e:
        raise HTTPException(
            status_code=400,
            detail='Email already registered',
        )

    return db_user

@app.get(path='/users/', response_model=list[schemas.User])
def read_users(
    email: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> list[schemas.User]:
    db_users = crud.get_user_from_params(
        db=db, email=email, skip=skip, limit=limit
    )
    return db_users

@app.get(path='/users/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session=Depends(get_db)) -> schemas.User:
    db_user = crud.get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status=404, detail='User not found.')
    return db_user

@app.delete(path='/users/{user_id}', response_model=schemas.User)
def delete_user(user_id: int, db: Session=Depends(get_db)) -> schemas.User:
    db_user = crud.get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status=404, detail='User not found.')
    try:
        db.delete(db_user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    return db_user

@app.post('/characters/', response_model=schemas.Character)
def create_character(
    character: schemas.CharacterCreate, db: Session = Depends(get_db)
):
    db_character = models.Character(**character.model_dump())
    try:
        db.add(db_character)
        db.commit()
        db.refresh(db_character)
    except Exception as e:
        db.rollback()
        raise e
    return db_character

@app.get(path='/characters/')
def read_character_class(
    character_class_name: schemas.CharacterClassName | None = None,
) -> schemas.CharacterClassName:
    return character_class_name
