from app.extensions import db
from app.models import UserAction, User, Match
from flask_login import current_user
from flask import session

def feed_ids():
    acted_user_ids = (
        db.session.query(UserAction.target_id)
        .filter(
            UserAction.actor_id == current_user.id,
        ).subquery()
    )

    candidates = (
        User.query
        .filter(User.id != current_user.id)
        .filter(~User.id.in_(acted_user_ids))
        .order_by(User.id.asc())
        .all()
    )

    return [user.id for user in candidates]

def pop_next_feed_id():
    ids = session.get('feed_ids', [])
    if ids:
        return ids[0]
    return None

def remove_feed_id(user_id):
    ids = session.get('feed_ids', [])
    if user_id in ids:
        ids.remove(user_id)
        session['feed_ids'] = ids

def ensure_match(user_1_id, user_2_id):
    a, b = sorted([user_1_id, user_2_id])
    existing = Match.query.filter_by(user_a_id=a, user_b_id=b).first()
    if existing:
        return existing
    
    m = Match(user_a_id=a, user_b_id=b)
    db.session.add(m)
    return m

