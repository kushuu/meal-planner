import re
from openai import OpenAI
import os
import ollama
import json
from typing import Dict, List
from app.config import get_settings
from dotenv import load_dotenv

settings = get_settings()
load_dotenv()


class LLMService:
    def __init__(self):
        self.ollama_client = ollama.Client(host=settings['ollama_host'])
        self.openai_client = OpenAI(
            api_key=os.getenv('NVIDIA_API_KEY'),
            base_url=settings['openai_base_url']
        )
        self.model = settings['ollama_model']
        self.use_ollama = settings['use_ollama']
        self.nvidia_nim_model = settings['nvidia_nim_model']

    async def generate_meal(
        self,
        is_vegetarian: bool,
        protein_target: int,
        fiber_target: int,
        previous_meals: List[str],
        available_ingredients: List[str],
        meal_type: str = "dinner"
    ) -> Dict:
        """
        Generate a meal suggestion using Ollama LLM
        Returns a dictionary with meal details
        """

        prompt = self._build_meal_prompt(
            is_vegetarian,
            protein_target,
            fiber_target,
            previous_meals,
            available_ingredients,
            meal_type
        )

        try:
            print("Generating meal for meal type:", meal_type)
            if self.use_ollama:
                response = self.ollama_client.generate(
                    model=self.model,
                    prompt=prompt,
                    format="json"
                )
                meal_data = json.loads(response)
            else:
                response = self.openai_client.chat.completions.create(
                    model=self.nvidia_nim_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=1000,
                    stream=False
                )

                json_content = re.search(r'```json(.*?)```', response.choices[0].message.content, re.DOTALL)
                meal_data = json.loads(json_content.group(1))
            return meal_data

        except Exception as e:
            print(f"Error generating meal: {e}.\nWas building the meal plan for {meal_type}.")
            return self._get_fallback_meal(is_vegetarian, meal_type)

    def _build_meal_prompt(
        self,
        is_vegetarian: bool,
        protein_target: int,
        fiber_target: int,
        previous_meals: List[str],
        available_ingredients: List[str],
        meal_type: str
    ) -> str:
        diet_type = "vegetarian (no meat, fish, or eggs)" if is_vegetarian else "any"
        prev_meals_str = ", ".join(
            previous_meals) if previous_meals else "None"
        ingredients_str = ", ".join(
            available_ingredients) if available_ingredients else "any common ingredients"
        print("Building prompt for meal type:", meal_type)
        print("Previous meals to avoid:", prev_meals_str)
        print("Ingredients available:", ingredients_str)

        prompt = f"""Create a {meal_type} meal plan with the following requirements:

Diet: {diet_type}
Target: High protein ({protein_target}g) and high fiber ({fiber_target}g)
Previous meals to avoid repetition: {prev_meals_str}
Available ingredients to prioritize: {ingredients_str}
Do not use any ingredients not listed as available and do not use all the ingredients in one meal.
Return the actual values of protein, fiber, calories, etc. Do not return estimates or placeholder values.

Return ONLY a JSON object with this exact structure:
{{
    "name": "Meal name",
    "description": "Brief description",
    "cuisine_type": "Cuisine type",
    "is_vegetarian": {str(is_vegetarian).lower()},
    "calories": 500,
    "protein": {protein_target // 3},
    "fiber": {fiber_target // 3},
    "carbs": 60,
    "fats": 20,
    "ingredients": [
        {{"name": "ingredient1", "quantity": "100", "unit": "g"}},
        {{"name": "ingredient2", "quantity": "2", "unit": "cups"}}
    ],
    "instructions": "Step by step cooking instructions",
    "prep_time_minutes": 30
}}

Make it nutritious, varied, and delicious. Ensure protein and fiber targets are met."""

        return prompt

    def _get_fallback_meal(self, is_vegetarian: bool, meal_type: str) -> Dict:
        """Fallback meal when LLM fails"""
        if is_vegetarian:
            return {
                "name": "Quinoa Buddha Bowl",
                "description": "Protein-rich quinoa bowl with vegetables",
                "cuisine_type": "Healthy",
                "is_vegetarian": True,
                "calories": 450,
                "protein": 25,
                "fiber": 12,
                "carbs": 55,
                "fats": 15,
                "ingredients": [
                    {"name": "quinoa", "quantity": "1", "unit": "cup"},
                    {"name": "chickpeas", "quantity": "150", "unit": "g"},
                    {"name": "spinach", "quantity": "2", "unit": "cups"},
                    {"name": "avocado", "quantity": "0.5", "unit": "whole"}
                ],
                "instructions": "Cook quinoa, roast chickpeas, assemble with fresh veggies",
                "prep_time_minutes": 25
            }
        else:
            return {
                "name": "Grilled Chicken with Veggies",
                "description": "High protein meal with mixed vegetables",
                "cuisine_type": "Healthy",
                "is_vegetarian": False,
                "calories": 500,
                "protein": 40,
                "fiber": 10,
                "carbs": 35,
                "fats": 18,
                "ingredients": [
                    {"name": "chicken breast", "quantity": "200", "unit": "g"},
                    {"name": "broccoli", "quantity": "1", "unit": "cup"},
                    {"name": "sweet potato", "quantity": "1", "unit": "medium"}
                ],
                "instructions": "Grill chicken, steam vegetables, serve together",
                "prep_time_minutes": 30
            }
