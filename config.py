import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'ztztopia'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'notes.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False