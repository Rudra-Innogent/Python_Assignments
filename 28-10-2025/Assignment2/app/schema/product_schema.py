
from pydantic import BaseModel, Field
from typing import Optional


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1)
    price: float
    companyId: int
    categoryId: int
    description: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    companyId: Optional[int] = None
    categoryId: Optional[int] = None
    description: Optional[str] = None

class ProductRead(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str]
    companyId: int
    categoryId: int
    company_name: str
    category_name: str

    class Config:
        orm_mode = True
