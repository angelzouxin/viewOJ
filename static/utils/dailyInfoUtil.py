from static.models.DailyInfo import DailyInfo
from static.models.UserInfo import UserInfo
from static.models.Oj import Oj
from static.models.User import User
from viewOJ import db
from sqlalchemy import and_, func

dict_name = ['userId', 'userName', 'ojId', 'ojName', 'userInfoId', 'acTimes', 'subTimes', 'countDate']


def query(user_id=None, oj_id=None, start_date=None, end_date=None, group_by=False):
    db_query = db.session. \
        query(User.userId, User.userName, Oj.ojId, Oj.ojName, DailyInfo.userInfoId, DailyInfo.acTimes,
              DailyInfo.subTimes, DailyInfo.countDate)
    if group_by:
        db_query = db.session. \
            query(User.userId, User.userName, Oj.ojId, Oj.ojName, DailyInfo.userInfoId, func.sum(DailyInfo.acTimes),
                  func.sum(DailyInfo.subTimes))
    db_query = db_query.join(UserInfo,
                  and_(UserInfo.userId == User.userId, Oj.ojId == UserInfo.ojId)
                  & (UserInfo.userInfoId == DailyInfo.userInfoId))
    if start_date is not None:
        db_query = db_query.filter(DailyInfo.countDate >= start_date)
    if end_date is not None:
        db_query = db_query.filter(DailyInfo.countDate < end_date)
    if user_id is not None:
        db_query = db_query.filter(User.userId == user_id)
    if oj_id is not None:
        db_query = db_query.filter(Oj.ojId == oj_id)
    if group_by:
        db_query = db_query.group_by(UserInfo.userInfoId)
    result = db_query.all()
    return [dict(zip(dict_name, item)) for item in result]
