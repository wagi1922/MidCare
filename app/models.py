# app/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, DateTime # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy.orm import relationship # type: ignore
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))
    role = Column(String(10), default='user') # 'user' atau 'admin'

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)
    description = Column(String(255), nullable=True)

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    text = Column(String(500))
    weight = Column(Integer, default=1)
    
    category = relationship("Category") # Relasi ke Category
    
class TestResult(Base):
    __tablename__ = "test_results"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.utcnow)
    total_score = Column(Float) # Rata-rata persentase
    raw_answers = Column(JSON)
    conclusion = Column(String(500))