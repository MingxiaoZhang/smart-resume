from api.app import app
from api.models import db

with app.app_context():
    db.create_all()
