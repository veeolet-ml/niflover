from flask import render_template
from flask_login import login_required, current_user
from . import bp

@bp.get('/')
@login_required
def index():
    return render_template('main/index.html')