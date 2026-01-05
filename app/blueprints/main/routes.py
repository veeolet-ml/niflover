import subprocess
import sys
from pathlib import Path

from flask import render_template, redirect, url_for, flash, session, request, current_app
from flask_login import login_required, current_user
from sqlalchemy import or_

from . import bp

from app.extensions import db
from app.models import User, UserAction, ActionType, Match, Game, UserGameStat
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

@bp.post('/game/submit_score')
def submit_game_score():
    print("Content-Type:", request.content_type)
    print("Raw body:", request.get_data(as_text=True))
    print("JSON parsed:", request.get_json(silent=True))

    data = request.get_json(silent=True) or {}
    score = data.get('score')
    slug = data.get('slug')
    username = data.get('username')
    print(score, slug, username)

    if score is None or score < 0:
        print('Invalid score submitted')
        flash('Invalid score submitted.', 'danger')
        return redirect(url_for('main.index'))
    
    if not slug:
        print('Invalid game identifier')
        flash('Invalid game identifier.', 'danger')
        return redirect(url_for('main.index'))
    
    if not username:
        print('Invalid username')
        flash('Invalid username.', 'danger')
        return redirect(url_for('main.index')) 
    
    game_slug = slug.strip()

    game = db.session.query(Game).filter_by(slug=game_slug).first()
    user = db.session.query(User).filter_by(username=username).first()

    if not game:
        print('Game not found for slug:', game_slug)
        flash('Game not found.', 'danger')
        return redirect(url_for('main.index'))
    
    user_game_stat = (
        db.session.query(UserGameStat)
        .filter_by(user_id=user.id, game_id=game.id)
        .first()
    )

    if user_game_stat:
        if score > user_game_stat.high_score:
            user_game_stat.high_score = score
            db.session.commit()
            flash(f'New high score of {score} submitted for game {game_slug}!', 'success')
    else:
        user_game_stat = UserGameStat(
            user_id=user.id,
            game_id=game.id,
            high_score=score
        )
        db.session.add(user_game_stat)
        db.session.commit()
        flash(f'Score of {score} submitted for game {game_slug}.', 'success')

    return redirect(request.referrer or url_for('main.index'))

@bp.post('/game/launch_snake')
@login_required
def launch_snake():
    path = Path(current_app.root_path).parent / 'games' / 'snake' / 'main.py'
    subprocess.Popen([sys.executable, str(path), '-s', 'localhost:5000', '-u', current_user.username])
    flash('Snake game launched in a separate window.', 'info')
    return redirect(url_for('main.index'))  