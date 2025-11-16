from pydantic import BaseModel
from typing import List, Dict, Optional


class MealBase(BaseModel):
    name: str
    description: str
    cuisine_type: str
    is_vegetarian: bool
    calories: float
    protein: float
    fiber: float
    carbs: float
    fats: float
    ingredients: List[Dict[str, str]]
    instructions: Optional[str] = None
    prep_time_minutes: Optional[int] = None


class MealCreate(MealBase):
    pass


class Meal(MealBase):
    id: int

    class Config:
        from_attributes = True
