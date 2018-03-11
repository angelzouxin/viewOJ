from flask import Flask, render_template, request, redirect, url_for, flash, abort, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import (LoginManager, UserMixin, login_user, logout_user,
                            current_user, login_required, fresh_login_required)
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
def manager():
    from static.models.User import User
    return render_template('manager.html', title='后台管理', items=db.session.query(User).all())


@app.route('/search', methods=['GET', 'POST'])
def search():
    from static.utils import sqlUtil
    jsonData = request.get_json()
    st = jsonData.get('st')
    ed = jsonData.get('ed')
    util = sqlUtil.sqlUtil(os.path.join(basedir, 'zuccOJ'))
    dic = {}
    dic['countDate'] = util.get_countDate(stDate=st, edDate=ed)
    dic['dates'] = util.get_inc_by_date(stDate=st, edDate=ed)
    json_str = util.obj_to_json(dic)
    return json_str


@app.route('/user/add', methods=['POST'])
@login_required
def add():
    from static.utils import userUtil
    user_name = request.form.get('userName')
    user_id = request.form.get('userId')
    userUtil.add(user_id, user_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7001, debug=True)
