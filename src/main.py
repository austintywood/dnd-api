from fastapi import Depends, FastAPI

from .database import SessionLocal


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
