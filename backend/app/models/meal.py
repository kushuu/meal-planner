from sqlalchemy import Column, Integer, String, Float, Text, JSON, Boolean
from app.database import Base


class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    cuisine_type = Column(String)
    is_vegetarian = Column(Boolean, default=False)

    # Nutritional info
    calories = Column(Float)
    protein = Column(Float)  # grams
    fiber = Column(Float)    # grams
    carbs = Column(Float)
    fats = Column(Float)

    # Ingredients stored as JSON: [{"name": "tomato", "quantity": "2", "unit": "whole"}]
    ingredients = Column(JSON)

    # Optional recipe instructions
    instructions = Column(Text, nullable=True)
    prep_time_minutes = Column(Integer, nullable=True)
