from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # Variable receive the server, all flask is content inside this
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/storage.db'
app.config['DEBUG'] = True
database = SQLAlchemy(app)

from app.controllers import default
