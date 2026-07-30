from app.models.base import Base
from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.patient import router as patient_router
from app.database.database import engine
app=FastAPI()


Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
app.include_router(patient_router)

@app.get("/")
async def home():
    return {"message": "backend is running"}

