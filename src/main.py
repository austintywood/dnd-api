from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.exc import IntegrityError, DataError
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

@app.get(path='/users/', response_model=dict[str, list[schemas.User]])
def read_users(
    email: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> dict[str, list[schemas.User]]:
    db_users = crud.get_users(db=db, email=email, skip=skip, limit=limit)
    return {'users': db_users}

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
) -> schemas.Character:
    db_character = models.Character(**character.model_dump())
    try:
        db.add(db_character)
        db.commit()
        db.refresh(db_character)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail='Character name is taken'
        )
    except Exception as e:
        db.rollback()
        raise e
    return db_character

@app.get(
    path='/characters/',
    response_model=dict[str, list[schemas.Character]],
)
def read_characters(
    name: str | None = Query(None, alias='name'),
    race: schemas.Race | None = Query(None, alias='race'),
    skip: int = Query(0, alias='skip'),
    limit: int = Query(100, alias='limit'),
    db: Session = Depends(get_db),
) -> dict[str, list[schemas.Character]]:
    db_characters = crud.get_characters(
        db=db,
        name=name,
        race=race,
        skip=skip,
        limit=limit,
    )
    return {'characters': db_characters}

@app.get(path='/characters/{character_id}', response_model=schemas.Character)
def read_character(
    character_id: int,
    db: Session=Depends(get_db)
) -> schemas.Character:
    db_character = crud.get_character(db=db, character_id=character_id)
    if not db_character:
        raise HTTPException(
            status_code=404,
            detail='Character not found',
        )
    return db_character

@app.put(path='/characters/{character_id}', response_model=schemas.Character)
def update_character(
    character_id: int,
    character_update: dict,
    db: Session = Depends(get_db)
) -> schemas.Character:
    db_character = crud.get_character(db=db, character_id=character_id)
    if not db_character:
        raise HTTPException(
            status_code=404,
            detail='Charater not found'
        )

    try:
        db_character = crud.update_character(
            db, db_character, character_update
        )
    except DataError as e:
        raise HTTPException(
            status_code=422,
            detail='Invalid data input.'
        )
    except Exception as e:
        raise e

    return db_character

@app.delete(
    path='/characters/{character_id}',
    response_model=dict[str, schemas.Character]
)
def delete_character(
    character_id: int,
    db: Session = Depends(get_db),
) -> dict[str, schemas.Character]:
    db_character = crud.get_character(db=db, character_id=character_id)
    if not db_character:
        raise HTTPException(
            status_code=404,
            detail='Character not found.'
        )

    crud.delete_character(db=db, db_character=db_character)
    return {'deleted': db_character}
