from flask import request, current_app, jsonify
from functools import wraps

def require_admin(func):
    @wraps(func)
    def inner(*args, **kwargs):
        token = request.headers.get("X-Admin-Token") or request.args.get("admin_token")
        if not token:
            return jsonify({"error": "admin token required"}), 401
        if token != current_app.config.get("ADMIN_TOKEN"):
            return jsonify({"error": "invalid admin token"}), 403
        return func(*args, **kwargs)
    return inner
