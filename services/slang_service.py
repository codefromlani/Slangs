import os
from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
import models


def read_and_insert_slangs(filename: str, db: Session):
    if not os.path.exists(filename):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    try:
        with open(filename, 'r') as file:
            content = file.read().strip()
        lines = content.splitlines()
        
        new_abbrs = []
        for line in lines:
            line = line.strip()
            
            if "=" not in line or line.count("=") != 1:
                print(f"Skipping invalid line: {line}")
                continue
            
            slang, meaning = line.split("=", 1)
            
            existing_abbr = db.query(models.Abbreviation).filter(
                func.lower(models.Abbreviation.abbreviation) == func.lower(slang)
            ).first()
            
            if existing_abbr:
                print(f"Skipping: {slang} (already exists)")
                continue
            
            new_abbr = models.Abbreviation(
                abbreviation=slang,
                meaning=meaning,
                status=models.AbbreviationEnum.APPROVED,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            new_abbrs.append(new_abbr)
        
        if new_abbrs:
            db.add_all(new_abbrs)
            db.commit()
            print(f"Inserted {len(new_abbrs)} new abbreviations")
    
    except Exception as e:
        print(f"Error reading file: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error reading file"
        )