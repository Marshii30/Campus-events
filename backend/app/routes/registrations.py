from flask import Blueprint, request, jsonify
from ..db import db
from ..models import Student, Registration, Event
from sqlalchemy.exc import IntegrityError

registrations_bp = Blueprint("registrations", __name__)

@registrations_bp.route("/events/<int:event_id>/register", methods=["POST"])
def register_event(event_id):
    data = request.get_json() or {}
    student_uid = data.get("student_uid")
    college_id = data.get("college_id")
    if not student_uid or not college_id:
        return jsonify({"error": "student_uid and college_id required"}), 400

    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "event not found"}), 404
    if event.status == "cancelled":
        return jsonify({"error": "event cancelled"}), 400

    student = Student.query.filter_by(college_id=college_id, student_uid=student_uid).first()
    if not student:
        student = Student(
            college_id=college_id,
            student_uid=student_uid,
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone")
        )
        db.session.add(student)
        db.session.flush()  # to get id for registration

    reg = Registration(event_id=event_id, student_id=student.id)
    db.session.add(reg)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        existing = Registration.query.filter_by(event_id=event_id, student_id=student.id).first()
        return jsonify({"message": "already registered", "registration_id": existing.id}), 200

    return jsonify({"message": "registered", "registration_id": reg.id}), 201

@registrations_bp.route("/students/<int:student_id>/registrations", methods=["GET"])
def student_regs(student_id):
    regs = Registration.query.filter_by(student_id=student_id).all()
    out = []
    for r in regs:
        out.append({
            "registration_id": r.id,
            "event_id": r.event_id,
            "registered_at": r.registered_at.isoformat(),
            "status": r.status
        })
    return jsonify(out)
