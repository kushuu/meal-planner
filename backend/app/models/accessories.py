from sqlalchemy import Column, Integer, String
from app.database import Base


class AccessoryItem(Base):
    __tablename__ = "accessories"

    id = Column(Integer, primary_key=True, index=True)
    accessory_name = Column(String, unique=True, index=True)
    description = Column(String, default="")
