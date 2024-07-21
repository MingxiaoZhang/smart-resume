from api.src.main import create_app
from api.src.models import Resume, db

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()