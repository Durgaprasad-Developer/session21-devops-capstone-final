from contextlib import asynccontextmanager
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from prometheus_fastapi_instrumentator import Instrumentator

from app.database import engine, get_db, SessionLocal
from app.routers import appointments, doctors, patients
import app.models as models


@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_sample_data()
    yield


app = FastAPI(
    title="BookEase API",
    description="Appointment Booking Management System",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow React dev server and production frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics
Instrumentator().instrument(app).expose(app)

# Routers
app.include_router(appointments.router)
app.include_router(doctors.router)
app.include_router(patients.router)


@app.get("/", tags=["health"])
def root():
    return {"service": "BookEase API", "version": "1.0.0", "status": "running"}


@app.get("/health", tags=["health"])
def health():
    return {"status": "healthy"}


@app.get("/ready", tags=["health"])
def ready():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception as exc:
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail=f"Database not ready: {exc}")


def seed_sample_data():
    """Insert sample data only if the tables are empty."""
    db = SessionLocal()
    try:
        if db.query(models.Doctor).count() > 0:
            return

        from datetime import time as t
        doctors = [
            models.Doctor(
                name="Dr. Ananya Krishnan",
                speciality="Cardiology",
                email="ananya.krishnan@bookease.com",
                phone="+91-9876543210",
                availability_start=t(9, 0),
                availability_end=t(17, 0),
            ),
            models.Doctor(
                name="Dr. Rahul Mehta",
                speciality="Orthopedics",
                email="rahul.mehta@bookease.com",
                phone="+91-9876543211",
                availability_start=t(10, 0),
                availability_end=t(18, 0),
            ),
            models.Doctor(
                name="Dr. Priya Sharma",
                speciality="Neurology",
                email="priya.sharma@bookease.com",
                phone="+91-9876543212",
                availability_start=t(8, 0),
                availability_end=t(16, 0),
            ),
        ]
        db.add_all(doctors)
        db.flush()

        patients = [
            models.Patient(
                name="Vikram Nair",
                email="vikram.nair@example.com",
                phone="+91-9123456781",
            ),
            models.Patient(
                name="Sunita Patel",
                email="sunita.patel@example.com",
                phone="+91-9123456782",
            ),
            models.Patient(
                name="Arjun Reddy",
                email="arjun.reddy@example.com",
                phone="+91-9123456783",
            ),
        ]
        db.add_all(patients)
        db.flush()

        from datetime import date, time as t
        appointments = [
            models.Appointment(
                patient_id=patients[0].id,
                doctor_id=doctors[0].id,
                appointment_date=date.today(),
                start_time=t(10, 0),
                end_time=t(10, 30),
                reason="Routine heart check-up",
                status=models.AppointmentStatus.scheduled,
            ),
            models.Appointment(
                patient_id=patients[1].id,
                doctor_id=doctors[1].id,
                appointment_date=date.today(),
                start_time=t(11, 0),
                end_time=t(11, 30),
                reason="Knee pain follow-up",
                status=models.AppointmentStatus.completed,
            ),
            models.Appointment(
                patient_id=patients[2].id,
                doctor_id=doctors[2].id,
                appointment_date=date.today(),
                start_time=t(14, 0),
                end_time=t(14, 30),
                reason="Migraine consultation",
                status=models.AppointmentStatus.scheduled,
            ),
        ]
        db.add_all(appointments)
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()


# Startup handled by lifespan context manager above
