# app/database.py (MODIFIKASI)
import os
from dotenv import load_dotenv # type: ignore
from sqlalchemy import create_engine # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore

# Load environment variables
load_dotenv()
USER = os.getenv("MYSQL_USER")
PASS = os.getenv("MYSQL_PASSWORD")
HOST = os.getenv("MYSQL_HOST")
DB_NAME = os.getenv("MYSQL_DB")

# ---------- PERUBAHAN DI SINI ----------
# Ganti mysql+mysqlclient menjadi mysql+pymysql
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{USER}:{PASS}@{HOST}/{DB_NAME}"
# --------------------------------------

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()