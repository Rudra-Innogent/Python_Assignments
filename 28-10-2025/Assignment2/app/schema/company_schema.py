
from pydantic import BaseModel
from typing import Optional

class CompanyBase(BaseModel):
    name: str

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: Optional[str] = None

class CompanyRead(CompanyBase):
    id: int

    class Config:
        orm_mode = True
