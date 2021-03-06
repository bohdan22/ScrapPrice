from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__,static_url_path = "/static", static_folder = "static")
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views,models