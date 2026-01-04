from flask import render_template, redirect, url_for, flash, session, request
from flask_login import login_required, current_user
from sqlalchemy import or_
from . import bp

from app.extensions import db
from app.models import User, UserAction, ActionType
from app.models import Match
from .utils import feed_ids, pop_next_feed_id, remove_feed_id, ensure_match

@bp.get('/')
@login_required
def index():
    if not session.get('feed_ids'):
        session['feed_ids'] = feed_ids()
    
    candidate_id = pop_next_feed_id()
    candidate = User.query.get(candidate_id) if candidate_id else None

    return render_template('main/index.html', candidate=candidate)

@bp.get("/matches")
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
        "main/matches.html",
        matched_users=matched_users
    )


@bp.post('/like/<int:target_id>')
@login_required
def like_user(target_id):
    if target_id == current_user.id:
        return redirect(url_for('main.index'))
    
    user_action = UserAction.query.filter_by(actor_id=current_user.id, target_id=target_id).first()
    if user_action is None:
        user_action = UserAction(
            actor_id=current_user.id,
            target_id=target_id,
            action=ActionType.LIKE
        )
        db.session.add(user_action)
    else:
        user_action.action = ActionType.LIKE

    mutual = UserAction.query.filter_by(
        actor_id=target_id,
        target_id=current_user.id,
        action=ActionType.LIKE
    ).first()

    if mutual:
        ensure_match(current_user.id, target_id)
        flash('It\'s a match!', 'success')
    
    remove_feed_id(target_id)
    db.session.commit()
    return redirect(url_for('main.index'))

@bp.post('/pass/<int:target_id>')
@login_required
def pass_user(target_id):
    if target_id == current_user.id:
        return redirect(url_for('main.index'))
    
    user_action = UserAction.query.filter_by(actor_id=current_user.id, target_id=target_id).first()
    if user_action is None:
        user_action = UserAction(
            actor_id=current_user.id,
            target_id=target_id,
            action=ActionType.PASS
        )
        db.session.add(user_action)
    else:
        user_action.action = ActionType.PASS

    remove_feed_id(target_id)
    db.session.commit()
    return redirect(url_for('main.index'))