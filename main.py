from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import jwt, exceptions
from sqlalchemy.orm import Session

from jobs.crud import create_openings, get_applicant_by_name
from jobs.models import *
from jobs.db import engine, get_db
from jobs.schema import ApplicantSchema, ApplySchema, OpeningSchema

# initialize the database
# should be called only once
def init_db():
    Base.metadata.create_all(bind=engine)

#init_db()


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        return payload
    except exceptions.ExpiredSignatureError:
        return {"message": "Token has expired"}
    except exceptions.JWTError:
        return {"message": "Invalid token"}

@app.post("/token")
def login(user: OAuth2PasswordRequestForm = Depends()):
    # logins for admin are admin and admin
    # logins for user are user and user
    username = user.username
    password = user.password
    if username == "admin" and password == "admin":
        return {
            "access_token": jwt.encode({"username": username, "password": password}, "secret", algorithm="HS256"),
            "token_type": "bearer"
        }
    elif username == "user" and password == "user":
        return {
            "access_token": jwt.encode({"username": username, "password": password}, "secret", algorithm="HS256"),
            "token_type": "bearer"
        }
    else:
        return {"message": "Invalid credentials"}



@app.get("/openings", response_model=List[OpeningSchema])
def read_openings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    openings = db.query(Opening).offset(skip).limit(limit).all()
    return openings


@app.post("/openings",
          response_model=dict)
def create_application(openings: List[OpeningSchema], db: Session = Depends(get_db), token: dict = Depends(get_token)):
    if token['username'] != 'admin':
        return HTTPException(status_code=401, detail="Unauthorized")

    return create_openings(db=db, openings=openings)


@app.get("/applicants", response_model=List[ApplicantSchema])
def read_applicants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    applicants = db.query(Applicant).offset(skip).limit(limit).all()
    return applicants

@app.post("/applicant", response_model=dict)
def create_applicant(applicant: ApplicantSchema, db: Session = Depends(get_db)):
    db_applicant = Applicant(**applicant.model_dump())
    db.add(db_applicant)
    db.commit()
    return {"message": "Applicant created successfully"}


@app.post("/apply", response_model=dict)
def apply(applications: List[ApplySchema], db: Session = Depends(get_db), _ = Depends(get_token)):
    try:
        for application in applications:
            applicant = get_applicant_by_name(db=db, name=application.applicant_name)
            if applicant is None:
                return {"message": "Applicant does not exist"}
            db_application = Application(applicant_id=applicant.id, opening_id=application.opening_id)
            db.add(db_application)
        db.commit()
        return {"message": "Application created successfully"}
    except Exception as e:
        db.rollback()
        return {"message": str(e)}

@app.get("/applications", response_model=List[dict])
def read_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _ = Depends(get_token)):
    users_applications = []
    applications = db.query(Application).offset(skip).limit(limit).all()
    print(applications)

    for application in applications:
        user = db.query(Applicant).filter(Applicant.id == application.applicant_id).first()
        applicant = ApplicantSchema(**user.__dict__)

        opening = db.query(Opening).filter(Opening.id == application.opening_id).first()
        opening = OpeningSchema(**opening.__dict__)

        user_application = {}
        user_application['applicant_name'] = applicant
        user_application['opening_id'] = opening

        users_applications.append(user_application)


    return users_applications

