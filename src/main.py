from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import schemas, crud, models


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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
    db_user = crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    return crud.create_user(db=db, user=user)

@app.get(path='/users/', response_model=list[schemas.User])
def read_users(
    skip: int=0, limit: int=100, db: Session=Depends(get_db)
) -> list[schemas.User]:
    db_users = crud.get_users(db=db, skip=skip, limit=limit)
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
