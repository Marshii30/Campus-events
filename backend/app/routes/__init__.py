from .events import events_bp
from .registrations import registrations_bp
from .attendance import attendance_bp
from .feedback import feedback_bp
from .reports import reports_bp

def register_routes(app):
    app.register_blueprint(events_bp, url_prefix="/api/v1/events")
    app.register_blueprint(registrations_bp, url_prefix="/api/v1")
    app.register_blueprint(attendance_bp, url_prefix="/api/v1")
    app.register_blueprint(feedback_bp, url_prefix="/api/v1")
    app.register_blueprint(reports_bp, url_prefix="/api/v1/reports")
