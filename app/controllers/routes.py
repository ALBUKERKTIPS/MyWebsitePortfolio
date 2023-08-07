from app import app, database
from flask import render_template, request, jsonify, send_file, redirect, url_for
from app.models.tables_db import CardProject, Tasks
from werkzeug.utils import safe_join


@app.route('/index')  # Initial Route to WebSite
@app.route('/')
def index():
    data_projects = CardProject.query.all()  # Here me we collect all information in database about the Card Projects
    return render_template("index.html", data_projects=data_projects)  # We render the html with the variable info


@app.route('/liked', methods=['POST'])  # After the user like the card project
def like():
    project_id = request.form.get('project_id')
    if project_id:
        card_project = CardProject.query.get(project_id)
        if card_project:
            card_project.like_count += 1
            database.session.commit()
            return jsonify({'likes': card_project.like_count})
    return jsonify({'error': 'Project not found or invalid request'}), 400


@app.route('/download_curriculum')
def download_curriculum():
    curriculum_file_path = safe_join(app.root_path, 'static', 'files', 'Anderson Albuquerque 1.2.pdf')
    return send_file(curriculum_file_path, as_attachment=True)


@app.route('/tasks')
def home():
    all_tasks = Tasks.query.all()
    return render_template("tasksmanager.html", tasks_list=all_tasks)


@app.route('/create-task', methods=['POST'])
def create():
    task = Tasks(content=request.form['task-content'], done=False)
    database.session.add(task)
    database.session.commit()
    return redirect(url_for('home'))


@app.route('/delete-task/<id>')
def delete(id):
    deleting_task = Tasks.query.filter_by(id=int(id)).delete()
    database.session.commit()
    return redirect(url_for('home'))


@app.route('/task-done/<id>')
def done(id):
    done_task = Tasks.query.filter_by(id=int(id)).first()
    done_task.done = True
    database.session.commit()
    return redirect(url_for('home'))
