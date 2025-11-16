from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    is_vegetarian = Column(Boolean, default=False)
    protein_target = Column(Integer, default=80)
    fiber_target = Column(Integer, default=30)