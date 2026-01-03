import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

db_url = os.getenv('DATABASE_URL', 'sqlite:///site.db')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'gigel')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'

    SQLALCHEMY_DATABASE_URI = db_url.replace("sqlite:///", f"sqlite:///{BASE_DIR}/")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WTF_CSRF_ENABLED = True

    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads/user_photos')
    MAX_PHOTOS = int(os.getenv('MAX_PHOTOS', '4'))
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit for uploads