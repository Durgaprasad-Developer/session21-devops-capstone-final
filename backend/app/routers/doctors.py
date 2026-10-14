from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/api/doctors", tags=["doctors"])


@router.get("", response_model=list[schemas.DoctorOut])
def list_doctors(
    skip: int = 0,
    limit: int = Query(default=100, le=200),
    db: Session = Depends(get_db),
):
    return crud.get_doctors(db, skip=skip, limit=limit)


@router.post("", response_model=schemas.DoctorOut, status_code=201)
def create_doctor(data: schemas.DoctorCreate, db: Session = Depends(get_db)):
    return crud.create_doctor(db, data)


@router.get("/{doctor_id}", response_model=schemas.DoctorOut)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    return crud.get_doctor(db, doctor_id)


@router.put("/{doctor_id}", response_model=schemas.DoctorOut)
def update_doctor(
    doctor_id: int, data: schemas.DoctorUpdate, db: Session = Depends(get_db)
):
    return crud.update_doctor(db, doctor_id, data)


@router.delete("/{doctor_id}", status_code=204)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    crud.delete_doctor(db, doctor_id)
