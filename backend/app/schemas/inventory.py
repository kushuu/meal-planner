from pydantic import BaseModel


class InventoryItemBase(BaseModel):
    item_name: str


class InventoryItemCreate(InventoryItemBase):
    pass


class InventoryItem(InventoryItemBase):
    id: int

    class Config:
        from_attributes = True
