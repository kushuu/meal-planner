from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.database import get_db
from app.models.meal_plan import MealPlan as MealPlanModel
from app.schemas.meal_plan import MealPlan
from app.services.meal_generator import MealGeneratorService

router = APIRouter()


@router.post("/generate/{user_id}")
async def generate_meal_plan(
    user_id: int,
    target_date: date,
    db: Session = Depends(get_db)
):
    """Generate daily meal plan for a user"""
    generator = MealGeneratorService(db)
    try:
        meal_plans = await generator.generate_daily_meals(user_id, target_date)
        return {"message": "Meal plan generated", "plans": len(meal_plans)}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating meals: {str(e)}")


@router.get("/user/{user_id}", response_model=List[MealPlan])
def get_user_meal_plans(
    user_id: int,
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db)
):
    """Get meal plans for a user within date range"""
    plans = (
        db.query(MealPlanModel)
        .filter(MealPlanModel.user_id == user_id)
        .filter(MealPlanModel.date >= start_date)
        .filter(MealPlanModel.date <= end_date)
        .all()
    )
    return plans


@router.patch("/{plan_id}/eaten-outside", response_model=MealPlan)
def mark_eaten_outside(plan_id: int, eaten_outside: bool, db: Session = Depends(get_db)):
    """Toggle eaten outside flag"""
    plan = db.query(MealPlanModel).filter(MealPlanModel.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Meal plan not found")

    plan.eaten_outside = eaten_outside
    db.commit()
    db.refresh(plan)
    return plan
