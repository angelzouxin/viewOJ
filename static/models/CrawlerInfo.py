from viewOJ import db
from static.models.UserInfo import UserInfo
from sqlalchemy import ForeignKey
import datetime


class CrawlerInfo(db.Model):
    __tablename__ = 'crawler_info'

    userInfoId = db.Column(db.Integer, ForeignKey(UserInfo.userInfoId), primary_key=True, nullable=False)
    lastFetchTime = db.Column(db.DateTime, nullable=False)
    retryTimes = db.Column(db.Integer, default=0, nullable=False)
    status = db.Column(db.Integer, default=0, nullable=False)

    CRAWLER_FAIL_STATUS = 0
    CRAWLER_SUCCESS_STATUS = 1
    DATETIME_FORMATE = '{0:%Y-%m-%d %H:%M:%S}'
    MAX_RETRY_TIMES = 3

    def __init__(self, user_info_id):
        self.userInfoId = user_info_id
        self.retryTimes = 0
        self.status = 0
