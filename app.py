from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy  # Allow you to manage SQL from the flask web server

app = Flask(__name__)  # Variable receive the server
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/like_projects.db'
app.config['DEBUG'] = True  # Always refresh the page, if changes
database = SQLAlchemy(app)  # Allow you manage the database using SQLAlchemy syntax


class ProjectLike(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String)
    count = database.Column(database.Integer, default=0)
    liked_ips = database.Column(database.String)  # Stores IPs that have already been liked, separated by a comma


with app.app_context():
    database.create_all()
    database.session.commit()


@app.route('/')  # Initial Route to website
def home():
    like_data = ProjectLike.query.filter_by(id=1).first()
    if not like_data:
        like_data = ProjectLike(id=1, count=0, liked_ips="")  # If there is nothing in the db ID: 0,counter:0,empty IP
        database.session.add(like_data)
        database.session.commit()

    user_ip = request.remote_addr  # Checks if the current user has already liked
    already_liked = user_ip in like_data.liked_ips.split(",")

    return render_template("index.html", count=like_data.count, already_liked=already_liked)


@app.route('/increment', methods=['POST'])
def increment_like():
    like_data = ProjectLike.query.filter_by(id=1).first()
    user_ip = request.remote_addr  # Checks if the user has previously liked

    if user_ip not in like_data.liked_ips.split(","):
        like_data.count += 1
        like_data.liked_ips += f',{user_ip}'
        database.session.commit()

    return jsonify({'count': like_data.count})


if __name__ == '__main__':
    app.run()
