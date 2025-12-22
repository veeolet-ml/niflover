from ..extensions import db

class Hobby(db.Model):
    __tablename__ = 'hobby'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), unique=True, nullable=False, index=True)

    users = db.relationship(
        'User',
        secondary='user_hobby',
        back_populates='hobbies',
        lazy='selectin'
    )

    def __repr__(self):
        return f"<Hobby {self.name!r}>"
    
