from viewOJ import db


class Oj(db.Model):
    __tablename__ = 'oj'

    ojId = db.Column(db.Integer, primary_key=True)
    ojName = db.Column(db.String(20), nullable=False)

    def __init__(self, oj_name):
        self.ojName = oj_name

    def __repr__(self):
        return str({'ojId': self.ojId, 'ojName': self.ojName})

