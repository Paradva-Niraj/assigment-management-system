from fastapi import FastAPI, Depends, HTTPException, File, UploadFile,status,Form
from fastapi.params import Body
# from.database import engine, SessionLocal
from .models import Base, Faculty, Assignment, Submission, Student
from .auth import create_access_token, hash_password, verify_password, get_current_user
# from sqlalchemy.orm import Session
# from pydantic import BaseModel

# from.models import Faculty
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, EmailStr
from .database import Base,engine,SessionLocal,get_password_hash
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime

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

Base.metadata.create_all(bind=engine)

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


class StudentCreate(BaseModel):
    name: str
    semester: str
    password: str

def generate_prn(db: Session) -> str:
    try:
        current_year = datetime.now().year % 100
        student_count = db.query(Student).count() + 1
        # Debug student count
        print(f"Student Count: {student_count}")  # Debugging
        prn_number = f"80{current_year}{student_count:03d}"
        print(f"Generated PRN: {prn_number}")  # Debugging
        return prn_number
    except Exception as e:
        print(f"PRN Generation Error: {e}")
        raise

@app.post("/student/register")
def register_student(student: StudentCreate, db: Session = Depends(get_db)):
    # Generate PRN
    prn = generate_prn(db)
    hashed_password = get_password_hash(student.password)
    
    new_student = Student(prn=prn, name=student.name, semester=student.semester, password=hashed_password)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    
    return {"message": "Student registered successfully", "prn": prn}

class StudentLogin(BaseModel):
    prn: str
    password: str

@app.post("/student/login")
def student_login(student: StudentLogin, db: Session = Depends(get_db)):
    student_record = db.query(Student).filter(Student.prn == student.prn).first()
    
    if not student_record or not verify_password(student.password, student_record.password):
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    
    token = create_access_token({"sub": student_record.prn})
    return {"access_token": token, "semester": student_record.semester}

@app.get("/student/{semester}/assignments")
def get_assignments(semester: str, db: Session = Depends(get_db)):
    """
    Fetch assignments for a student based on their PRN and semester.
    """
    assignments = db.query(Assignment).filter(Assignment.semester == semester).all()

    if not assignments:
        raise HTTPException(status_code=404, detail="No assignments found")

    return [{"id": a.id, "title": a.title, "subject": a.subject, "description": a.description, "file_path": a.file_path} for a in assignments]
    
@app.get("{file_path:path}")
def download_file(file_path: str):
    file_location = os.path.join("uploads", file_path)  # Ensure correct folder
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_location)