from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from sqlalchemy import or_
from . import bp
from app.extensions import db
from app.models import User, Match, Message
from .utils import is_participant, other_participant
from sqlalchemy.orm import selectinload

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
        .order_by(Match.created_at.desc())
        .all()
    )

    other_by_match = {m.id: other_participant(m, current_user.id) for m in matches}

    # matched_users = []
    # for m in matches:
    #     other_id = m.user_b_id if m.user_a_id == current_user.id else m.user_a_id
    #     other_user = User.query.get(other_id)
    #     if other_user:
    #         matched_users.append(other_user)

    return render_template(
        "matches/matches.html",
        matches=matches,
        other_by_match=other_by_match,
        active_match=None,
        other_user=None
    )

@bp.route("/<int:match_id>", methods=["GET", "POST"])
@login_required
def match_thread(match_id):
    matches = (
        Match.query
        .filter(or_(
            Match.user_a_id == current_user.id,
            Match.user_b_id == current_user.id
        ))
        .order_by(Match.created_at.desc())
        .all()
    )

    other_by_match = {m.id: other_participant(m, current_user.id) for m in matches}

    active_match = (
        Match.query.options(selectinload(Match.messages))
        .get_or_404(match_id)
    )

    if not is_participant(active_match, current_user.id):
        abort(403)
    
    other_user = other_participant(active_match, current_user.id)

    if request.method == "POST":
        body = request.form.get("body", "").strip()
        if not body:
            flash("Message cannot be empty.", "warning")
            return redirect(url_for("matches.match_thread", match_id=match_id))
        
        msg = Message(
            match_id=active_match.id,
            sender_id=current_user.id,
            body=body
        )

        db.session.add(msg)
        db.session.commit()

        return redirect(url_for("matches.match_thread", match_id=match_id))
    
    return render_template(
        "matches/matches.html",
        matches=matches,
        other_by_match=other_by_match,
        active_match=active_match,
        other_user=other_user
    )

    