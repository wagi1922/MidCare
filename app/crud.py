# app/crud.py
from sqlalchemy.orm import Session, joinedload # type: ignore
from typing import List, Dict, Optional, Tuple, Any
from . import models, schemas

# --- CRUD Kategori ---
def create_category(db: Session, category: schemas.CategoryCreate) -> models.Category:
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[models.Category]:
    return db.query(models.Category).offset(skip).limit(limit).all()

# --- CRUD Pertanyaan ---
def get_questions(db: Session, skip: int = 0, limit: int = 100) -> List[models.Question]:
    return db.query(models.Question).options(
        joinedload(models.Question.category)
    ).offset(skip).limit(limit).all()

def create_question(db: Session, question: schemas.QuestionCreate) -> models.Question:
    db_question = models.Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def update_question(db: Session, question_id: int, question_data: schemas.QuestionCreate) -> Optional[models.Question]:
    db_question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if db_question:
        for key, value in question_data.dict().items():
            setattr(db_question, key, value)
        db.commit()
        db.refresh(db_question)
        return db_question
    return None

def delete_question(db: Session, question_id: int) -> bool:
    db_question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if db_question:
        db.delete(db_question)
        db.commit()
        return True
    return False

# --- FUNGSI PENDUKUNG USER/ES ---

def get_all_test_data(db: Session) -> Tuple[Dict[int, Dict[str, Any]], Dict[int, str]]:
    """Mengambil data Pertanyaan dan Kategori untuk Mesin Inferensi."""
    questions = db.query(models.Question).all()
    categories = db.query(models.Category).all()
    
    questions_map = {
        q.id: {'category_id': q.category_id, 'weight': q.weight} 
        for q in questions
    }
    categories_map = {c.id: c.name for c in categories}
    
    return questions_map, categories_map # type: ignore

def create_test_result(db: Session, result_data: schemas.ResultCreate) -> models.TestResult:
    """Menyimpan hasil tes ke database."""
    db_result = models.TestResult(**result_data.dict())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

def get_user_test_results(db: Session, user_id: int) -> List[models.TestResult]:
    """Mengambil riwayat hasil tes user."""
    return db.query(models.TestResult)\
        .filter(models.TestResult.user_id == user_id)\
        .order_by(models.TestResult.date.desc())\
        .all()