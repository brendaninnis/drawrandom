from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from drawrandom.db import get_db

bp = Blueprint('draw', __name__, url_prefix='/d')
