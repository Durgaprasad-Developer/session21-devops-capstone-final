from datetime import datetime, date, time
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
from app.models import AppointmentStatus


# ─── Doctor Schemas ────────────────────────────────────────────────────────────

class DoctorBase(BaseModel):
    name: str
    speciality: str
    email: Optional[str] = None
    phone: Optional[str] = None
    availability_start: Optional[time] = None
    availability_end: Optional[time] = None


class DoctorCreate(DoctorBase):
    pass


class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    speciality: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    availability_start: Optional[time] = None
    availability_end: Optional[time] = None


class DoctorOut(DoctorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ─── Patient Schemas ───────────────────────────────────────────────────────────

class PatientBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None


class PatientOut(PatientBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ─── Appointment Schemas ───────────────────────────────────────────────────────

class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: date
    start_time: time
    end_time: time
    reason: Optional[str] = None
    status: AppointmentStatus = AppointmentStatus.scheduled

    @field_validator("end_time")
    @classmethod
    def end_after_start(cls, end_time, info):
        start = info.data.get("start_time")
        if start and end_time <= start:
            raise ValueError("end_time must be after start_time")
        return end_time


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    appointment_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    reason: Optional[str] = None
    status: Optional[AppointmentStatus] = None


class AppointmentOut(AppointmentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    patient: Optional[PatientOut] = None
    doctor: Optional[DoctorOut] = None

    model_config = {"from_attributes": True}


class AppointmentStats(BaseModel):
    total: int
    today: int
    upcoming: int
    completed: int
    cancelled: int
