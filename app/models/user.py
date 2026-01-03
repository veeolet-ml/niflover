from flask_login import UserMixin
from enum import Enum
from datetime import datetime, timezone
from sqlalchemy import UniqueConstraint, CheckConstraint
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)

    # authentication fields
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)

    # personal information
    display_name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)

    photos = db.relationship(
        'UserPhoto', 
        back_populates='user', 
        cascade='all, delete-orphan',
        order_by='UserPhoto.position.asc()',
        lazy='selectin'
    )

    hobbies = db.relationship(
        'Hobby',
        secondary='user_hobby',
        back_populates='users',
        lazy='selectin'
    )

    game_stats = db.relationship(
        'UserGameStat',
        back_populates='user',
        cascade='all, delete-orphan',
        lazy='selectin'
    )

    __table_args__ = (
        CheckConstraint('length(username) >= 3', name='ck_user_username_length'),
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def add_photo(self, rel_path, position):
        photo = UserPhoto(path=rel_path, position=position)
        self.photos.append(photo)
        return photo

user_hobby = db.Table(
    'user_hobby',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('hobby_id', db.Integer, db.ForeignKey('hobby.id'), primary_key=True)
)

class UserPhoto(db.Model):
    __tablename__ = 'user_photo'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)

    path = db.Column(db.String(255), nullable=False)

    uploaded_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)

    position = db.Column(db.Integer, nullable=False, default=0)

    user = db.relationship('User', back_populates='photos')

    __table_args__ = (
        UniqueConstraint('user_id', 'position', name='uq_userphoto_user_position'),
        CheckConstraint('position >= 0', name='ck_userphoto_position_nonnegative'),
    )   

class UserGameStat(db.Model):
    __tablename__ = 'user_game_stat'
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id', ondelete='CASCADE'), primary_key=True)

    high_score = db.Column(db.Integer, nullable=False, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

    user = db.relationship('User', back_populates='game_stats')
    game = db.relationship('Game', back_populates='user_stats')

    __table_args__ = (
        CheckConstraint('high_score >= 0', name='ck_usergamestat_high_score_nonnegative'),
    )

class ActionType(str, Enum):
    LIKE = 'like'
    PASS = 'pass'

class UserAction(db.Model):
    __tablename__ = 'user_action'

    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    target_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)

    action = db.Column(db.Enum(ActionType, name="action_type"), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        UniqueConstraint('actor_id', 'target_id', name='uq_useraction_actor_target'),
        CheckConstraint('actor_id != target_id', name='ck_useraction_no_self_action'),
    )

