from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.api import meals, inventory, meal_plans, users

settings = get_settings()

app = FastAPI(
    title=settings['api_title'],
    version=settings['api_version']
)

# CORS middleware for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(meals.router, prefix="/api/meals", tags=["meals"])
app.include_router(
    inventory.router, prefix="/api/inventory", tags=["inventory"])
app.include_router(meal_plans.router,
                   prefix="/api/meal-plans", tags=["meal-plans"])


@app.get("/")
def root():
    return {"message": "Meal Planner API", "version": settings['api_version']}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
