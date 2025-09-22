from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "mysql+pymysql://root:Kaif%40mysql22-26@localhost:3306/mydb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: db.close()

# JWT

SECRET_KEY = "fat_cat123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30