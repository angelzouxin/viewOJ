from static.models.UserInfo import UserInfo
from static.models.Oj import Oj
from static.models.User import User
from sqlalchemy.sql import and_
from viewOJ import db


def add(user_id, oj_id, user_oj_id):
    if query(user_id, oj_id):
        print('user oj info exits')
        return False
    user_info = UserInfo(user_id, oj_id, user_oj_id)
    db.session.add(user_info)
    db.session.commit()
    return True


def query(user_id, oj_id):
    return db.session.query(UserInfo) \
        .filter(UserInfo.userId == user_id) \
        .filter(UserInfo.ojId == oj_id) \
        .first()


def update_user_oj_id(user_info_id, user_oj_id):
    user_info = UserInfo.query.filter_by(userInfoId=user_info_id).first()
    if user_info:
        user_info.userOjId = user_oj_id
        db.session.commit()
        return True
    return False


def list_by_filter(user_id=None, oj_id=None):
    db_query = db.session.query(User.userId, User.userName, Oj.ojId, Oj.ojName, UserInfo.userInfoId,
                                UserInfo.userOjId).outerjoin(UserInfo, and_(UserInfo.ojId == Oj.ojId,
                                                                            UserInfo.userId == User.userId))
    if user_id:
        db_query = db_query.filter(User.userId == user_id)
    if oj_id:
        db_query = db_query.filter(Oj.ojId == oj_id)
    return db_query.all()
