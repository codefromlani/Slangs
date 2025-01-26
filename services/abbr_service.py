from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from sqlalchemy import func
import schemas
import models

def create_abbr(abbr: schemas.AbbreviationCreate, db: Session) -> models.Abbreviation:
    db_abbr = db.query(models.Abbreviation).filter(
        func.lower(models.Abbreviation.abbreviation) == func.lower(abbr.abbreviation)  
    ).first()
    if db_abbr:
        if db_abbr.status == models.AbbreviationEnum.PENDING:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This abbreviation is pending review!"
            )
        
        if db_abbr.status == models.AbbreviationEnum.REJECTED:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This abbreviation was previously rejected. Please modify it before resubmitting."
            )
        
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Abbreviation already exists."
        )
    
    new_abbr = models.Abbreviation(
        abbreviation=abbr.abbreviation,
        meaning=abbr.meaning,
        status=models.AbbreviationEnum.PENDING,
        created_at=datetime.utcnow()
    )

    db.add(new_abbr)
    db.commit()
    db.refresh(new_abbr)

    return {
        "message": "Abbreviation created successfully.",
    }

def approve_abbr(abbr_id: int, new_status: schemas.AbbreviationEnum, db: Session):
    abbr = db.query(models.Abbreviation).filter(models.Abbreviation.id == abbr_id).first()
    if not abbr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Abbreviation not found."
        )
    
    if new_status not in [
        schemas.AbbreviationEnum.PENDING,
        schemas.AbbreviationEnum.APPROVED,
        schemas.AbbreviationEnum.REJECTED
    ]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status"
        )
    
    if abbr.status == models.AbbreviationEnum.APPROVED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Abbreviation has already been approved."
        )
    if abbr.status == models.AbbreviationEnum.REJECTED and new_status != models.AbbreviationEnum.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rejected abbreviations must be modified before resubmitting."
        )
    
    abbr.status = new_status
    
    abbr.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(abbr)

    return schemas.AbbreviationResponse(
        id=abbr.id,
        abbreviation=abbr.abbreviation,
        meaning=abbr.meaning,
        status=abbr.status
    )

def get_abbr(abbr: str, db: Session):
    result = db.query(models.Abbreviation).filter(
        func.lower(models.Abbreviation.abbreviation) == func.lower(abbr),
        models.Abbreviation.status == models.AbbreviationEnum.APPROVED
    ).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This abbreviation does not exist in our records."
        )
    
    return schemas.AbbreviationResponse(
        id=result.id,
        abbreviation=result.abbreviation,
        meaning=result.meaning,
        status=result.status
    )

def get_all_abbr(db: Session, skip: int = 0, limit: int = 20) -> List[models.Abbreviation]:
    db_abbr = db.query(models.Abbreviation).offset(skip).limit(limit).all()
    return db_abbr

def update_abbr(abbr_id: int, updated_abbr: schemas.AbbreviationUpdate, db: Session) -> Optional[models.Abbreviation]:
    db_abbr = db.query(models.Abbreviation).filter(models.Abbreviation.id == abbr_id).first()
    if db_abbr is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(f"Abbreviation with the id {abbr_id} not found.")
            )
    
    if updated_abbr.abbreviation:
        db_abbr.abbreviation=updated_abbr.abbreviation

    if updated_abbr.meaning:
        db_abbr.meaning=updated_abbr.meaning

    if updated_abbr.status:
        db_abbr.status=updated_abbr.status

    db.commit()
    db.refresh(db_abbr)
    return db_abbr

def delete_abbr(abbr_id: int, db: Session):
    db_abbr = db.query(models.Abbreviation).filter(models.Abbreviation.id == abbr_id).first()
    if db_abbr is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(f"Abbreviation with the id {abbr_id} not found.")
            )
    
    db.delete(db_abbr)
    db.commit()

    return {"message": "Abbreviation deleted successfully."}

def get_abbr_by_status(db: Session, abbr_status: schemas.AbbreviationEnum, skip: int=0, limit: int =10) -> list[models.Abbreviation]:

    if abbr_status not in [schemas.AbbreviationEnum.PENDING, schemas.AbbreviationEnum.REJECTED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status must be either 'pending' or 'rejected'."
        )
    
    db_abbr = db.query(models.Abbreviation).filter(models.Abbreviation.status == abbr_status).offset(skip).limit(limit).all()
    return db_abbr