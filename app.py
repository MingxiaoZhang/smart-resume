from flask_cors import CORS
from src.main import create_app

app = create_app()
CORS(app, origins="http://localhost:3000", supports_credentials=True, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])