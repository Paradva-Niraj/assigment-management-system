from fastapi import FastAPI, Depends, HTTPException, File, UploadFile,status,Form
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
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

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

# Upload Assignment File
UPLOAD_FOLDER = "uploads/assignments/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/faculty/upload_assignment/")
async def upload_assignment(
    title: str = Form(...),
    description: str = Form(...),
    semester: str = Form(...),
    subject: str = Form(...),
    uploaded_by: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Generate safe file path
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        # Read and write file safely
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Save to database
        new_assignment = Assignment(
            title=title,
            description=description,
            semester=semester,
            subject=subject,
            uploaded_by=uploaded_by,
            file_path=file_path
        )
        db.add(new_assignment)
        db.commit()
        db.refresh(new_assignment)

        return {"message": "Assignment uploaded successfully", "file_path": file_path}
    
    except Exception as e:
        return {"error": f"Upload failed: {str(e)}"}

@app.get("/faculty/{email}/assignments")
def get_faculty_assignments(email: str, db: Session = Depends(get_db)):
    assignments = db.query(Assignment).filter(Assignment.uploaded_by == email).all()
    # if not assignments:
        # return {"message": "No assignments found"}
    return assignments


@app.delete("/faculty/delete_assignment/{assignment_id}")
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # Delete file from server (optional)
    import os
    if os.path.exists(assignment.file_path):
        os.remove(assignment.file_path)

    db.delete(assignment)
    db.commit()

    return {"message": "Assignment deleted successfully"}