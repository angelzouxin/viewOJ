import functools
import json
import sqlite3

import pandas as pd

from static.models.models import *


class sqlUtil:
    obj_to_json = functools.partial(json.dumps, default=lambda o: o.__dict__, sort_keys=True, ensure_ascii=False)

    def __init__(self, sqliteName="zuccOJ"):
        self.conn = sqlite3.connect(sqliteName)
        self.ojInfo = {}
        self.info = {}
        self.stDate = None
        cursor = self.conn.cursor()
        cursor.execute('SELECT ojId, ojName FROM oj')
        values = cursor.fetchall()
        self.ojInfo = {oj[1]: oj[0] for oj in values}
        self.oj = {oj[0]: oj[1] for oj in values}

        cursor.execute('SELECT userInfoId, userId, ojId FROM user_info')
        values = cursor.fetchall()
        self.info = {(info[1], info[2]): info[0] for info in values}
        self.user = {info[0]: info[1] for info in cursor.execute('SELECT userId, userName FROM user').fetchall()}
        self.stDate = cursor.execute('SELECT min(countDate) FROM daily_info').fetchall()[0][0]
        cursor.close()

    def import_id_list_by_xls(self, xlsName='xls/id_list.xls'):
        df = pd.read_excel(xlsName)
        cursor = self.conn.cursor()
        for index, row in df.T.iteritems():
            userId = str(row['学号'])
            userName = str(row['姓名'])
            if self.user.get(userId) is None:
                cursor.execute(
                    'INSERT INTO user(userId, userName, password, yn) VALUES (?,?,?,?)',
                    (userId, userName, userId, 1))
            for ojName, ojId in self.ojInfo.items():
                userOjId = row[ojName] if row[ojName] == row[ojName] else row['zucc']
                userInfo = user_info(userId, ojId, userOjId)
                if self.info.get((userId, ojId)) is None:
                    cursor.execute(
                        'INSERT INTO user_info(userInfoId, ojId, userId, userOjId) VALUES (?,?,?,?)',
                        (userInfo.uesrInfoId, userInfo.ojId, userInfo.userId, userInfo.userOjId))
                else:
                    cursor.execute(
                        'UPDATE user_info SET userOjId = ? WHERE userInfoId = ? AND userOjId != ?',
                        (userInfo.userOjId, self.info.get((userId, ojId)), userInfo.userOjId))
        self.conn.commit()
        cursor.execute('SELECT userInfoId, userId, ojId FROM user_info')
        values = cursor.fetchall()
        self.info = {(info[1], info[2]): info[0] for info in values}
        cursor.close()

    def get_detial_by_userId(self, userId, stDate=None, edDate=datetime.date.today().strftime('%Y-%m-%d')):
        if stDate is None: stDate = self.stDate
        if edDate is None: edDate = datetime.date.today().strftime('%Y-%m-%d')
        cursor = self.conn.cursor()
        cursor.execute('''SELECT  ojId, userId, proId, acDate
                            FROM user_info AS a , sub_info AS b
                            WHERE b.userInfoId IN (
                            SELECT userInfoId
                            FROM  user_info
                            WHERE userId = ?
                            ) AND a.userInfoId = b.userInfoId AND acDate > ? AND acDate <= ?''',
                       (userId, stDate, edDate))
        values = list(
            map(lambda info: [self.user.get(info[1]), self.oj.get(info[0])] + list(info)[1:], cursor.fetchall()))
        return values

    def get_inc_by_date(self, stDate=None, edDate=None):
        if stDate is None: stDate = self.stDate
        if edDate is None: edDate = datetime.date.today().strftime('%Y-%m-%d')
        cursor = self.conn.cursor()
        cursor.execute('''SELECT b.userId,sum(acTimes),sum(subTimes),countDate
                          FROM daily_info AS a,user_info AS b
                          WHERE a.userInfoId = b.userInfoId
                          AND countDate >= ? AND countDate < ?
                          GROUP BY userId,countDate''', (stDate, edDate))
        values = list(map(lambda info: [self.user.get(info[0])] + list(info), cursor.fetchall()))
        res = {}
        for value in values:
            userId = value[1]
            if res.get(userId) is None:
                now = user_daily(value[1], value[0], info(value[2], value[3], value[4]))
                res[userId] = now
            else:
                res.get(userId).addInfo(info(value[2], value[3], value[4]))
        values = [value for value in res.values()]
        return values

    def get_countDate(self, stDate=None, edDate=None):
        if stDate is None: stDate = self.stDate
        if edDate is None: edDate = datetime.date.today().strftime('%Y-%m-%d')
        cursor = self.conn.cursor()
        cursor.execute('''SELECT countDate
                          FROM daily_info 
                          WHERE countDate >= ? AND  countDate < ?
                          GROUP BY countDate
                          ORDER BY countDate ASC''', (stDate, edDate))
        values = [info[0] for info in cursor.fetchall()]

        return values

    def get_user_valid(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT userId, userName FROM user WHERE yn = 1')
        return list(map(list, cursor.fetchall()))

    def list_user(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT userId, userName, yn FROM user')
        return list(map(list, cursor.fetchall()))

    def get_userInfo_by_id(self, userId):
        cursor = self.conn.cursor()
        cursor.execute('SELECT userInfoId, ojId, userOjId FROM user_info WHERE userId = ?', (userId,))
        values = list(map(list, cursor.fetchall()))
        cursor.close()
        return values

    def get_subTimes_by_id(self, userInfoId):
        cursor = self.conn.cursor()
        cursor.execute('SELECT sum(subTimes) FROM daily_info WHERE userInfoId = ?', (userInfoId,))
        value = cursor.fetchone()
        return int(value[0])

    def get_subInfo_by_id(self, userInfoId):
        cursor = self.conn.cursor()
        cursor.execute('SELECT proId FROM sub_info WHERE userInfoId = ?', (userInfoId,))
        values = list(map(lambda x: x[0], cursor.fetchall()))
        return values

    def insert_subInfo(self, pros):
        cursor = self.conn.cursor()
        cursor.executemany('INSERT INTO sub_info(userINfoId, proId, acDate) VALUES(?,?,?)', pros)
        self.conn.commit()
        cursor.close()

    def insert_dailyInfo(self, dailyInfos):
        cursor = self.conn.cursor()
        cursor.executemany('INSERT INTO daily_info(userINfoId, acTimes, subTimes, countDate) VALUES(?,?,?,?)',
                           dailyInfos)
        self.conn.commit()
        cursor.close()
