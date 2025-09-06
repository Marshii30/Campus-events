from .db import db
from datetime import datetime

class College(db.Model):
    __tablename__ = "colleges"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    domain = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    students = db.relationship("Student", backref="college", cascade="all, delete-orphan")
    events = db.relationship("Event", backref="college", cascade="all, delete-orphan")

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.Integer, db.ForeignKey("colleges.id", ondelete="CASCADE"), nullable=False)
    student_uid = db.Column(db.String(64), nullable=False)  # roll number / uid
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('college_id', 'student_uid', name='uq_student_uid_college'),)

class Admin(db.Model):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.Integer, db.ForeignKey("colleges.id"), nullable=False)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    token = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    college_id = db.Column(db.Integer, db.ForeignKey("colleges.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(50))
    capacity = db.Column(db.Integer)
    starts_at = db.Column(db.DateTime)
    ends_at = db.Column(db.DateTime)
    location = db.Column(db.String(255))
    status = db.Column(db.String(20), default="scheduled")  # scheduled|cancelled|completed
    created_by = db.Column(db.Integer)  # admin id
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Registration(db.Model):
    __tablename__ = "registrations"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    event_id = db.Column(db.BigInteger, db.ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="registered")

    __table_args__ = (db.UniqueConstraint('event_id', 'student_id', name='uq_event_student'),)

class Attendance(db.Model):
    __tablename__ = "attendances"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    event_id = db.Column(db.BigInteger, db.ForeignKey("events.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    checkin_at = db.Column(db.DateTime, default=datetime.utcnow)
    method = db.Column(db.String(20), default="manual")

    __table_args__ = (db.UniqueConstraint('event_id', 'student_id', name='uq_attendance_event_student'),)

class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    event_id = db.Column(db.BigInteger, db.ForeignKey("events.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    rating = db.Column(db.SmallInteger, nullable=False)  # 1..5
    comments = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('event_id', 'student_id', name='uq_feedback_event_student'),)
