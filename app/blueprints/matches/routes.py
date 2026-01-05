from flask import render_template
from flask_login import login_required, current_user
from sqlalchemy import or_
from . import bp
from app.extensions import db
from app.models import User, Match

@bp.get("/")
@login_required
def matches():
    """
    List all users the current user has matched with.
    """
    matches = (
        Match.query
        .filter(or_(
            Match.user_a_id == current_user.id,
            Match.user_b_id == current_user.id
        ))
        .all()
    )

    matched_users = []
    for m in matches:
        other_id = m.user_b_id if m.user_a_id == current_user.id else m.user_a_id
        other_user = User.query.get(other_id)
        if other_user:
            matched_users.append(other_user)

    return render_template(
        "matches/matches.html",
        matched_users=matched_users
    )