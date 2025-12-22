import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

db_url = os.getenv('DATABASE_URL', 'sqlite:///site.db')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'gigel')
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'
    SQLALCHEMY_DATABASE_URI = db_url.replace("sqlite:///", f"sqlite:///{BASE_DIR}/")
    SQLALCHEMY_TRACK_MODIFICATIONS = False