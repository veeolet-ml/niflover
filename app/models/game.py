from ..extensions import db

class Game(db.Model):
    __tablename__ = 'game'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(150), unique=True, nullable=False, index=True)

    user_stats = db.relationship(
        'UserGameStat',
        back_populates='game',
        cascade='all, delete-orphan',
        lazy='selectin'
    )

    def __repr__(self):
        return f"<Game slug={self.slug!r}>"