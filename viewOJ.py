
from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from threading import Timer, Thread

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template('view.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title='Login')


@app.route('/search', methods=['GET', 'POST'])
def search():
    from static.utils import searchUtil
    jsonData = request.get_json()
    st = jsonData.get('st')
    ed = jsonData.get('ed')
    util = searchUtil.sqlUtil()
    dic = {}
    dic['countDate'] = util.get_countDate(stDate=st,edDate=ed)
    dic['dates'] = util.get_inc_by_date(stDate=st,edDate=ed)
    json_str = util.obj_to_json(dic)
    return json_str


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7001, debug=True)
