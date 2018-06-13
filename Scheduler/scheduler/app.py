import os

from datetime import datetime
from scheduler.db import get_db
from . import db
from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
import requests


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    Bootstrap(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'scheduler.sqlite'),
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

        # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    return app


app = create_app()


@app.route('/tasks', methods=('GET', 'POST'))
def tasks():
    dbs = get_db()

    if request.method == 'POST':
        cursor = dbs.cursor()
        cursor.execute(
            'INSERT INTO task (tracking_id, url, generating_time, state_name, visits, start_time)'
            ' VALUES (?, ?, ?, ?, ?, ?)',
            ('', '', '', 'NEW', '', '')
        )

        task_id = cursor.lastrowid

        dbs.commit()

        return redirect('/tasks/%d' % task_id)

    else:
        all_tasks = dbs.execute(
            'SELECT task_id, tracking_id, state_name'
            ' FROM task'
        ).fetchall()

        return render_template('display_tasks.html', tasks=all_tasks)


def edit_template(dbs, task_id, errors):
    all_tasks = dbs.execute(
        'SELECT task_id, tracking_id, state_name'
        ' FROM task'
    ).fetchall()

    current_task = dbs.execute(
        'SELECT task_id, tracking_id, url, generating_time, visits, start_time, state_name'
        ' FROM task'
        ' WHERE task_id=?', (task_id,)
    ).fetchone()

    if current_task['start_time']:
        current_task['start_time'] = datetime.strptime(current_task['start_time'], "%Y-%m-%d %H:%M:%S")
        current_task['start_time'] = datetime.strftime(current_task['start_time'], "%Y-%m-%dT%H:%M")

    modify = (current_task['state_name'] == 'DONE' or current_task['state_name'] == 'CANCELED'
                or current_task['state_name'] == 'DELETED' or current_task['state_name'] == 'IN_PROGRESS')

    return render_template('edit_task.html', tasks=all_tasks, current_task=current_task, errors=errors, modify=modify)


@app.route('/tasks/<task_id>', methods=['POST', 'GET'])
def task(task_id):
    dbs = get_db()

    if request.method == 'POST':
        tracking_id = request.form['tracking_id']
        url = request.form['url']
        time = request.form['time']
        visits = request.form['visits']
        date = datetime.strptime(request.form['date'], "%Y-%m-%dT%H:%M")
        errors = None

        try:
             response = requests.post("https://www.google-analytics.com/debug/collect", data={
                 "tid": tracking_id,
                 "dp": url,
                 "v": 1,
                 "cid": 1
             }, timeout=60)
        except (requests.Timeout, requests.ConnectionError):
            errors = "Connection problem encountered - try again or go cry"
        
        if not response.json()["hitParsingResult"][0]["valid"]:
            errors = "Wrong tracking_id"
    
        if errors:
            return edit_template(dbs, task_id, errors)

        task = dbs.execute('SELECT state_name FROM task WHERE task_id=?', (task_id,)).fetchone()

        if task['state_name'] == 'NEW' or task['state_name'] == 'READY':
            dbs.execute(
                'UPDATE task SET tracking_id=?, url=?, generating_time=?, state_name=?, visits=?, start_time=?'
                ' WHERE task_id=?',
                (tracking_id, url, time, 'READY', visits, date, task_id)
            )
            dbs.commit()

            return redirect('/tasks')
        elif task['state_name'] == 'IN_PROGRESS':
            errors = "You can't modify task in progress"
            return edit_template(dbs, task_id, errors)
    else:
        return edit_template(dbs, task_id, None)
        

@app.route('/remove_tasks/<state>/<int:task_id>')
def remove_task(state, task_id):
    dbs = get_db()
    if state in ['DELETED', 'ERROR', 'CANCELED', 'DONE']:
        dbs.execute(
            'DELETE FROM task'
            ' WHERE task_id=?', (task_id,)
        )
    elif state in ['READY', 'IN_PROGRESS']:
        new_state = ''
        if state == 'READY':
            new_state = "DELETED"
        if state == 'IN_PROGRESS':
            new_state = 'CANCELED'
        dbs.execute(
            'UPDATE task SET state_name=?'
            'WHERE task_id=?',
            (new_state, task_id)
        )
    dbs.commit()
    return redirect('/tasks')


@app.route('/clear_tasks')
def clear_tasks():
    dbs = get_db()
    dbs.execute(
        'DELETE FROM task'
    )
    dbs.commit()
    return redirect('/tasks')
