from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings

# url connnection string for postgres database
# SQLALQUEMY_DATABASE_URL = "postgresql://[user]:[password]@[host]:[port]/[database_name]"
SQLALQUEMY_DATABASE_URL = settings.SQLALQUEMY_DATABASE_URL
engine = create_engine(SQLALQUEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()