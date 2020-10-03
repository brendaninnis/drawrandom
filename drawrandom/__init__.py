import os
import random
import string

from flask import (
    Flask, render_template, request, flash
)
from drawrandom.db import get_db


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'drawrandom.sqlite'),
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

    # index page
    @app.route('/', methods=('GET', 'POST'))
    def hello():
        listarray = ['Apples', 'Oranges', 'Snakes']
        if request.method == 'POST':
            error = None
            listinput = request.form['list']
            print(listinput)
            if not listinput:
                error = 'Enter some items in the list'

            listarray = listinput.replace('\r', '').split('\n')
            listarray = list(filter(('').__ne__, listarray))
            random.shuffle(listarray)
            print(listarray)
            if len(listarray) < 2 and not error:
                error = 'Enter more than 1 item in the list'

            if error is not None:
                flash(error)
            else:
                key = id_generator()
                query = 'INSERT INTO list (key) VALUES ' + key
                db = get_db()
                db.execute(query)
                query = 'INSERT INTO item (name, list) VALUES '
                for item in listarray:
                    query += '(' + item + ',' + key + ')'
                db.execute(query)
                db.commit()
                return render_template('link.html', key=key)

        return render_template('create.html', listarray=listarray)

    from . import draw
    app.register_blueprint(draw.bp)

    from . import db
    db.init_app(app)

    return app
