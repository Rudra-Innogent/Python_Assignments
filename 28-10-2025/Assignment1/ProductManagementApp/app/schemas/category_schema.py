from pydantic import BaseModel
from typing import Optional

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    company_id: int

class CategoryRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    company_id: int

    class Config:
        orm_mode = True
        from_attributes = True
