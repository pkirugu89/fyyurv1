import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
class DbConfig:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:p0l07x@localhost:5432/fyyur_app'
