from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student') # 'admin' or 'student'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    student_details = db.relationship('StudentDetails', backref='user', uselist=False, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    link = db.Column(db.String(255)) # Link to course materials/video
    credits = db.Column(db.Integer, nullable=False)
    seats = db.Column(db.Integer, nullable=False, default=30)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='course', lazy=True, cascade="all, delete-orphan")

class StudentDetails(db.Model):
    __tablename__ = 'student_details'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    enrollment_no = db.Column(db.String(50), unique=True, nullable=True) # Generated after approval or registration
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    dob = db.Column(db.Date)
    profile_image = db.Column(db.String(255)) # Path to profile image
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='student_details', lazy=True, cascade="all, delete-orphan")

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_details.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    date_enrolled = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='enrolled') # 'enrolled', 'completed', 'dropped'

    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', name='_student_course_uc'),)
