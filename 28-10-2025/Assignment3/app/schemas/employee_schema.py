from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class EmployeeBase(BaseModel):
    name: str
    email: str
    department: str
    salary: float
    joinDate: datetime


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeResponse(EmployeeBase):
    id: int
    createdAt: datetime


class EmployeeUpdate():
    name: Optional[str]
    email: Optional[str]
    department: Optional[str]
    salary: Optional[float]
    joinDate: Optional[datetime]