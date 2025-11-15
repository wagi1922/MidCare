# app/routers/admin.py
from fastapi import APIRouter, Depends, HTTPException, status # type: ignore
from sqlalchemy.orm import Session # type: ignore
from typing import List
from ..database import get_db
from ..auth import get_current_admin # type: ignore
from .. import crud, schemas, models

admin_router = APIRouter(prefix="/api/admin", tags=["Admin - Management"])
ADMIN_ACCESS = Depends(get_current_admin)

# Endpoint Kategori (CRUD)
@admin_router.post("/categories", response_model=schemas.CategoryRead, status_code=status.HTTP_201_CREATED)
def add_category(category: schemas.CategoryCreate, db: Session = Depends(get_db), admin: dict = ADMIN_ACCESS):
    return crud.create_category(db=db, category=category)

@admin_router.get("/categories", response_model=List[schemas.CategoryRead])
def read_categories(db: Session = Depends(get_db), admin: dict = ADMIN_ACCESS):
    return crud.get_categories(db=db)

# Endpoint Pertanyaan (CRUD)
@admin_router.post("/questions", response_model=schemas.QuestionRead, status_code=status.HTTP_201_CREATED)
def add_question(question: schemas.QuestionCreate, db: Session = Depends(get_db), admin: dict = ADMIN_ACCESS):
    category = db.query(models.Category).filter(models.Category.id == question.category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category ID not found")
        
    return crud.create_question(db=db, question=question)

@admin_router.get("/questions", response_model=List[schemas.QuestionRead])
def read_questions(db: Session = Depends(get_db), admin: dict = ADMIN_ACCESS):
    return crud.get_questions(db=db)

@admin_router.put("/questions/{question_id}", response_model=schemas.QuestionRead)
def update_question_endpoint(question_id: int, question_data: schemas.QuestionCreate, db: Session = Depends(get_db), admin: dict = ADMIN_ACCESS):
    updated_q = crud.update_question(db=db, question_id=question_id, question_data=question_data)
    if updated_q is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return updated_q

@admin_router.delete("/questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question_endpoint(question_id: int, db: Session = Depends(get_db), admin: dict = ADMIN_ACCESS):
    success = crud.delete_question(db=db, question_id=question_id)
    if not success:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"ok": True}

# Endpoint Tambahan (Admin - Melihat Hasil User)
@admin_router.get("/users/results", response_model=List[schemas.ResultOutput])
def get_all_user_results(db: Session = Depends(get_db), admin: dict = ADMIN_ACCESS):
    # Mengambil semua hasil tes dari semua pengguna
    return db.query(models.TestResult).order_by(models.TestResult.date.desc()).all()

@admin_router.get("/users", response_model=List[schemas.UserRead]) # Melihat semua user
def get_all_users(db: Session = Depends(get_db), admin: dict = ADMIN_ACCESS):
    return db.query(models.User).all()