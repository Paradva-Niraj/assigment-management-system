from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.params import Body
from.database import engine, SessionLocal
from .models import Base, Faculty, Assignment, Submission
from .auth import create_access_token, hash_password, verify_password, get_current_user
from sqlalchemy.orm import Session
from pydantic import BaseModel

from.models import Faculty
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, EmailStr
from .database import Base,engine,SessionLocal,get_password_hash

# file upload
import shutil
import os


app = FastAPI()


# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/faculty/login")
def login(
    email: str = Body(..., embed=True), 
    password: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    faculty = db.query(Faculty).filter(Faculty.email == email).first()
    if not faculty or not verify_password(password, faculty.password):
        raise HTTPException(status_code=400, detail="Invalid Credentials")

    token = create_access_token({"sub": faculty.email})
    return {"access_token": token}


# Pydantic Schema
class FacultyCreate(BaseModel):
    email: EmailStr
    password: str


@app.post("/faculty/register")
def register_faculty(faculty: FacultyCreate, db: Session = Depends(get_db)):
    # Check if faculty already exists
    existing_faculty = db.query(Faculty).filter(Faculty.email == faculty.email).first()
    if existing_faculty:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(faculty.password)
    new_faculty = Faculty(email=faculty.email, password=hashed_password)
    db.add(new_faculty)
    db.commit()
    db.refresh(new_faculty)
    return {"message": "Faculty registered successfully"}


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/assignments/upload")
def upload_assignment(
    title: str, 
    description: str, 
    semester: str, 
    subject: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    faculty: Faculty = Depends(get_current_user)
):
    """
    Uploads an assignment. Only logged-in faculty can upload.
    """
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_assignment = Assignment(
        title=title,
        description=description,
        file_path=file_location,
        semester=semester,
        subject=subject,
        uploaded_by=faculty.id
    )
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)

    return {"message": "Assignment uploaded successfully!", "file_path": file_location}