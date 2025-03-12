from fastapi import APIRouter, UploadFile, File, Depends
from .database import SessionLocal
from .models import Assignment
import shutil

router = APIRouter()

@router.post("/upload-assignment/")
def upload_assignment(
    title: str, subject: str, semester: str, 
    file: UploadFile = File(...), db: Session = SessionLocal()
):
    file_path = f"media/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    assignment = Assignment(
        title=title,
        subject=subject,
        semester=semester,
        file_path=file_path
    )
    db.add(assignment)
    db.commit()
    return {"message": "Assignment Uploaded Successfully"}
