from static.models.User import User
from viewOJ import db


def add(user_id, user_name, yn=0, user_permission='student'):
    if query(user_id):
        print('user exits')
        return False
    user = User(user_id, user_name, yn=yn, permission=user_permission)
    db.session.add(user)
    db.session.commit()
    return True


def query(user_id):
    return db.session.query(User).filter(User.userId == user_id).first()


def update_yn(user_id, yn):
    user = User.query.filter_by(userId=user_id).first()
    if user:
        user.yn = yn
        db.session.commit()
        return True
    return False


def update_permission(user_id, permission):
    user = User.query.filter_by(userId=user_id).first()
    if user:
        user.permission = permission
        db.session.commit()
        return True
    return False


def list_by_filter(user_id=None, user_name=None):
    if user_id or user_name:
        return db.session.query(User).filter((User.userName == user_name) | (User.userId == user_id))
    return db.session.query(User).all()


def reset(user_id):
    return update(user_id, user_id)


def update(user_id, password):
    user = User.query.filter_by(userId=user_id).first()
    if user:
        user.password = password
        db.session.commit()
        return True
    return False
