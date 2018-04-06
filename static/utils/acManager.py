import datetime
import time

import xlrd
from xlwt import *

from static.utils.sqlUtil import sqlUtil
from static.models.WeChatAlarms import WeChatAlarms
from static.models.CrawlerInfo import CrawlerInfo
from static.utils import crawlerInfoUtil

import os
basedir = os.path.abspath(os.path.dirname(__file__))
alarm = WeChatAlarms()
DELIMITER = ','
DATETIME_FORMATE = '{0:%Y-%m-%d %H:%M:%S}'
ALARM_TEMPLATE = '爬取用户信息失败\n学号：{user_id}\n姓名：{user_name}\noj: {oj_name}\n日期: {date}'
__author__ = 'zouxin'


class AcManager:
    supportedOJ = ['poj', 'hdu', 'zoj', 'codeforces', 'fzu', 'acdream', 'bzoj', 'ural', 'csu', 'hust', 'spoj', 'sgu',
                   'vjudge', 'bnu', 'cqu', 'uestc', 'zucc']

    def __init__(self):
        self.crawled_time = time.strftime('%Y-%m-%d %a %H:%M', time.localtime(time.time()))
        # [[userId, userName, {ojName: userOjId}, subTimes]]
        self.user_list = []
        self.col_id = []
        self.sqlUtil = sqlUtil(os.path.join(basedir, '../../zuccOJ'))

    def get_IDlist(self, id_file):
        self.crawled_time = time.strftime('%Y-%m-%d %a %H:%M', time.localtime(time.time()))
        table = xlrd.open_workbook(id_file).sheet_by_index(0)
        rows, cols = table.nrows, table.ncols
        head = table.row_values(0)
        self.col_id = [head[idx] for idx in range(cols)]
        for row in range(1, rows):
            mes = table.row_values(row)
            id, name = mes[:2]
            id = int(id)
            oj_id = {self.col_id[idx]: (type(mes[idx]) == float and str(int(mes[idx])) or mes[idx]) for idx in
                     range(2, cols) if mes[idx] is not None and mes[idx] != ''}

            oj_id['default'] = oj_id.get('zucc') is None and oj_id.get('hdu') or oj_id.get('zucc')
            print({id, name}, oj_id)
            self.user_list.append([id, name, oj_id])

    def list_user(self):
        # list of [userId,userName]
        users = self.sqlUtil.get_user_valid()
        for user in users:
            userId, userName = user
            # list of [userInfoId, ojId, userOjId]
            ojInfos = self.sqlUtil.get_userInfo_by_id(userId)
            oj_id = {}
            ac_archive = {}
            sub_Num = {}
            for ojInfo in ojInfos:
                userInfoId, ojId, userOjId = ojInfo
                ojName = self.sqlUtil.oj[ojId]
                oj_id[ojName] = userOjId
                sub_Num[ojName] = self.sqlUtil.get_subTimes_by_id(userInfoId)
                ac_archive[ojName] = set(self.sqlUtil.get_subInfo_by_id(userInfoId))
            oj_id['default'] = oj_id.get('zucc') is None and oj_id.get('hdu') or oj_id.get('zucc')
            self.user_list.append([userId, userName, oj_id, ac_archive, sub_Num])

    # get pre info from excel
    def get_pre_info(self, info_file, sheet_name1='ac_count', sheet_name2='ac_submission'):
        from static.utils.xlsUtil import xlsUtil
        self.info = xlrd.open_workbook(info_file)
        self.col_id, info_data = xlsUtil.read_xls(info_file, sheet_name1)
        self.col_id = self.col_id[:-2]

        info_head, info_achieve = xlsUtil.read_xls(info_file, sheet_name2)

        self.crawled_time = info_data[0][-1]

        rows, col = 0, len(info_data)
        for ac_num in info_achieve:
            # print (ac_num)
            user_id, user_name = ac_num[:2]
            user_id = int(user_id)
            ac_archive = {self.col_id[column]: (
                ac_num[column] != '' and set(
                    map(lambda x: x.strip("'"), ac_num[column].strip('{}').split(', '))) or set()) for
                column
                in range(2, len(ac_num))}
            self.user_list.append([user_id, user_name, {}, ac_archive.copy()])
        for ac_sub in info_data:
            submit_num = {self.col_id[column]: int(ac_sub[column].split('/')[-1]) for column in
                          range(2, len(ac_sub) - 2)}
            self.user_list[rows].append(submit_num.copy())
            rows += 1

    def get_count(self):
        from static.utils.countOJUtil import Crawler
        for user in self.user_list:
            crawler = Crawler(user[2])
            crawler.run()
            count = 0
            error_oj = []
            for ojName, value in crawler.wrongOJ.items():
                user_info_id = self.sqlUtil.info.get((user[0], self.sqlUtil.ojInfo.get(ojName)))
                if len(value) > 0:
                    if user_info_id is not None:
                        crawler_info = crawlerInfoUtil.query(user_info_id)
                        retry_time = crawler_info.retryTimes if crawler_info is not None else 0
                        # only alarm when retry_times >= max_retry_times, then clear out retry times
                        if retry_time == CrawlerInfo.MAX_RETRY_TIMES:
                            retry_time = 0
                            count += 1
                            error_oj.append(ojName)
                        else:
                            retry_time += 1
                        crawlerInfoUtil.upsert(user_info_id, CrawlerInfo.CRAWLER_FAIL_STATUS, retry_time=retry_time)
                else:
                    if user_info_id is not None:
                        crawlerInfoUtil.upsert(user_info_id, CrawlerInfo.CRAWLER_SUCCESS_STATUS)
            if count > 0:
                err_msg = AcManager.generate_alarm_msg(user[0], user[1], error_oj)
                alarm.send_msg(err_msg)
            user[3] = crawler.acArchive.copy()
            user[4] = crawler.submitNum.copy()

    def save_count_to_xls(self, out_file):
        from static.utils.xlsUtil import xlsUtil
        w = Workbook()
        ws1 = w.add_sheet('ac_count')
        headings = self.col_id.copy()
        headings.append('总计AC/Submission')
        headings.append('统计日期')
        datas = []
        for user in self.user_list:
            data = []
            # AC_num/AC_submission
            user_num = user[3]
            user_sub = user[4]
            data.append(user[0])  # id
            data.append(user[1])  # name
            sum_num, sum_sub = 0, 0
            for col_name in self.col_id[2:]:
                if user_num.get(col_name) is not None:
                    ac_num = len(user_num.get(col_name))
                    ac_sub = user_sub.get(col_name)
                    sum_num += ac_num
                    sum_sub += ac_sub
                    data.append('%d/%d' % (ac_num, ac_sub))
                else:
                    data.append('0/0')
            data.append('%d/%d' % (sum_num, sum_sub))
            data.append(self.crawled_time)
            datas.append(data)
        xlsUtil.write_xls(ws1, headings, datas)
        ws2 = w.add_sheet('ac_submission')
        headings = self.col_id
        datas = []
        for user in self.user_list:
            data = []
            user_num = user[3]
            data.append(user[0])
            data.append(user[1])
            for col_name in self.col_id[2:]:
                if user_num.get(col_name) is not None:
                    data.append('%s' % ('' if len(user_num.get(col_name)) == 0 else str(user_num.get(col_name))))
                else:
                    data.append('')
            datas.append(data)
        xlsUtil.write_xls(ws2, headings, datas)
        w.save(out_file)

    def save_to_db(self):
        pros = []
        dailyInfos = []
        date = datetime.datetime.today().strftime('%Y-%m-%d')
        for user in self.user_list:
            acTimes = {}
            userId = user[0]
            ac_Num, ac_archive = user[:-3:-1]
            for ojName, acPros in ac_archive.items():
                userInfoId = self.sqlUtil.info.get((userId, self.sqlUtil.ojInfo.get(ojName)))
                if userInfoId is None: continue
                acTimes[userInfoId] = len(acPros)
                for pro in acPros:
                    pros.append((userInfoId, pro, date))

            for ojName, subTimes in ac_Num.items():
                userInfoId = self.sqlUtil.info.get((userId, self.sqlUtil.ojInfo.get(ojName)))
                if userInfoId is None: continue
                if subTimes < 0:
                    subTimes = acTimes[userInfoId]

                dailyInfos.append((userInfoId, acTimes[userInfoId], subTimes, date))

        self.sqlUtil.insert_dailyInfo(dailyInfos)
        self.sqlUtil.insert_subInfo(pros)

    # get Incremental
    @staticmethod
    def get_today_mes(total_mes, pre_mes):
        res = AcManager()
        # count by user's id
        today_dic = {str(data[0]): data[1:] for data in total_mes.user_list}
        pre_dic = {data[0]: data[1:] for data in pre_mes.user_list}

        res.crawled_time = total_mes.crawled_time
        res.col_id = total_mes.col_id
        res.user_list = [[user] + today_dic[user][:2] + (today_dic[user][2:] if pre_dic.get(user) is None
                                                         else ([{oj: today_dic[user][2][oj] if pre_dic[user][2].get(
            oj) is None else today_dic[user][2][oj] - pre_dic[user][2][oj] for oj in today_dic[user][2]}]
                                                               + [{oj: today_dic[user][3][oj] if pre_dic[user][3].get(
            oj) is None else today_dic[user][3][oj] - pre_dic[user][3][oj] for oj in today_dic[user][3]}]))
                         for user in today_dic]

        # for user in res.user_list:
        #     print(user[:3], user[-1])
        return res

    @staticmethod
    def generate_alarm_msg(user_id, user_name, oj_names):
        oj_name = DELIMITER.join(oj_names)
        date = DATETIME_FORMATE.format(datetime.datetime.now())
        return ALARM_TEMPLATE.format_map(vars())

    @staticmethod
    def run():
        pre = AcManager()
        pre.list_user()
        total = AcManager()
        total.list_user()
        total.get_count()
        today_manager = AcManager.get_today_mes(total, pre)
        today_manager.save_to_db()

# if __name__ == '__main__':
#     # headName = 'Count_list_'
#     # sufNameFormat = '%Y_%m_%d'
#     # today = datetime.datetime.today()
#     # oneDay = datetime.timedelta(days=1)
#     # yesterday = today - oneDay
#     # fileName = headName + today.strftime(sufNameFormat)
#     # preName = 'xls/total_' + yesterday.strftime(sufNameFormat)
#     # totalName = 'xls/total_' + today.strftime(sufNameFormat)
#     #
#     # # get pre ac info
#     # pre_acManager = AcManager()
#     # pre_acManager.get_pre()
#     #
#     # # get team info and count
#     # total_acManager = AcManager()
#     # # total_acManager.get_pre_info(totalName+'.xls')
#     # total_acManager.get_IDlist('xls/id_list.xls')
#     # total_acManager.get_count()
#     # # total_acManager.get_counts()
#     # total_acManager.save_count_to_xls(totalName + '.xls')
#     # # get Incremental
#     # today_acManager = AcManager.get_today_mes(total_acManager, pre_acManager)
#     # today_acManager.save_count_to_xls(fileName + '.xls')
#     pre = AcManager()
#     pre.get_pre()
#     total = AcManager()
#     total.get_IDlist('static/xls/id_list.xls')
#     total.get_count()
#     today_acManager = AcManager.get_today_mes(total, pre)
#     today_acManager.save_to_db()
