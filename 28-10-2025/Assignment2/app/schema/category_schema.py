
from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    name: str
    companyId: int

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None

class CategoryRead(BaseModel):
    id: int
    name: str
    companyId: int

    class Config:
        orm_mode = True
