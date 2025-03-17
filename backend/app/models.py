from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base,engine
import datetime
from passlib.context import CryptContext

# Create database tables
Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Faculty(Base):
    __tablename__ = "faculty"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    prn = Column(String, unique=True, index=True)
    name = Column(String)
    semester = Column(String)
    password = Column(String)

class Assignment(Base):
    __tablename__ = 'assignments'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    file_path = Column(String)
    semester = Column(String)
    subject = Column(String)
    uploaded_by = Column(String)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

class Submission(Base):
    __tablename__ = 'submissions'

    id = Column(Integer, primary_key=True, index=True)
    student_prn = Column(String, ForeignKey('students.prn'))  # Store PRN instead of name
    assignment_id = Column(Integer, ForeignKey('assignments.id'))
    file_path = Column(String)
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow)
    student = relationship("Student")
    assignment = relationship("Assignment")