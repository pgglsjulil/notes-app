import os
import secrets
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(32))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'notes.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
