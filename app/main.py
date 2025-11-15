# app/main.py
from fastapi import FastAPI # type: ignore
from .database import Base, engine 
from .auth import auth_router # type: ignore
from .routers.admin import admin_router 
from .routers.user import user_router 

# Inisialisasi Aplikasi dengan Metadata Tambahan
app = FastAPI(
    title="MidCare API", # Judul yang lebih jelas
    description="API Backend untuk Expert System Tes Psikologis dengan Otentikasi dan CRUD Admin.",
    version="1.0.0", # Versi API
    # Anda juga bisa menambahkan kontak, lisensi, dll.
)

# Buat semua tabel di database (Jalankan sekali di awal)
Base.metadata.create_all(bind=engine)

# Daftarkan Routers
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(user_router)