from viewOJ import db
from static.models.UserInfo import UserInfo
from sqlalchemy import ForeignKey


class DailyInfo(db.Model):
    __tablename__ = 'daily_info'

    userInfoId = db.Column(db.Integer, ForeignKey(UserInfo.userInfoId), primary_key=True, nullable=False)
    subTimes = db.Column(db.Integer, default=0, nullable=False)
    acTimes = db.Column(db.Integer, default=0, nullable=False)
    countDate = db.Column(db.Date)

    def __init__(self, user_info_id, count_date, ac_times=0, sub_times=0):
        self.userInfoId = user_info_id
        self.countDate = count_date
        self.acTimes = ac_times
        self.subTimes = sub_times

    def __repr__(self):
        return str({'userInfoId': self.userInfoId, 'acTimes': self.acTimes, 'subTimes': self.subTimes,
                    'countDate': self.countDate})
