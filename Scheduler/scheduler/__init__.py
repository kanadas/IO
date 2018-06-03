import os

from scheduler.db import get_db
from scheduler.static.consts import states
from . import db
from flask import Flask, render_template, redirect, request


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
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



@app.route('/load_states')
def load_states():
    dbs = get_db()
    dbs.execute(
        'DELETE FROM state'
    )
    for state in states:
        dbs.execute(
            'INSERT INTO state (name)'
            ' VALUES (?)',
            [state]
        )

    dbs.commit()
    return redirect('/tasks')


@app.route('/tasks', methods=('GET', 'POST'))
def tasks():
    dbs = get_db()

    if request.method == 'POST':
        tracking_id = request.form['tracking_id']
        url = request.form['url']
        time = request.form['time']
        visits = request.form['visits']
        date = request.form['date']
        dbs.execute(
            'INSERT INTO task (tracking_id, url, generating_time, state_name, visits, start_time)'
            ' VALUES (?, ?, ?, ?, ?, ?)',
            (tracking_id, url, time, 'NEW', visits, date)
        )
        dbs.commit()

    all_tasks = dbs.execute(
        'SELECT tracking_id'
        ' FROM task'
    ).fetchall()

    return render_template('display_tasks.html', tasks=all_tasks)
