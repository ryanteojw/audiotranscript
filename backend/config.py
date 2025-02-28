import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.getenv("DB_PATH", os.path.join(BASE_DIR, "audio_db.db"))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
