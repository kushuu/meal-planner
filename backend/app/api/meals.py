from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.meal import Meal as MealModel
from app.schemas.meal import Meal, MealCreate

router = APIRouter()


@router.post("/", response_model=Meal)
def create_user(meal: MealCreate, db: Session = Depends(get_db)):
    db_user = MealModel(**meal.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/", response_model=List[Meal])
def get_users(db: Session = Depends(get_db)):
    return db.query(MealModel).all()


@router.get("/{user_id}", response_model=Meal)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(MealModel).filter(MealModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Meal not found")
    return user
