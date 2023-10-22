from jobs.models import *
from jobs.db import engine

def init_db():
    Base.metadata.create_all(bind=engine)

#init_db()
