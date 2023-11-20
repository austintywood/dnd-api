import os
import dotenv
from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

dotenv.load_dotenv()

db_url = URL.create(
    drivername='postgresql',
    username=os.getenv('DATABASE_USERNAME'),
    password=os.getenv('DATABASE_PASSWORD'),
    host=os.getenv('DATABASE_HOST'),
    port=os.getenv('DATABASE_PORT'),
    database=os.getenv('DATABASE_NAME'),
)
engine = create_engine(db_url)

SessionLocal: Session = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base = declarative_base()
