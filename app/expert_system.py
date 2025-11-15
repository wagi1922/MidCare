# app/expert_system.py
from typing import List, Dict, Any, Tuple

class ExpertSystem:
    def __init__(self, rules: List[Dict[str, Any]]):
        self.rules = rules # Placeholder untuk aturan kompleks

    def calculate_score(self, answers: List[Dict[str, Any]], questions_map: Dict[int, Dict[str, Any]]) -> Dict[int, float]:
        """Menghitung skor persentase per kategori dari input nilai 1-10."""
        category_scores: Dict[int, float] = {}
        category_max_scores: Dict[int, float] = {}
        
        # Hitung Kontribusi Skor Maksimum
        for q_data in questions_map.values():
            cat_id = q_data['category_id']
            weight = q_data['weight']
            category_max_scores[cat_id] = category_max_scores.get(cat_id, 0.0) + (10 * weight)

        # Hitung Skor Diperoleh
        for answer in answers:
            q_id = answer['question_id']
            if q_id not in questions_map: continue 
            
            q_data = questions_map[q_id]
            cat_id = q_data['category_id']
            weight = q_data['weight']
            value = answer['answer_value']
            
            score_contribution = float(value * weight)
            category_scores[cat_id] = category_scores.get(cat_id, 0.0) + score_contribution

        # Konversi ke Persentase
        final_scores_id: Dict[int, float] = {}
        for cat_id, score in category_scores.items():
            max_score = category_max_scores.get(cat_id, 1.0) 
            percentage = (score / max_score) * 100
            final_scores_id[cat_id] = round(percentage, 2)
            
        return final_scores_id

    def infer_conclusion(self, scores: Dict[int, float], categories: Dict[int, str]) -> str:
        """Menarik kesimpulan berdasarkan skor persentase."""
        interpretations = []
        complex_conclusions = []
        
        # Analisis Dasar
        for cat_id, percentage in scores.items():
            cat_name = categories.get(cat_id, "Unknown")
            level = ""
            if percentage >= 85: level = "Sangat Tinggi"
            elif percentage >= 70: level = "Tinggi"
            elif percentage >= 40: level = "Rata-Rata"
            elif percentage < 40: level = "Rendah"
            interpretations.append(f"Skor {cat_name}: {percentage:.2f}% ({level}).")
            
        # Analisis Kombinasi (Anda perlu menyesuaikan ID Kategori)
        # Contoh: Jika ID 1 adalah Introversion, dan ID 2 adalah Neuroticism
        if scores.get(1, 0) > 75 and scores.get(2, 0) > 70:
            complex_conclusions.append("Profil Anda menunjukkan kecenderungan Cemas-Introvert.")

        header = "--- Kesimpulan Psikologis ---"
        detail = "\n".join(interpretations)
        complex_section = "\n\n--- Analisis Kombinasi ---\n" + ("\n".join(complex_conclusions) if complex_conclusions else "Tidak ditemukan kombinasi profil dominan unik.")
        
        return f"{header}\n{detail}\n{complex_section}"