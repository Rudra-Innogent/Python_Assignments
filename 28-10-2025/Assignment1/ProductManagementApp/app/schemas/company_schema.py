from pydantic import BaseModel
from typing import Optional

class CompanyCreate(BaseModel):
    name: str
    description: Optional[str] = None

class CompanyRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True
