from flask import Blueprint, request, jsonify
from ..db import db
from ..models import Event, Student, Registration, Attendance
from sqlalchemy.exc import IntegrityError

attendance_bp = Blueprint("attendance", __name__)

@attendance_bp.route("/events/<int:event_id>/attendance", methods=["POST"])
def mark_attendance(event_id):
    data = request.get_json() or {}
    student_uid = data.get("student_uid")
    college_id = data.get("college_id")
    method = data.get("method", "manual")

    if not student_uid or not college_id:
        return jsonify({"error": "student_uid and college_id required"}), 400

    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "event not found"}), 404
    if event.status == "cancelled":
        return jsonify({"error": "event cancelled"}), 400

    student = Student.query.filter_by(college_id=college_id, student_uid=student_uid).first()
    if not student:
        return jsonify({"error": "student not found, register first"}), 404

    # ensure registration exists; if not, create it (auto-register / walk-in)
    reg = Registration.query.filter_by(event_id=event_id, student_id=student.id).first()
    if not reg:
        try:
            reg = Registration(event_id=event_id, student_id=student.id)
            db.session.add(reg)
            db.session.flush()
        except Exception:
            db.session.rollback()
            return jsonify({"error": "failed to create registration"}), 500

    att = Attendance(event_id=event_id, student_id=student.id, method=method)
    db.session.add(att)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        existing = Attendance.query.filter_by(event_id=event_id, student_id=student.id).first()
        return jsonify({"message": "already checked-in", "attendance_id": existing.id}), 200

    return jsonify({"message": "attendance marked", "attendance_id": att.id}), 201
