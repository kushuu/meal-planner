from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.accessories import AccessoryItem as AccessoryModel
from app.schemas.accessories import Accessory, AccessoryCreate

router = APIRouter()


@router.post("/", response_model=Accessory)
def create_accessory(accessory: AccessoryCreate, db: Session = Depends(get_db)):
    db_accessory = AccessoryModel(**accessory.dict())
    db.add(db_accessory)
    db.commit()
    db.refresh(db_accessory)
    return db_accessory


@router.get("/", response_model=List[Accessory])
def get_accessories(db: Session = Depends(get_db)):
    return db.query(AccessoryModel).all()


@router.get("/{accessory_id}", response_model=Accessory)
def get_accessory(accessory_id: int, db: Session = Depends(get_db)):
    accessory = (
        db.query(AccessoryModel).filter(AccessoryModel.id == accessory_id).first()
    )
    if not accessory:
        raise HTTPException(status_code=404, detail="Accessory not found")
    return accessory


@router.delete("/{id}")
def delete_accessory(id: int, db: Session = Depends(get_db)):
    accessory = db.query(AccessoryModel).filter(AccessoryModel.id == id).first()
    if not accessory:
        raise HTTPException(status_code=404, detail="Accessory not found")
    db.delete(accessory)
    db.commit()
    return {"detail": "Accessory deleted successfully"}
