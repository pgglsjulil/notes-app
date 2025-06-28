import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(16)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'notes.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
