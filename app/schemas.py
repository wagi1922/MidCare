# app/schemas.py
from pydantic import BaseModel, field_validator # type: ignore
from typing import List, Optional, Dict, Any
from datetime import datetime

# --- Otentikasi & User ---
class TokenRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

class UserCreate(BaseModel):
    username: str
    password: str

    # --- TAMBAHKAN VALIDASI PANJANG PASSWORD (DISARANKAN) ---
    @field_validator('password')
    @classmethod
    def check_password_length(cls, v):
        # 72 bytes adalah batas atas, 128 karakter ASCII adalah batas aman.
        # Kita batasi hingga 72 karakter (asumsi ASCII/UTF-8 sederhana) untuk menghindari masalah.
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password must not exceed 72 characters.')
        return v

# --- Kategori & Pertanyaan (Admin) ---
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int
    class Config:
        from_attributes = True

class QuestionBase(BaseModel):
    category_id: int
    text: str
    weight: int = 1

class QuestionCreate(QuestionBase):
    pass

class QuestionRead(QuestionBase):
    id: int
    category: CategoryRead
    class Config:
        from_attributes = True

# --- Tes & Hasil (User) ---
class AnswerInput(BaseModel):
    question_id: int
    answer_value: int # Nilai 1-10

class TestSubmit(BaseModel):
    test_id: int = 1 # Hanya 1 tipe tes
    answers: List[AnswerInput]

class ResultCreate(BaseModel):
    user_id: int
    total_score: float
    raw_answers: List[Dict[str, Any]]
    conclusion: str

class ResultOutput(BaseModel):
    id: int
    date: datetime
    total_score: float
    conclusion: str
    class Config:
        from_attributes = True