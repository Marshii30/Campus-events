import os
from flask import Flask, jsonify
from .config import Config
from .db import db, migrate
from .routes import register_routes
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Allow cross origin for development
    CORS(app)

    # init db + migrations
    db.init_app(app)
    migrate.init_app(app, db)

    # register routes blueprint(s)
    register_routes(app)

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "not found"}), 404

    return app
