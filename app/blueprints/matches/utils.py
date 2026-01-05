from flask_login import current_user
from app.models import Match, User

def is_participant(match, user_id):
    return user_id in (match.user_a_id, match.user_b_id)

def other_participant(match, user_id):
    other_id = match.user_b_id if match.user_a_id == current_user.id else match.user_a_id
    return User.query.get(other_id)