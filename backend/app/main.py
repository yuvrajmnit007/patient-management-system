from app.models.base import Base
from app.models.user import User
from app.models.patient import Patient
from app.models.doctor import Doctor
from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.patient import router as patient_router
from app.routers.doctor import router as doctor_router
from app.database.database import engine
app=FastAPI()


Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
app.include_router(patient_router)
app.include_router(doctor_router)

@app.get("/")
async def home():
    return {"message": "backend is running"}

