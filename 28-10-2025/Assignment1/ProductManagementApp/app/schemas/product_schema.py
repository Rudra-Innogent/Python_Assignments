from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    company_id: int
    category_id: int

class ProductCreate(ProductBase):
    pass

class ProductRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    company_name: str
    category_name: str

    class Config:
        orm_mode = True
        from_attributes = True
