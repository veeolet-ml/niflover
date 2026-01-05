from datetime import timezone, datetime
from sqlalchemy import CheckConstraint, UniqueConstraint
from ..extensions import db
from . import User

class Match(db.Model):
    __tablename__ = 'match'
    id = db.Column(db.Integer, primary_key=True)
    user_a_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user_b_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    messages = db.relationship(
        "Message",
        back_populates="match",
        cascade="all, delete-orphan",
        order_by="Message.created_at.asc()",
        lazy="selectin",
    )


    __table_args__ = (
        UniqueConstraint('user_a_id', 'user_b_id', name='uq_match_user_a_user_b'),
        CheckConstraint('user_a_id < user_b_id', name='ck_match_user_order'),
    )