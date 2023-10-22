from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from jobs.db import Base

class Opening(Base):
    __tablename__ = 'openings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    description = Column(String(255))
    company = Column(String(255))
    location = Column(String(255))
    category = Column(String(255))
    created_at = Column(DateTime)
    deadline = Column(DateTime)
    open = Column(Boolean)

class Applicant(Base):
    __tablename__ = 'applicants'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(255))
    resume = Column(String(255))


class Application(Base):
    __tablename__ = 'applications'
    id = Column(Integer, primary_key=True, autoincrement=True)
    applicant_id = Column(Integer, ForeignKey('applicants.id'))
    opening_id = Column(Integer, ForeignKey('openings.id'))
    created_at = Column(DateTime)






