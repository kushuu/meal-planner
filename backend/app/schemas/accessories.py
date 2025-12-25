from pydantic import BaseModel


class AccessoryBase(BaseModel):
    accessory_name: str
    description: str | None = None


class AccessoryCreate(AccessoryBase):
    pass


class Accessory(AccessoryBase):
    id: int

    class Config:
        from_attributes = True
