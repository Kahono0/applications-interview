from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class OpeningSchema(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    company: str
    location: str
    category: str
    created_at: datetime
    deadline: datetime

    class Config:
        orm_mode = True
        from_attributes=True

class ApplicantSchema(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    phone: str
    resume: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes=True


class ApplicationSchema(BaseModel):
    id: Optional[int] = None
    applicant_id: int
    opening_id: int
    created_at: str

    class Config:
        orm_mode = True
        from_attributes=True


class ApplySchema(BaseModel):
    applicant_name: str
    opening_id: int
    resume: str

    class Config:
        orm_mode = True
        from_attributes=True
