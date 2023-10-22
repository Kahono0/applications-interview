from pydantic import BaseModel

class OpeningSchema(BaseModel):
    title: str
    description: str
    company: str
    location: str
    category: str
    deadline: str

    class Config:
        orm_mode = True

class ApplicantSchema(BaseModel):
    name: str
    email: str
    phone: str
    resume: str

    class Config:
        orm_mode = True


class ApplicationSchema(BaseModel):
    applicant_id: int
    opening_id: int
    created_at: str

    class Config:
        orm_mode = True


