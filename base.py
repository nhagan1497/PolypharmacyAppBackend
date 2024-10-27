from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import os
from tenacity import retry, stop_after_attempt, wait_exponential
from time import sleep

SQLALCHEMY_DATABASE_URL = os.getenv("SQL_CONNECTION_STRING")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@retry(stop=stop_after_attempt(10), wait=wait_exponential(multiplier=1, min=5, max=60))
def initialize_database():
    if 'sqlite' in os.environ.get('SQL_CONNECTION_STRING'):
        db_path = os.environ.get('SQL_CONNECTION_STRING').replace('sqlite:///', '')
        if not os.path.exists(db_path):
            open(db_path, 'a').close()
    Base.metadata.create_all(bind=engine)


def get_db():
    @retry(stop=stop_after_attempt(10), wait=wait_exponential(multiplier=1, min=5, max=60))
    def _get_db():
        return SessionLocal()
    db = _get_db()
    try:
        yield db
    finally:
        db.close()


def db_heartbeat_task():
    try:
        # Perform a lightweight query to keep the connection alive
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
        print("Database ping successful.")
    except Exception as e:
        print(f"Database ping failed: {e}")
    sleep(5)
