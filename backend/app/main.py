from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Model imports required so Base.metadata.create_all sees every table
from app.models.base import Base
from app.models.user import User  # noqa: F401
from app.models.patient import Patient  # noqa: F401
from app.models.doctor import Doctor  # noqa: F401
from app.models.appointment import Appointment  # noqa: F401
from app.models.prescription import Prescription  # noqa: F401
from app.models.prescription_item import PrescriptionItem  # noqa: F401  <-- FIX

from app.config.settings import settings
from app.database.database import engine

from app.routers.auth import router as auth_router
from app.routers.patient import router as patient_router
from app.routers.doctor import router as doctor_router
from app.routers.appointment import router as appointment_router
from app.routers.prescription import router as prescription_router


app = FastAPI(
    title="HMS API",
    version="1.0.0",
    description="Hospital Management System backend",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(patient_router)
app.include_router(doctor_router)
app.include_router(appointment_router)
app.include_router(prescription_router)


@app.get("/", tags=["Health"])
async def home():
    return {"status": "ok", "service": "HMS backend"}