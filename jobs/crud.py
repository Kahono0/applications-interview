from typing import List
from sqlalchemy.orm.session import Session
from jobs.models import Opening, Applicant, Application
from jobs.schema import OpeningSchema, ApplicantSchema, ApplicationSchema

def create_openings(db: Session, openings: List[OpeningSchema]) -> dict:
    try:
        for opening in openings:
            db_opening = Opening(**opening.model_dump())
            db.add(db_opening)
        db.commit()
        return {"message": "Openings created successfully"}
    except Exception as e:
        db.rollback()
        return {"message": str(e)}

def create_applicants(db: Session, applicants: List[ApplicantSchema]) -> dict:
    try:
        for applicant in applicants:
            db_applicant = Applicant(**applicant.model_dump())
            db.add(db_applicant)
        db.commit()
        return {"message": "Applicants created successfully"}
    except Exception as e:
        db.rollback()
        return {"message": str(e)}


def create_application(db: Session, applicant_id: int, opening_id: int) -> dict:
    try:
        db_application = Application(applicant_id=applicant_id, opening_id=opening_id)
        db.add(db_application)
        db.commit()
        return {"message": "Application created successfully"}
    except Exception as e:
        db.rollback()
        return {"message": str(e)}


def get_openings(db: Session) -> List[OpeningSchema]:
    return [OpeningSchema.from_orm(opening) for opening in db.query(Opening).all()]




