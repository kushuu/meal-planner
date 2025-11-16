from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    is_vegetarian: bool = False
    protein_target: int = 80
    fiber_target: int = 30


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        from_attributes = True
