import os
import dotenv
from sqlalchemy import create_engine
from sqlalchemy import URL

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
