from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class MealPlan(Base):
    __tablename__ = "meal_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date, index=True)
    meal_type = Column(String)  # breakfast, lunch, dinner
    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=True)
    eaten_outside = Column(Boolean, default=False)

    user = relationship("User")
    meal = relationship("Meal")
