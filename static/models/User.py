from viewOJ import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    userId = db.Column(db.String(20), primary_key=True)
    userName = db.Column(db.String(50), nullable=False)
    yn = db.Column(db.Integer, default=0)
    password = db.Column(db.String(100), nullable=False)
    permission = db.Column(db.String(10), nullable=False, default='student')

    def __init__(self, user_id, user_name, password=None, yn=0, permission='student'):
        self.userId = user_id
        self.userName = user_name
        self.password = password or user_id
        self.yn = yn
        self.permission = permission

    def __repr__(self):
        return '<User %r>' % self.userName

    def get_id(self):
        return str(self.userId)
