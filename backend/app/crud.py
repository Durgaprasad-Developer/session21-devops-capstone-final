from datetime import date, time
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from app import models, schemas
from fastapi import HTTPException


# ─── Doctor CRUD ──────────────────────────────────────────────────────────────

def get_doctors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Doctor).offset(skip).limit(limit).all()


def get_doctor(db: Session, doctor_id: int):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


def create_doctor(db: Session, data: schemas.DoctorCreate):
    doctor = models.Doctor(**data.model_dump())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


def update_doctor(db: Session, doctor_id: int, data: schemas.DoctorUpdate):
    doctor = get_doctor(db, doctor_id)
    for field, val in data.model_dump(exclude_unset=True).items():
        setattr(doctor, field, val)
    db.commit()
    db.refresh(doctor)
    return doctor


def delete_doctor(db: Session, doctor_id: int):
    doctor = get_doctor(db, doctor_id)
    db.delete(doctor)
    db.commit()


# ─── Patient CRUD ─────────────────────────────────────────────────────────────

def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Patient).offset(skip).limit(limit).all()


def get_patient(db: Session, patient_id: int):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


def create_patient(db: Session, data: schemas.PatientCreate):
    patient = models.Patient(**data.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def update_patient(db: Session, patient_id: int, data: schemas.PatientUpdate):
    patient = get_patient(db, patient_id)
    for field, val in data.model_dump(exclude_unset=True).items():
        setattr(patient, field, val)
    db.commit()
    db.refresh(patient)
    return patient


def delete_patient(db: Session, patient_id: int):
    patient = get_patient(db, patient_id)
    db.delete(patient)
    db.commit()


# ─── Appointment CRUD ─────────────────────────────────────────────────────────

def _check_no_overlap(
    db: Session,
    doctor_id: int,
    appt_date: date,
    start: time,
    end: time,
    exclude_id: Optional[int] = None,
):
    """Raise 409 if a non-cancelled appointment overlaps the requested slot."""
    query = db.query(models.Appointment).filter(
        models.Appointment.doctor_id == doctor_id,
        models.Appointment.appointment_date == appt_date,
        models.Appointment.status != models.AppointmentStatus.cancelled,
        models.Appointment.start_time < end,
        models.Appointment.end_time > start,
    )
    if exclude_id:
        query = query.filter(models.Appointment.id != exclude_id)
    if query.first():
        raise HTTPException(
            status_code=409,
            detail="Doctor already has a non-cancelled appointment in that time slot.",
        )


def _check_availability(db: Session, doctor_id: int, start: time, end: time):
    """Raise 422 if appointment is outside doctor's configured availability."""
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if doctor and doctor.availability_start and doctor.availability_end:
        if start < doctor.availability_start or end > doctor.availability_end:
            raise HTTPException(
                status_code=422,
                detail=(
                    f"Doctor is only available between "
                    f"{doctor.availability_start} and {doctor.availability_end}."
                ),
            )


def get_appointments(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    search: Optional[str] = None,
):
    query = (
        db.query(models.Appointment)
        .join(models.Patient)
        .join(models.Doctor)
    )
    if status:
        query = query.filter(models.Appointment.status == status)
    if search:
        term = f"%{search}%"
        query = query.filter(
            or_(
                models.Patient.name.ilike(term),
                models.Doctor.name.ilike(term),
                models.Appointment.reason.ilike(term),
            )
        )
    return (
        query.order_by(
            models.Appointment.appointment_date.desc(),
            models.Appointment.start_time.desc(),
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_appointment(db: Session, appointment_id: int):
    appt = (
        db.query(models.Appointment)
        .filter(models.Appointment.id == appointment_id)
        .first()
    )
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt


def create_appointment(db: Session, data: schemas.AppointmentCreate):
    # Validate referenced entities exist
    get_patient(db, data.patient_id)
    get_doctor(db, data.doctor_id)
    _check_availability(db, data.doctor_id, data.start_time, data.end_time)
    _check_no_overlap(db, data.doctor_id, data.appointment_date, data.start_time, data.end_time)

    appt = models.Appointment(**data.model_dump())
    db.add(appt)
    db.commit()
    db.refresh(appt)
    # Reload with relationships
    return get_appointment(db, appt.id)


def update_appointment(db: Session, appointment_id: int, data: schemas.AppointmentUpdate):
    appt = get_appointment(db, appointment_id)
    updates = data.model_dump(exclude_unset=True)

    new_doctor_id = updates.get("doctor_id", appt.doctor_id)
    new_date = updates.get("appointment_date", appt.appointment_date)
    new_start = updates.get("start_time", appt.start_time)
    new_end = updates.get("end_time", appt.end_time)

    if new_end <= new_start:
        raise HTTPException(status_code=422, detail="end_time must be after start_time")

    new_status = updates.get("status", appt.status)
    if new_status != models.AppointmentStatus.cancelled:
        _check_availability(db, new_doctor_id, new_start, new_end)
        _check_no_overlap(db, new_doctor_id, new_date, new_start, new_end, exclude_id=appointment_id)

    for field, val in updates.items():
        setattr(appt, field, val)
    db.commit()
    db.refresh(appt)
    return get_appointment(db, appt.id)


def delete_appointment(db: Session, appointment_id: int):
    appt = get_appointment(db, appointment_id)
    db.delete(appt)
    db.commit()


def get_appointment_stats(db: Session) -> schemas.AppointmentStats:
    today = date.today()
    total = db.query(func.count(models.Appointment.id)).scalar()
    today_count = (
        db.query(func.count(models.Appointment.id))
        .filter(models.Appointment.appointment_date == today)
        .scalar()
    )
    upcoming = (
        db.query(func.count(models.Appointment.id))
        .filter(
            models.Appointment.appointment_date > today,
            models.Appointment.status == models.AppointmentStatus.scheduled,
        )
        .scalar()
    )
    completed = (
        db.query(func.count(models.Appointment.id))
        .filter(models.Appointment.status == models.AppointmentStatus.completed)
        .scalar()
    )
    cancelled = (
        db.query(func.count(models.Appointment.id))
        .filter(models.Appointment.status == models.AppointmentStatus.cancelled)
        .scalar()
    )
    return schemas.AppointmentStats(
        total=total,
        today=today_count,
        upcoming=upcoming,
        completed=completed,
        cancelled=cancelled,
    )
