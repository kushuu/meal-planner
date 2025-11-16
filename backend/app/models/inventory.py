from sqlalchemy import Column, Integer, String
from app.database import Base


class InventoryItem(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, unique=True, index=True)
    quantity = Column(Integer, default=0)
    unit = Column(String, default="units")
