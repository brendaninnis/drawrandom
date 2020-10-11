from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, make_response
)
from werkzeug.exceptions import abort

from drawrandom.models import db, Item
from drawrandom.util import id_generator

bp = Blueprint('draw', __name__, url_prefix='/d')

@bp.route('/<key>', methods=('GET', 'POST'))
def draw(key):
    # Fetch an item from the list with key
    item = Item.query.filter(Item.listkey == key).filter(Item.assignee == None).first()

    if item is None:
        abort(404, "This list is empty")

    if request.method == 'POST':
        response = make_response(render_template('draw.html', item=item.name))

        # Give this person a name and assing them to the item
        username = request.cookies.get('username')
        if username is None:
            username = id_generator()
            response.set_cookie('username', username)

        item.assignee = username
        db.session.commit()
        return response
    else:
        return render_template('getdraw.html', key=key)

