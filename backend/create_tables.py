"""
Direct Database Table Creation Script
This creates all tables directly without using Alembic migrations.
Use this if you want a quick setup without migration history.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.database import engine, Base
from app.models import User, Meal, InventoryItem, MealPlan, AccessoryItem


def create_tables():
    """Create all tables in the database."""
    print("🚀 Creating database tables...")

    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)

        print("✅ Database tables created successfully!")
        print("")
        print("Tables created:")
        print("  - users")
        print("  - meals")
        print("  - inventory")
        print("  - meal_plans")
        print("  - accessories")

    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        sys.exit(1)


if __name__ == "__main__":
    create_tables()
