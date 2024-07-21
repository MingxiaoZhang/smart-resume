from flask_cors import CORS
from src.main import create_app

app = create_app()
CORS(app)