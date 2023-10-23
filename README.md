# Application system
A system that collects job openings and applications and can give you a list of applicants and their applications.
It uses fastapi python framework.

I used pydantic models for serialization and sqlalchemy for database models, sqlite as the database.

To implement security, I used oauth2 fastapi that requests for an authorization header for the below endpoints
```
POST /openings
POST /apply
GET /applications
```
For the endpoint `POST /opening` the user must be admin.

The credentials for admin are :
```
username: admin
password: admin
```
and for a normal user are:
```
username: user
password: user
```

## Running the application
Clone this project
```bash
git clone https://github.com/Kahono0/applications-interview.git
```
Change into the directory
```bash
cd applications-interview
```
Start the virtual environment and install the requirements
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Run the program
```bash
uvicorn main:app
```

Now head to the docs page to test the api endpoints at [http://127.0.0.1:8000/docs/](http://127.0.0.1:8000/docs/)

Before testing the endpoints, click on Authorize and input the credentials above.


