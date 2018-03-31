from static.models.SubInfo import SubInfo
from static.models.UserInfo import UserInfo
from static.models.Oj import Oj
from static.models.User import User
from viewOJ import db
from sqlalchemy import and_

dict_name = ['userId', 'userName', 'ojId', 'ojName', 'userInfoId', 'proId', 'acDate']


def query(user_id=None, oj_id=None, start_date=None, end_date=None):
    db_query = db.session.query(User.userId, User.userName, Oj.ojId, Oj.ojName, SubInfo.userInfoId, SubInfo.proId, SubInfo.acDate).join(UserInfo, and_(
        UserInfo.userId == User.userId, Oj.ojId == UserInfo.ojId) & (UserInfo.userInfoId == SubInfo.userInfoId))
    if start_date:
        db_query.filter(SubInfo.acDate >= start_date)
    if end_date:
        db_query.filter(SubInfo.acDate <= end_date)
    if user_id:
        db_query.filter(User.userId == user_id)
    if oj_id:
        db_query.filter(Oj.ojId == oj_id)

    return [dict(zip(dict_name, item)) for item in db_query.all()]

