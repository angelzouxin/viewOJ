from flask import Flask, render_template, request, redirect, url_for, flash, abort, Response, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps
from flask.ext.login import (LoginManager, login_user, logout_user,
                             current_user, login_required, fresh_login_required)
from sqlalchemy import asc
from static.utils import toolsUtil
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Unauthorized User'
login_manager.login_message_category = "info"


# 通过用户名，获取用户记录，如果不存在，则返回None
def query_user(user_id):
    from static.models.User import User
    return db.session.query(User).filter(User.userId == user_id).first()


# 如果用户名存在则构建一个新的用户类对象，并使用用户名作为ID
# 如果不存在，必须返回None
@login_manager.user_loader
def load_user(user_id):
    from static.utils import userUtil
    return userUtil.query(user_id)


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permission != 'admin':
            return Response('Permission Denied', status=401)
        return func(*args, **kwargs)

    return decorated_view


@app.route('/index')
@app.route('/home')
@app.route('/')
def home():
    return render_template('view.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # from static.utils import loginUtil
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = query_user(username)
        if user is not None and user.password == password:
            curr_user = user

            # 通过Flask-Login的login_user方法登录用户
            login_user(curr_user, remember=True)

            # 如果请求中有next参数，则重定向到其指定的地址，
            # 没有next参数，则重定向到"index"视图
            next_url = request.args.get('next')
            return redirect(next_url or url_for('home'))

        flash('Wrong username or password!')

    return render_template('login.html', title='登录')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('view.html', title='登录')


@app.route('/manager', methods=['GET', 'POST'])
@login_required
@admin_required
def manager():
    from static.models.User import User
    result = db.session.query(User).order_by(asc(User.permission)).order_by(User.userId).all()
    rows = [row.to_dict() for row in result]
    return render_template('manager.html', title='后台管理',
                           items=rows)


@app.route('/search', methods=['GET', 'POST'])
def search():
    from static.utils import sqlUtil
    json_data = request.get_json()
    st = json_data.get('st')
    ed = json_data.get('ed')
    util = sqlUtil.sqlUtil(os.path.join(basedir, 'zuccOJ'))
    dic = dict()
    dic['countDate'] = util.get_countDate(stDate=st, edDate=ed)
    dic['dates'] = util.get_inc_by_date(stDate=st, edDate=ed)
    json_str = util.obj_to_json(dic)
    return json_str


@app.route('/user/add', methods=['POST'])
@login_required
@admin_required
def add_user():
    from static.utils import userUtil
    user_name = request.form.get('userName')
    user_id = request.form.get('userId')
    user_permission = 'admin' if request.form.get('permission') == 'admin' else 'student'
    if userUtil.add(user_id, user_name, 1, user_permission):
        return redirect(url_for('manager'))
    else:
        return Response('Permission Denied', status=401)


@app.route('/user/update', methods=['POST'])
@login_required
@admin_required
def update():
    from static.utils import userUtil
    params = request.get_json()
    user_id = params.get('userId')
    user_name = params.get('userName')
    yn = params.get('yn')
    permission = params.get('permission')
    result = False
    if yn is not None:
        result = userUtil.update_yn(user_id, yn)
    elif permission:
        result = userUtil.update_permission(user_id, permission)
    elif user_name:
        result = userUtil.update_user_name(user_id, user_name)
    dic = {"result": result}
    return jsonify(dic)


@app.route('/userInfo/<user_id>', methods=['GET', 'POST'])
@login_required
def get_user_info(user_id):
    from static.utils import userInfoUtil
    rows = userInfoUtil.list_by_filter()
    result = []
    names = ['user_id', 'user_name', 'oj_id', 'oj_name', 'user_info_id', 'user_oj_id']
    for row in rows:
        result.append(dict(zip(names, row)))
    return render_template('userinfo.html', title='个人信息',
                           items={'items': result, 'user_id': rows[0].userId, 'user_name': rows[0].userName})


@app.route('/userInfo/update', methods=['POST'])
@login_required
def update_user_info():
    from static.utils import userInfoUtil
    json_data = request.get_json()
    origin = json_data.get('origin')
    if origin['user_id'] != current_user.userId and current_user.permission != 'admin':
        return toolsUtil.obj_to_json({'status': 'error', 'message': '不能更新他人账号'})
    user_oj_id = json_data.get('user_oj_id')
    if current_user.permission != 'admin':
        origin['user_id'] = current_user.userId
    query_origin = userInfoUtil.query(origin['user_id'], origin['oj_id'])
    if query_origin is None:
        userInfoUtil.add(origin['user_id'], origin['oj_id'], user_oj_id)
    else:
        userInfoUtil.update_user_oj_id(query_origin.userInfoId, user_oj_id)
    return toolsUtil.obj_to_json({'status': 'ok'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7001, debug=True)
