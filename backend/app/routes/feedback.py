from flask import Blueprint, request, jsonify
from ..db import db
from ..models import Feedback, Student, Event, Registration
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

feedback_bp = Blueprint("feedback", __name__)

@feedback_bp.route("/events/<int:event_id>/feedback", methods=["POST"])
def submit_feedback(event_id):
    data = request.get_json() or {}
    student_uid = data.get("student_uid")
    college_id = data.get("college_id")
    rating = data.get("rating")
    comments = data.get("comments")

    if not student_uid or not college_id or rating is None:
        return jsonify({"error": "student_uid, college_id and rating required"}), 400
    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            raise ValueError()
    except Exception:
        return jsonify({"error": "rating must be integer 1..5"}), 400

    student = Student.query.filter_by(college_id=college_id, student_uid=student_uid).first()
    if not student:
        return jsonify({"error": "student not found"}), 404

    # require registration (or attendance) optionally
    reg = Registration.query.filter_by(event_id=event_id, student_id=student.id).first()
    if not reg:
        return jsonify({"error": "student not registered for event"}), 400

    fb = Feedback(event_id=event_id, student_id=student.id, rating=rating, comments=comments)
    db.session.add(fb)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        existing = Feedback.query.filter_by(event_id=event_id, student_id=student.id).first()
        return jsonify({"message": "feedback already submitted", "feedback_id": existing.id}), 200

    return jsonify({"message": "feedback recorded", "feedback_id": fb.id}), 201


@feedback_bp.route("/events/<int:event_id>/feedbacks", methods=["GET"])
def list_feedbacks(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "event not found"}), 404

    rows = db.session.query(Feedback, Student).join(
        Student, Feedback.student_id == Student.id
    ).filter(Feedback.event_id == event_id).order_by(Feedback.submitted_at.desc()).all()

    out = []
    for fb, st in rows:
        out.append({
            "feedback_id": fb.id,
            "student_id": st.id,
            "student_uid": st.student_uid,
            "student_name": st.name,
            "rating": fb.rating,
            "comments": fb.comments,
            "submitted_at": fb.submitted_at.isoformat() if fb.submitted_at else None
        })

    avg_rating = db.session.query(func.avg(Feedback.rating)).filter(Feedback.event_id == event_id).scalar()
    feedback_count = db.session.query(func.count(Feedback.id)).filter(Feedback.event_id == event_id).scalar() or 0

    return jsonify({
        "avg_rating": float(avg_rating) if avg_rating is not None else None,
        "feedback_count": int(feedback_count),
        "feedbacks": out
    })
