from flask import Blueprint, request, jsonify
from ..db import db
from ..models import Event, Registration, Attendance, Feedback, Student
from sqlalchemy import func

reports_bp = Blueprint("reports", __name__)

@reports_bp.route("/event_popularity", methods=["GET"])
def event_popularity():
    college_id = request.args.get("college_id")
    event_type = request.args.get("event_type")

    q = db.session.query(
        Event.id, Event.title, Event.event_type, func.count(Registration.id).label("registrations")
    ).outerjoin(Registration, Registration.event_id == Event.id).group_by(Event.id)

    if college_id:
        q = q.filter(Event.college_id == college_id)
    if event_type:
        q = q.filter(Event.event_type == event_type)

    q = q.order_by(func.count(Registration.id).desc())
    results = q.all()
    out = [{"event_id": r.id, "title": r.title, "event_type": r.event_type, "registrations": int(r.registrations)} for r in results]
    return jsonify(out)

@reports_bp.route("/event/<int:event_id>/summary", methods=["GET"])
def event_summary(event_id):
    reg_count = db.session.query(func.count(Registration.id)).filter(Registration.event_id == event_id).scalar() or 0
    att_count = db.session.query(func.count(Attendance.id)).filter(Attendance.event_id == event_id).scalar() or 0
    avg_rating = db.session.query(func.avg(Feedback.rating)).filter(Feedback.event_id == event_id).scalar()
    feedback_count = db.session.query(func.count(Feedback.id)).filter(Feedback.event_id == event_id).scalar() or 0
    attendance_pct = (att_count / reg_count * 100) if reg_count > 0 else 0.0
    return jsonify({
        "event_id": event_id,
        "registrations": int(reg_count),
        "attendees": int(att_count),
        "attendance_pct": round(attendance_pct,2),
        "avg_rating": float(avg_rating) if avg_rating is not None else None,
        "feedback_count": int(feedback_count)
    })

@reports_bp.route("/student_participation", methods=["GET"])
def student_participation():
    college_id = request.args.get("college_id")
    q = db.session.query(
        Student.id, Student.student_uid, Student.name, func.count(Attendance.id).label("events_attended")
    ).outerjoin(Attendance, Attendance.student_id == Student.id).group_by(Student.id)

    if college_id:
        q = q.filter(Student.college_id == college_id)

    q = q.order_by(func.count(Attendance.id).desc())
    results = q.all()
    out = [{"student_id": r.id, "student_uid": r.student_uid, "name": r.name, "events_attended": int(r.events_attended)} for r in results]
    return jsonify(out)

@reports_bp.route("/most_active_students", methods=["GET"])
def most_active_students():
    college_id = request.args.get("college_id")
    limit = int(request.args.get("limit", 3))
    q = db.session.query(
        Student.id, Student.student_uid, Student.name, func.count(Attendance.id).label("events_attended")
    ).join(Attendance, Attendance.student_id == Student.id).group_by(Student.id)

    if college_id:
        q = q.filter(Student.college_id == college_id)

    q = q.order_by(func.count(Attendance.id).desc()).limit(limit)
    results = q.all()
    out = [{"student_id": r.id, "student_uid": r.student_uid, "name": r.name, "events_attended": int(r.events_attended)} for r in results]
    return jsonify(out)
