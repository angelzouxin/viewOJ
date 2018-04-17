from static.models.UserRatingInfo import UserRatingInfo
from datetime import date
from viewOJ import db
from sqlalchemy import and_

dict_name = ['userId', 'rating', 'countDate']
DEFAULT_RATING = 1500


def query(user_id, count_date):
    db_query = db.session.query(UserRatingInfo).\
        filter(UserRatingInfo.userId == user_id)
    if count_date:
        db_query = db_query.filter(UserRatingInfo.countDate == count_date)
    result = db_query.all()
    return [item.to_dict() for item in result]


def queryByIds(user_ids, count_date):
    db_query = db.session.query(UserRatingInfo).\
        filter(and_(UserRatingInfo.count_date == count_date, UserRatingInfo.userId.in_(user_ids)))
    result = db_query.all()
    return [item.to_dict() for item in result]


def add(user_id, rating=1500, count_date=None):
    rating = UserRatingInfo(user_id, rating)
    if count_date:
        rating.countDate = count_date
    db.session.add(rating)
    db.session.commit()
    return True


def queryOne(user_id, count_date):
    db_query = db.session.query(UserRatingInfo).\
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
