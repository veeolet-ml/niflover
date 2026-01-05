from flask import Blueprint

bp = Blueprint('matches', __name__, template_folder='templates', url_prefix='/matches')

from . import routes