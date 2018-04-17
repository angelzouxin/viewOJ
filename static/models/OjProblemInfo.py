from viewOJ import db
from static.models.Oj import Oj
from sqlalchemy import ForeignKey
from datetime import date


class OjProblemInfo(db.Model):
    __tablename__ = 'oj_problem_info'

    ojId = db.Column(db.Integer, ForeignKey(Oj.ojId), primary_key=True, nullable=False)
    proId = db.Column(db.String(50), primary_key=True, nullable=False)
    acNums = db.Column(db.Integer, default=0)
    subNums = db.Column(db.Integer, default=0)
    crawlerDate = db.Column(db.Date, default=date.today())
    tags = db.Column(db.String(80), default='')

    def __init__(self, oj_id, pro_id, ac_nums=0, sub_nums=0, tags='', crawler_date=date.today()):
        self.ojId = oj_id
        self.proId = pro_id
        self.acNums = ac_nums
        self.subNums = sub_nums
        self.tags = tags
        self.crawlerDate = crawler_date

    def __repr__(self):
        return str({'ojId': self.ojId, 'proId': self.proId, 'acNums': self.acNums, 'subNums': self.subNums,
                    'crawlerDate': self.crawlerDate})

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}