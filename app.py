from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy  # Allow you to manage SQL from the flask web server
from sqlalchemy import event
import json


app = Flask(__name__)  # Variable receive the server
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/like_projects.db'
app.config['DEBUG'] = True  # Always refresh the page, if changes
database = SQLAlchemy(app)  # Allow you manage the database using SQLAlchemy syntax


class ProjectLike(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    image_url = database.Column(database.String)
    title = database.Column(database.String)
    legend = database.Column(database.String)
    count = database.Column(database.Integer, default=0)
    liked_ips = database.Column(database.String, default=" ")  # Stores IPs that have already been liked


@event.listens_for(ProjectLike.liked_ips, "set", retval=True)
def set_liked_ips(target, value, oldvalue, initiator):
    # If the value being set is None, return an empty string instead
    return value if value is not None else ""


with app.app_context():
    database.create_all()
    database.session.commit()


@app.route('/')  # Initial Route to website
def home():
    projects = ProjectLike.query.all()
    return render_template("index.html", projects=projects)


@app.route('/increment', methods=['POST'])
def increment_like():
    project_id = request.form.get('project_id')
    if not project_id:
        return 'Invalid project_id', 400

    try:
        project_id = int(project_id)
    except (ValueError, TypeError):
        return 'Invalid project_id', 400

    like_data = ProjectLike.query.get(project_id)
    if not like_data:
        return 'Project not found', 404

    # Use the proxy-provided header for the user's IP address if available
    user_ip = request.headers.get('X-Forwarded-For') or request.headers.get('X-Real-IP') or request.remote_addr

    try:
        liked_ips_list = json.loads(like_data.liked_ips)  # Convert the liked_ips from JSON to a Python list
    except json.JSONDecodeError:
        liked_ips_list = []

    if user_ip not in liked_ips_list:
        liked_ips_list.append(user_ip)
        like_data.count += 1

    like_data.liked_ips = json.dumps(liked_ips_list)  # Convert liked_ips list to JSON before storing in the database

    database.session.commit()

    return jsonify({'count': like_data.count})


if __name__ == '__main__':
    app.run()
