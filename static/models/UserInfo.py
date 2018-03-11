from viewOJ import db
from sqlalchemy import ForeignKey
from static.models.User import User


class UserInfo(db.Model):
    __tablename__ = 'user_info'

    userId = db.Column(db.String(20), ForeignKey(User.userId), primary_key=True)
    ojId = db.Column(db.String(50), nullable=False)
    yn = db.Column(db.Integer, default=0)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, user_id, user_name, password=None, yn=0):
        self.userId = user_id
        self.userName = user_name
        self.password = password or user_id
        self.yn = yn

    def __repr__(self):
        return '<User %r>' % self.userName

    def get_id(self):
        return str(self.userId)
