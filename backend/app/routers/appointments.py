from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/api/appointments", tags=["appointments"])


@router.get("/stats", response_model=schemas.AppointmentStats)
def appointment_stats(db: Session = Depends(get_db)):
    return crud.get_appointment_stats(db)


@router.get("", response_model=list[schemas.AppointmentOut])
def list_appointments(
    skip: int = 0,
    limit: int = Query(default=100, le=200),
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return crud.get_appointments(db, skip=skip, limit=limit, status=status, search=search)


@router.post("", response_model=schemas.AppointmentOut, status_code=201)
def create_appointment(data: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    return crud.create_appointment(db, data)


@router.get("/{appointment_id}", response_model=schemas.AppointmentOut)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    return crud.get_appointment(db, appointment_id)


@router.put("/{appointment_id}", response_model=schemas.AppointmentOut)
def update_appointment(
    appointment_id: int,
    data: schemas.AppointmentUpdate,
    db: Session = Depends(get_db),
):
    return crud.update_appointment(db, appointment_id, data)


@router.delete("/{appointment_id}", status_code=204)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    crud.delete_appointment(db, appointment_id)
