from viewOJ import db
from sqlalchemy import ForeignKey
from static.models.User import User
from static.models.Oj import Oj


class UserInfo(db.Model):
    __tablename__ = 'user_info'

    userInfoId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(20), ForeignKey(User.userId), primary_key=True, nullable=False)
    ojId = db.Column(db.Integer, ForeignKey(Oj.ojId), primary_key=True, nullable=False)
    userOjId = db.Column(db.String(50), nullable=False)

    def __init__(self, user_id, oj_id, user_oj_id=None):
        self.userId = user_id
        self.ojId = oj_id
        self.userOjId = user_oj_id or user_id

    def __repr__(self):
        return str({'UserInfo': self.userInfoId, 'UserOjId': self.userOjId})

    def get_id(self):
        return self.userInfoId

    def get_user_info(self):
        return self.userOjId
