from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from services import abbr_service
from database import get_db
from typing import List
import schemas
import models
import auth

router = APIRouter(
    tags=["Abbreviation"]
)

@router.post("/abbreviations", status_code=status.HTTP_201_CREATED)
def create_abbr(
    abbr: schemas.AbbreviationCreate,
    db: Session = Depends(get_db)
):
    return abbr_service.create_abbr(abbr=abbr, db=db)

@router.patch("/approve_abbreviation/{abbr_id}", response_model=schemas.AbbreviationResponse)
def approve_abbr(
    abbr_id: int, 
    new_status: schemas.AbbreviationEnum,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_admin_user)
):
    return abbr_service.approve_abbr(abbr_id=abbr_id, new_status=new_status, db=db)

@router.get("/get_abbreviation/{abbr}", response_model=schemas.AbbreviationResponse)
def get_abbr(
    abbr: str, 
    db: Session = Depends(get_db)
):
    return abbr_service.get_abbr(abbr=abbr, db=db)

@router.get("/get_abbreviations", response_model=List[schemas.AbbreviationResponse])
def get_all_abbr(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_admin_user)
):
    return abbr_service.get_all_abbr(skip=skip, limit=limit, db=db)

@router.patch("/abbreviations/{abbr_id}", response_model=schemas.AbbreviationResponse)
def update_abbr(
    abbr_id: int,
    updated_abbr: schemas.AbbreviationUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_admin_user)
):
    return abbr_service.update_abbr(abbr_id=abbr_id, updated_abbr=updated_abbr, db=db)

@router.delete("/abbreviations/{abbr_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_abbr(
    abbr_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_admin_user)
):
    return abbr_service.delete_abbr(abbr_id=abbr_id, db=db)

@router.get("/abbreviations/status/{status}", response_model=List[schemas.AbbreviationResponse])
def get_abbr_by_status(
    abbr_status: schemas.AbbreviationEnum,  
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_admin_user)
):
    return abbr_service.get_abbr_by_status(abbr_status=abbr_status, limit=limit, skip=skip, db=db)