import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("POSTGRES_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
