from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy  # Allow you to manage SQL from the flask web server

app = Flask(__name__)  # Variable receive the server
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/likes.db'
app.config['DEBUG'] = True  # Always refresh the page, if changes
database = SQLAlchemy(app)  # Allow you manage the database using SQLAlchemy syntax


class CardProject(database.Model):
    __tablename__ = 'CardProject'  # Table name of database
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(100), nullable=False)
    description = database.Column(database.Text, nullable=False)
    github_link = database.Column(database.String(200))
    demo_link = database.Column(database.String(200))
    likes = database.Column(database.Integer, default=0)  # Likes


with app.app_context():
    database.create_all()
    database.session.commit()


@app.route('/')  # Initial Route to website
def home():
    return render_template("index.html")


app.run()
