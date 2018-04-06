from static.models.CrawlerInfo import CrawlerInfo
from viewOJ import db
import datetime


def get_last_failure_status():
    filter_time = datetime.time.today().__str__()
    db_query = db.session.query(CrawlerInfo)\
        .filter(CrawlerInfo.lastFetchTime > filter_time)\
        .filter(CrawlerInfo.status == CrawlerInfo.CRAWLER_FAIL_STATUS)\
        .filter(CrawlerInfo.retryTimes < CrawlerInfo.MAX_RETRY_TIMES)

    return db_query.all()


def upsert(user_info_id, status, last_fetch_time=None, retry_time=0):
    crawler_info = query(user_info_id)
    if last_fetch_time is None:
        last_fetch_time = CrawlerInfo.DATETIME_FORMATE.format(datetime.datetime.now())
        last_fetch_time = datetime.datetime.strptime(last_fetch_time, '%Y-%m-%d %H:%M:%S')
    if crawler_info:
        crawler_info.status = status
        crawler_info.retry_time = retry_time
        crawler_info.last_fetch_time = last_fetch_time
        db.session.commit()
        return True
    crawler_info = CrawlerInfo(user_info_id)
    crawler_info.lastFetchTime = last_fetch_time
    crawler_info.retryTime = retry_time
    crawler_info.status = status
    db.session.add(crawler_info)
    db.session.commit()
    return True


def query(user_info_id):
    return db.session.query(CrawlerInfo).filter(CrawlerInfo.userInfoId == user_info_id).first()
