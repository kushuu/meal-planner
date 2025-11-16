from pydantic import BaseModel
from datetime import date
from typing import Optional
from app.schemas.meal import Meal


class MealPlanBase(BaseModel):
    user_id: int
    date: date
    meal_type: str  # breakfast, lunch, dinner
    meal_id: Optional[int] = None
    eaten_outside: bool = False


class MealPlanCreate(MealPlanBase):
    pass


class MealPlan(MealPlanBase):
    id: int

    class Config:
        from_attributes = True


class MealPlanWithDetails(MealPlan):
    meal: Optional[Meal] = None
    user_name: str
