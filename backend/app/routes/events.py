from flask import Blueprint, request, jsonify, current_app
from ..db import db
from ..models import Event
from ..auth import require_admin
from datetime import datetime

events_bp = Blueprint("events", __name__)

@events_bp.route("", methods=["POST"])
@require_admin
def create_event():
    data = request.get_json() or {}
    required = ["college_id", "title"]
    for r in required:
        if r not in data:
            return jsonify({"error": f"{r} required"}), 400

    event = Event(
        college_id = data["college_id"],
        title = data["title"],
        description = data.get("description"),
        event_type = data.get("event_type"),
        capacity = data.get("capacity"),
        starts_at = _parse_dt(data.get("starts_at")),
        ends_at = _parse_dt(data.get("ends_at")),
        location = data.get("location"),
        status = data.get("status","scheduled"),
        created_by = data.get("created_by")
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({"id": event.id, "message": "event created"}), 201

@events_bp.route("", methods=["GET"])
def list_events():
    q = Event.query
    college_id = request.args.get("college_id")
    event_type = request.args.get("event_type")
    status = request.args.get("status")
    if college_id:
        q = q.filter_by(college_id=college_id)
    if event_type:
        q = q.filter_by(event_type=event_type)
    if status:
        q = q.filter_by(status=status)
    events = q.order_by(Event.starts_at.asc().nullsfirst()).all()
    out = []
    for e in events:
        out.append({
            "id": e.id, "title": e.title, "description": e.description,
            "event_type": e.event_type, "starts_at": e.starts_at.isoformat() if e.starts_at else None,
            "ends_at": e.ends_at.isoformat() if e.ends_at else None,
            "location": e.location, "status": e.status
        })
    return jsonify(out)

@events_bp.route("/<int:event_id>", methods=["GET"])
def get_event(event_id):
    e = Event.query.get_or_404(event_id)
    return jsonify({
        "id": e.id, "title": e.title, "description": e.description,
        "event_type": e.event_type, "starts_at": e.starts_at.isoformat() if e.starts_at else None,
        "ends_at": e.ends_at.isoformat() if e.ends_at else None,
        "location": e.location, "status": e.status
    })

@events_bp.route("/<int:event_id>/cancel", methods=["POST"])
@require_admin
def cancel_event(event_id):
    e = Event.query.get_or_404(event_id)
    e.status = "cancelled"
    db.session.commit()
    return jsonify({"message": "event cancelled"})

def _parse_dt(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None
