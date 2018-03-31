from viewOJ import db
from static.models.UserInfo import UserInfo
from sqlalchemy import ForeignKey


class SubInfo(db.Model):
    __tablename__ = 'sub_info'

    userInfoId = db.Column(db.Integer, ForeignKey(UserInfo.userInfoId), primary_key=True, nullable=False)
    proId = db.Column(db.String(50), primary_key=True, nullable=False)
    acDate = db.Column(db.Date)

    def __init__(self, user_info_id, pro_id, ac_date):
        self.userInfoId = user_info_id
        self.proId = pro_id
        self.acDate = ac_date

    def __repr__(self):
        return str({'userInfoId': self.userInfoId, 'proId': self.proId, 'acDate': self.acDate})
