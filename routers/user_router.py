from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from services import user_service
from database import get_db
import schemas

router = APIRouter(
    tags=["User"]
)

# @router.post("/users", status_code=status.HTTP_201_CREATED)
# def create_user(
#     user: schemas.UserCreate,
#     db: Session = Depends(get_db),
# ):
#     return user_service.create_user(user=user, db=db)