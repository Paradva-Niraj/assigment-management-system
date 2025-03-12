from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Faculty(Base):
    __tablename__ = 'faculties'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Assignment(Base):
    __tablename__ = 'assignments'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    file_path = Column(String)
    semester = Column(String)
    subject = Column(String)
    uploaded_by = Column(Integer, ForeignKey('faculties.id'))
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

class Submission(Base):
    __tablename__ = 'submissions'

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String)
    assignment_id = Column(Integer, ForeignKey('assignments.id'))
    file_path = Column(String)
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow)
