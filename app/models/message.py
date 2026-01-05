from datetime import datetime, timezone
from ..extensions import db

class Message(db.Model):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True)

    match_id = db.Column(
        db.Integer,
        db.ForeignKey("match.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    sender_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    sender = db.relationship(
        "User",
        back_populates="messages_sent",
        foreign_keys=[sender_id],
    )

    body = db.Column(db.Text, nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )

    # relationships
    match = db.relationship("Match", back_populates="messages")
    sender = db.relationship("User")
