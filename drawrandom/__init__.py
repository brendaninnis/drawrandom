import os
import random

from flask import (
    Flask, render_template, request, flash, url_for
)
from drawrandom.util import id_generator
from drawrandom.models import db, List, Item

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
            if not listinput:
                error = 'Enter some items in the list'

            listarray = listinput.replace('\r', '').split('\n')
            listarray = list(filter(('').__ne__, listarray))
            random.shuffle(listarray)
            if len(listarray) < 2 and not error:
                error = 'Enter more than 1 item in the list'

            if error is not None:
                flash(error)
            else:
                key = id_generator()
                response = render_template('link.html', link=url_for('draw.draw', key=key, _external=True))

                # Give this person a name and assing them to the item
                username = request.cookies.get('username')
                if username is None:
                    username = id_generator()
                    response.set_cookie('username', username)

                newlist = List(key=key, creator=username)
                db.session.add(newlist)
                db.session.commit()

                newitems = []
                for item in listarray:
                    newitems.append(Item(listkey=key, name=item))
                db.session.add_all(newitems)
                db.session.commit()

                return response

        response = render_template('create.html', listarray=listarray)
        return response

    from . import draw
    app.register_blueprint(draw.bp)

    db.init_app(app)

    return app
