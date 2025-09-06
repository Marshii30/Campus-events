from .db import db
from .models import College, Student, Event, Admin
from datetime import datetime, timedelta

def seed_sample_data(app):
    with app.app_context():
        if College.query.count() == 0:
            c = College(name="Demo College", domain="demo.edu")
            db.session.add(c)
            db.session.commit()
        else:
            c = College.query.first()

        if Admin.query.filter_by(email="admin@demo.edu").first() is None:
            a = Admin(college_id=c.id, name="Demo Admin", email="admin@demo.edu", token=app.config.get("ADMIN_TOKEN"))
            db.session.add(a)
            db.session.commit()

        if Event.query.count() == 0:
            e1 = Event(
                college_id=c.id,
                title="Intro to Robotics",
                description="Workshop on robotics basics",
                event_type="Workshop",
                capacity=100,
                starts_at=datetime.utcnow() + timedelta(days=3),
                ends_at=datetime.utcnow() + timedelta(days=3, hours=2),
                location="Auditorium"
            )
            e2 = Event(
                college_id=c.id,
                title="Hack Night",
                description="24h hackathon",
                event_type="Hackathon",
                capacity=200,
                starts_at=datetime.utcnow() + timedelta(days=7),
                ends_at=datetime.utcnow() + timedelta(days=8),
                location="Lab 1"
            )
            db.session.add_all([e1,e2])
            db.session.commit()
