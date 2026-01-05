from math import log

from sqlalchemy import select
from app.extensions import db
from app.models import UserAction, User, Match
from flask_login import current_user
from flask import session


def scalar_product(user1, user2) -> float:
    score = 0
    for hobby in user1.hobbies:
        for hobby2 in user2.hobbies:
            if hobby.name == hobby2.name:
                score += 1
            elif hobby.category == hobby2.category:
                score += 0.5
    for game in user1.game_stats:
        for game2 in user2.game_stats:
            if game.game.slug == game2.game.slug:
                if game.game.slug == 'snake':
                    score += 1
                    score -= abs(game2.score - game.score) / 400
                if game.game.slug == 'block_blast':
                    score += 1
                    score -= abs(log(game2.score, 10) - log(game.score, 10))
                if game.game.slug == 'dino':
                    score += 1
                    score -= abs(log(game2.score, 10) - log(game.score, 10))

    return score


def feed_ids():
    acted_user_ids = select(UserAction.target_id).where(
        UserAction.actor_id == current_user.id
    )

    candidates = (
        User.query
        .filter(User.id != current_user.id)
        .filter(~User.id.in_(acted_user_ids))
        .order_by(User.id.asc())
        .all()
    )

    # TODO: sort based on matchmaking algorithm
    candidates.sort(key=lambda user: -scalar_product(user, current_user))
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

