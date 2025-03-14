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

    prn = Column(String, primary_key=True, unique=True, index=True)  # PRN as unique ID
    name = Column(String, nullable=False)
    semester = Column(String, nullable=False)
    password = Column(String, nullable=False)  # Hashed password

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.password)

    def set_password(self, plain_password):
        self.password = pwd_context.hash(plain_password)

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
    student_name = Column(String)
    assignment_id = Column(Integer, ForeignKey('assignments.id'))
    file_path = Column(String)
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow)
