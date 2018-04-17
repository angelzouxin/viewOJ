from static.models.OjProblemInfo import OjProblemInfo
from viewOJ import db
from sqlalchemy import and_

dict_name = ['ojId', 'proId', 'acNums', 'subNums', 'crawlerDate', 'tags']


def query(oj_id, pro_id):
    db_query = db.session.query(OjProblemInfo).\
        filter(and_(OjProblemInfo.ojId == oj_id, OjProblemInfo.proId == pro_id))
    return db_query.first()


def add(oj_id, pro_id, ac_nums, sub_nums, crawler_date=None, tags=None):
    oj_problem_info = OjProblemInfo(oj_id, pro_id, ac_nums, sub_nums)
    if crawler_date:
        oj_problem_info.crawlerDate = crawler_date
    if tags:
        oj_problem_info.tags = tags
    db.session.add(oj_problem_info)
    db.session.commit()
    return True


def update(oj_id, pro_id, crawler_date=None, ac_nums=None, sub_nums=None, tags=None):
    info = query(oj_id, pro_id)
    if info is None:
        return False
    if crawler_date:
        info.crawlerDate = crawler_date
    if ac_nums:
        info.acNums = ac_nums
    if sub_nums:
        info.sub_nums = sub_nums
    if tags:
        info.tags = tags
    db.session.commit()
    return True


def upsert(oj_id, pro_id, ac_nums, sub_nums, crawler_date=None, tags=None):
    info = query(oj_id, pro_id)
    if info is None:
        add(oj_id, pro_id, ac_nums, sub_nums, crawler_date, tags)
        return True
    info.acNums = ac_nums
    info.subNums = sub_nums
    if crawler_date:
        info.crawlerDate = crawler_date
    if tags:
        info.tags = tags
    db.session.commit()
    return True
