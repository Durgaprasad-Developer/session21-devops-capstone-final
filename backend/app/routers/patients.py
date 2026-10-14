from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/api/patients", tags=["patients"])


@router.get("", response_model=list[schemas.PatientOut])
def list_patients(
    skip: int = 0,
    limit: int = Query(default=100, le=200),
    db: Session = Depends(get_db),
):
    return crud.get_patients(db, skip=skip, limit=limit)


@router.post("", response_model=schemas.PatientOut, status_code=201)
def create_patient(data: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db, data)


@router.get("/{patient_id}", response_model=schemas.PatientOut)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    return crud.get_patient(db, patient_id)


@router.put("/{patient_id}", response_model=schemas.PatientOut)
def update_patient(
    patient_id: int, data: schemas.PatientUpdate, db: Session = Depends(get_db)
):
    return crud.update_patient(db, patient_id, data)


@router.delete("/{patient_id}", status_code=204)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    crud.delete_patient(db, patient_id)
