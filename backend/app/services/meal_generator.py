from datetime import date, timedelta
from typing import List
from sqlalchemy.orm import Session
from app.models.meal import Meal
from app.models.meal_plan import MealPlan
from app.models.user import User
from app.models.inventory import InventoryItem
from app.services.llm_service import LLMService
from app.schemas.meal import MealCreate


class MealGeneratorService:
    def __init__(self, db: Session):
        self.db = db
        self.llm_service = LLMService()

    async def generate_daily_meals(self, user_id: int, target_date: date):
        """Generate breakfast, lunch, and dinner for a user on a specific date"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"User {user_id} not found")

        # Get previous 7 days of meals to avoid repetition
        previous_meals = self._get_recent_meals(user_id, days=7)

        # Get available ingredients
        available_ingredients = self._get_inventory_items()

        meal_plans = []
        for meal_type in ["breakfast", "lunch", "dinner"]:
            meal_data = await self.llm_service.generate_meal(
                is_vegetarian=user.is_vegetarian,
                protein_target=user.protein_target,
                fiber_target=user.fiber_target,
                previous_meals=previous_meals,
                available_ingredients=available_ingredients,
                meal_type=meal_type
            )

            # Create or get existing meal
            meal = self._create_or_get_meal(meal_data)

            # Create meal plan entry
            meal_plan = MealPlan(
                user_id=user_id,
                date=target_date,
                meal_type=meal_type,
                meal_id=meal.id,
                eaten_outside=False
            )
            self.db.add(meal_plan)
            meal_plans.append(meal_plan)

        self.db.commit()
        return meal_plans

    def _get_recent_meals(self, user_id: int, days: int = 7) -> List[str]:
        """Get list of recent meal names to avoid repetition"""
        start_date = date.today() - timedelta(days=days)

        recent_plans = (
            self.db.query(MealPlan)
            .filter(MealPlan.user_id == user_id)
            .filter(MealPlan.date >= start_date)
            .filter(MealPlan.meal_id.isnot(None))
            .all()
        )

        meal_ids = [plan.meal_id for plan in recent_plans]
        meals: List[Meal] = self.db.query(
            Meal).filter(Meal.id.in_(meal_ids)).all()

        return [meal.name for meal in meals]

    def _get_inventory_items(self) -> List[str]:
        """Get list of available ingredients from inventory"""
        items = self.db.query(InventoryItem).all()
        return [item.item_name for item in items]

    def _create_or_get_meal(self, meal_data: dict) -> Meal:
        """Create a new meal or return existing one with same name"""
        existing = (
            self.db.query(Meal)
            .filter(Meal.name == meal_data["name"])
            .first()
        )

        if existing:
            return existing

        meal = Meal(**meal_data)
        self.db.add(meal)
        self.db.flush()
        return meal
