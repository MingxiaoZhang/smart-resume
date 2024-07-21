import json
from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from src.config import Config
from src.models import db
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    jwt = JWTManager(app)

    from src.routes.auth import auth
    from src.routes.education import education
    from src.routes.resume import resume
    from src.routes.project import project
    from src.routes.experience import experience
    from src.routes.user import user

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(education, url_prefix='/profile')
    app.register_blueprint(experience, url_prefix='/profile')
    app.register_blueprint(user, url_prefix='/profile')
    app.register_blueprint(project, url_prefix='/profile')
    app.register_blueprint(resume, url_prefix='/resume')

    return app