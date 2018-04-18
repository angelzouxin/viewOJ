from static.models.UserRatingInfo import UserRatingInfo
from static.models.User import User
from datetime import date
from viewOJ import db
from sqlalchemy import and_, func

rank_list_dict_name = ['userName', 'userId', 'rating']
rank_dict_name = ['userName', 'userId', 'rating', 'countDate']
DEFAULT_RATING = 1500


def query(user_id, count_date):
    db_query = db.session.query(UserRatingInfo). \
        filter(UserRatingInfo.userId == user_id)
    if count_date:
        db_query = db_query.filter(UserRatingInfo.countDate == count_date)
    result = db_query.all()
    return [item.to_dict() for item in result]


def queryByIds(user_ids, count_date):
    db_query = db.session.query(UserRatingInfo). \
        filter(and_(UserRatingInfo.count_date == count_date, UserRatingInfo.userId.in_(user_ids)))
    result = db_query.all()
    return [item.to_dict() for item in result]


def add(user_id, rating, count_date=None):
    rating_info = UserRatingInfo(user_id, rating)
    if count_date:
        rating_info.countDate = count_date
    db.session.add(rating_info)
    db.session.commit()
    return True


def queryOne(user_id, count_date):
    db_query = db.session.query(UserRatingInfo). \
        filter(UserRatingInfo.userId == user_id)
    if count_date:
        db_query = db_query.filter(UserRatingInfo.countDate == count_date)
    return db_query.first()


def upsert(user_id, rating, count_date=date.today()):
    user_rating_info = queryOne(user_id, count_date)
    if user_rating_info is None:
        add(user_id, rating, count_date)
        return True
    user_rating_info.rating = rating
    db.session.commit()


def getRankList():
    t = db.session.query(
        UserRatingInfo.userId,
        func.max(UserRatingInfo.countDate).label('maxDate')
    ).group_by(UserRatingInfo.userId).subquery('t')
    db_query = db.session.query(User.userName, User.userId, UserRatingInfo.rating). \
        join(t, and_(UserRatingInfo.userId == User.userId,
                     and_(t.c.userId == UserRatingInfo.userId, t.c.maxDate == UserRatingInfo.countDate))).group_by(
        User.userId).order_by(UserRatingInfo.rating.desc())
    return [dict(zip(rank_list_dict_name, item)) for item in db_query.all()]


def getRankById(user_id):
    db_query = db.session.query(User.userName, User.userId, UserRatingInfo.rating, UserRatingInfo.countDate). \
        join(UserRatingInfo, User.userId == UserRatingInfo.userId). \
        filter(User.userId == user_id). \
        order_by(UserRatingInfo.countDate.asc())
    return [dict(zip(rank_dict_name, item)) for item in db_query.all()]
