from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import schemas
import models


def create_user(user: schemas.UserCreate, db: Session) -> models.User:
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists."
        )
    
    hashed_password = models.hash_password(user.password)
    new_user = models.User(
        username=user.username,
        password=hashed_password,
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "username": new_user.username}