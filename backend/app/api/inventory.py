from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.inventory import InventoryItem as InventoryModel
from app.schemas.inventory import InventoryItem, InventoryItemCreate

router = APIRouter()


@router.post("/", response_model=InventoryItem)
def create_user(meal: InventoryItemCreate, db: Session = Depends(get_db)):
    db_user = InventoryModel(**meal.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/", response_model=List[InventoryItem])
def get_users(db: Session = Depends(get_db)):
    return db.query(InventoryModel).all()


@router.get("/{user_id}", response_model=InventoryItem)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(InventoryModel).filter(
        InventoryModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="InventoryItem not found")
    return user


@router.delete("/{id}")
def delete_inventory_item(id: int, db: Session = Depends(get_db)):
    item = db.query(InventoryModel).filter(InventoryModel.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="InventoryItem not found")
    db.delete(item)
    db.commit()
    return {"detail": "InventoryItem deleted successfully"}
