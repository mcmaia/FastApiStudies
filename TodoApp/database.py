from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

PSQL_PASSWORD=os.getenv("PSQL_PASSWORD")
HOST=os.getenv("HOST")
DATABASE=os.getenv("DATABASE")

SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:{PSQL_PASSWORD}@{HOST}:5432/{DATABASE}'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  

