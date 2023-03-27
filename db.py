from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from sqlalchemy.sql import text

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
