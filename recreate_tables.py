from src.app import create_app
from src.models import Resume, db

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()