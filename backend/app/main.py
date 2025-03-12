from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.params import Body
from.database import engine, SessionLocal
from .models import Base, Faculty, Assignment, Submission
from .auth import create_access_token, hash_password, verify_password
from sqlalchemy.orm import Session
from pydantic import BaseModel

app = FastAPI()

# This will create tables in the database
Base.metadata.create_all(bind=engine)

# Dependency Injection to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/faculty/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    faculty = db.query(Faculty).filter(Faculty.email == email).first()
    if not faculty or not verify_password(password, faculty.password):
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    token = create_access_token({"sub": faculty.email})
    return {"access_token": token} 

# class FacultyCreate(BaseModel):
#     email: str
#     password: str

# # Function to Register Faculty
# @app.post("/faculty/register")
# def register_faculty(faculty: FacultyCreate, db: Session = Depends(SessionLocal)):
#     # Check if email already exists
#     existing_faculty = db.query(Faculty).filter(Faculty.email == faculty.email).first()
#     if existing_faculty:
#         raise HTTPException(status_code=400, detail="Email already registered")
    
#     # Create new faculty
#     new_faculty = Faculty(email=faculty.email, password=faculty.password)
#     db.add(new_faculty)
#     db.commit()
#     db.refresh(new_faculty)

#     # Return success response
#     return {
#         "message": "Faculty registered successfully",
#         "faculty_id": new_faculty.id
#     }


@app.post("/faculty/register")
def register_faculty(
    email: str, 
    password: str, 
    db: Session = Depends(SessionLocal)
):
    # Check if email already exists
    existing_faculty = db.query(Faculty).filter(Faculty.email == email).first()
    if existing_faculty:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new faculty
    new_faculty = Faculty(email=email, password=password)
    db.add(new_faculty)
    db.commit()
    db.refresh(new_faculty)

    # Return success response
    return {
        "message": "Faculty registered successfully",
        "faculty_id": new_faculty.id
    }