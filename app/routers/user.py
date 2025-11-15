# app/routers/user.py
from fastapi import APIRouter, Depends, HTTPException, status # type: ignore
from sqlalchemy.orm import Session # type: ignore
from typing import List
from ..database import get_db
from ..auth import get_current_normal_user  # type: ignore
from .. import crud, schemas, models
from ..expert_system import ExpertSystem 

user_router = APIRouter(prefix="/api/user", tags=["User - Testing"])
USER_ACCESS = Depends(get_current_normal_user)

# Inisialisasi ES (Asumsi rules dimuat saat aplikasi berjalan)
ES_RULES = [] # Placeholder
es = ExpertSystem(ES_RULES)

# Endpoint 1: Mendapatkan Pertanyaan
@user_router.get("/test/questions", response_model=List[schemas.QuestionRead])
def get_test_questions(db: Session = Depends(get_db), current_user: dict = USER_ACCESS):
    questions = crud.get_questions(db)
    if not questions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tidak ada pertanyaan yang tersedia.")
    return questions

# Endpoint 2: Pengiriman Tes Psikologis (Core Logic)
@user_router.post("/test/submit", response_model=schemas.ResultOutput)
async def submit_test(
    test_data: schemas.TestSubmit, 
    db: Session = Depends(get_db),
    current_user: dict = USER_ACCESS
):
    user_id = current_user["user_id"]
    
    questions_map, categories_map = crud.get_all_test_data(db)
    
    if not questions_map or not categories_map:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Data tes belum lengkap.")

    # Hitung Skor dan Inferensi
    raw_answers_data = [a.dict() for a in test_data.answers]
    final_scores_percentage = es.calculate_score(raw_answers_data, questions_map)
    conclusion = es.infer_conclusion(final_scores_percentage, categories_map)
    
    avg_score = sum(final_scores_percentage.values()) / len(final_scores_percentage) if final_scores_percentage else 0

    # Simpan Hasil
    result_to_save = {
        "user_id": user_id,
        "total_score": avg_score,
        "raw_answers": raw_answers_data,
        "conclusion": conclusion
    }
    db_result = crud.create_test_result(db, schemas.ResultCreate(**result_to_save))

    return db_result

# Endpoint 3: Histori Hasil Tes
@user_router.get("/results", response_model=List[schemas.ResultOutput])
def get_user_results(db: Session = Depends(get_db), current_user: dict = USER_ACCESS):
    user_id = current_user["user_id"]
    results = crud.get_user_test_results(db, user_id)
    return results