from viewOJ import db
from static.models.User import User
from sqlalchemy import ForeignKey
from datetime import date


class UserRatingInfo(db.Model):
    __tablename__ = 'user_rating_info'

    userId = db.Column(db.String(20), ForeignKey(User.userId), primary_key=True)
    rating = db.Column(db.Integer, nullable=False, default=1500)
    countDate = db.Column(db.Date, default=date.today(), primary_key=True)

    def __init__(self, user_id, rating=1500):
        self.userId = user_id
        self.proId = rating

    def __repr__(self):
        return str({'userId': self.userId, 'rating': self.rating, 'countDate': self.countDate})

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}