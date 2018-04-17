# coding=utf-8

import http.cookiejar
import json
import time
import random
import re
from lxml import etree

import urllib
from urllib import parse
from urllib import request

__author__ = 'zouxin'


class Crawler:
    '''
    This is the main crawler which contains a dictionary.
    This dictionary's key is the judge name,value is a set that contains each problem that user has ACed.
    As for submit condition , just store the number.
    '''
    name = ''
    dict_name = {}
    acArchive = {}
    submitNum = {}
    # OJ's name : [user,user]
    wrongOJ = {}
    # match dictionary.dict[oj]:[acRegex],[submitRegex]
    matchDict = {}
    supportedOJ = ['poj', 'hdu', 'zoj', 'codeforces', 'fzu', 'acdream', 'bzoj', 'ural', 'csu', 'hust', 'spoj', 'sgu',
                   'vjudge', 'bnu', 'uestc', 'zucc', 'codechef']

    def __init__(self, query_name={}):
        '''
        This is the initial part which describe the crawler opener.
        '''
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
        }
        self.cookie = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie))
        self.dict_name = query_name
        self.name = query_name.get('default')
        '''
        initialize all the data structure
        '''
        for oj in self.supportedOJ:
            # for achive ,use set
            self.submitNum[oj] = 0
            self.acArchive[oj] = set()
            # for problem , use list
            self.wrongOJ[oj] = []

        '''
        read the dictionary which guide spider to browser website and how to match information
        '''

    def getNoAuthRules(self):
        import configparser
        import os
        cf = configparser.ConfigParser()
        config_file_path = os.path.join(os.path.dirname(__file__), "regexDict.ini")
        cf.read(config_file_path)
        # travel all the useable site
        return [(oj, cf.get(oj, 'website'), cf.get(oj, 'acRegex'), cf.get(oj, 'submitRegex')) for oj in cf.sections()]

    def actRegexRules(self, html, acRegex, submitRegex, oj):
        submission = re.findall(submitRegex, html, re.S)
        acProblem = re.findall(acRegex, html, re.S)
        # print '# submission : ', submission
        # print '# problem : ', acProblem
        # for submit
        try:
            self.submitNum[oj] += int(submission[0])
            yield oj, len(set(acProblem)), submission[0]
        except:
            self.wrongOJ[oj].append(self.name)
            yield oj, 0, 0
        # for AC merge all the information
        self.acArchive[oj] = self.acArchive[oj] | set(acProblem)

    def followRules(self, oj, website, acRegex, submitRegex):
        name = self.name
        req = urllib.request.Request(
            url=website % name,
            headers=self.headers
        )
        try:
            html = self.opener.open(req).read(timeout=5)
        except:
            self.wrongOJ[oj].append(name)
            return 0
        submission = re.findall(submitRegex, html, re.S)
        acProblem = re.findall(acRegex, html, re.S)
        print('# submission : ', submission)
        print('# problem : ', acProblem)
        # for submit
        try:
            self.submitNum[oj] += int(submission[0])
        except:
            self.wrongOJ[oj] = name
            return 0
        # for AC merge all the information
        self.acArchive[oj] = self.acArchive[oj] | set(acProblem)
        return html

    def getInfoNoAuth(self, query_name='lqybzx'):
        '''
        This function only browser the website without authentication and also use regex.
        For 'poj','hdu','zoj','fzu','acdream','bzoj','ural','csu','hust','spoj','sgu','vjudge','bnu','cqu','uestc','zucc'
        :param query: query_name
        :return:
        '''
        import configparser
        import os
        if query_name == '':
            name = self.name
        else:
            name = query_name
        cf = configparser.ConfigParser()
        # configFilePath = os.path.join(os.path.dirname(__file__), "regexDict.ini")
        cf.read("static/regexDict.ini")
        # travel all the useable site
        for oj in cf.sections():
            website = cf.get(oj, 'website')
            acRegex = cf.get(oj, 'acRegex')
            submitRegex = cf.get(oj, 'submitRegex')
            name = self.getName(oj)
            if name is None:
                continue
            print(website % name)
            req = urllib.request.Request(
                url=website % name,
                headers=self.headers
            )
            try:
                html = str(self.opener.open(req, timeout = 5).read())
            except:
                self.wrongOJ[oj].append(name)
                continue
            submission = re.findall(submitRegex, html, re.S)
            acProblem = re.findall(acRegex, html, re.S)
            print('# submission : ', submission)
            print('# problem : ', acProblem)
            # for submit
            try:
                self.submitNum[oj] += int(submission[0])
            except:
                self.wrongOJ[oj] = name
                continue
            # for AC merge all the information
            self.acArchive[oj] = self.acArchive[oj] | set(acProblem)
            # print submission[0],acProblem
            # return submission[0], acProblem

    def getACdream(self, query_name=''):
        oj = 'acdream'
        if query_name == '':
            name = self.getName(oj)
        else:
            name = query_name
        if name is None:
            return
        req = urllib.request.Request(
            url='http://acdream.info/user/' + name,
            headers=self.headers
        )
        html = ''
        try:
            html = str(self.opener.open(req).read())
        except:
            self.wrongOJ[oj].append(name)
            return 0
        submission = re.findall('Submissions: <a href="/status\?name=.*?">([0-9]*?)</a>', html, re.S)
        linkAddress = re.findall(
            r'List of <span class="success-text">solved</span> problems</div>(.*?)<div class="block block-warning">',
            html, re.S)
        try:
            acProblem = re.findall(r'<a class="pid" href="/problem\?pid=[0-9]*?">([0-9]*?)</a>', linkAddress[0], re.S)
            self.submitNum[oj] += int(submission[0])
        except:
            self.wrongOJ[oj].append(name)
            return 0
        self.acArchive[oj] = self.acArchive[oj] | set(acProblem)
        return submission[0], acProblem

    def getAsyncACdream(self, html, query_name=''):
        oj = 'acdream'
        if query_name == '':
            name = self.name
        else:
            name = query_name
        submission = re.findall('Submissions: <a href="/status\?name=.*?">([0-9]*?)</a>', html, re.S)
        linkAddress = re.findall(
            r'List of <span class="success-text">solved</span> problems</div>(.*?)<div class="block block-warning">',
            html, re.S)
        try:
            acProblem = re.findall(r'<a class="pid" href="/problem\?pid=[0-9]*?">([0-9]*?)</a>', linkAddress[0], re.S)
            self.submitNum[oj] += int(submission[0])
            self.acArchive[oj] = self.acArchive[oj] | set(acProblem)
            yield oj, len(acProblem), submission[0]
        except:
            self.wrongOJ[oj].append(name)
            yield oj, 0, 0

    def showsgu(self, query_name=''):
        oj = 'sgu'
        if query_name == '':
            name = self.name
        else:
            name = query_name
        postData = {
            'find_id': name
        }
        postData = urllib.parse.urlencode(postData).encode('utf-8')
        req = urllib.request.Request(
            url='http://acm.sgu.ru/find.php',
            headers=self.headers,
            data=postData
        )
        html = ''
        try:
            html = str(self.opener.open(req, timeout=5).read())
        except:
            self.wrongOJ[oj].append(name)
            return 0
        sem = re.findall(r'</h5><ul><li>[0-9]*?.*?<a href=.teaminfo.php.id=([0-9]*?).>.*?</a></ul>', html, re.S)
        # print sem
        try:
            temp = sem[0]
            req = urllib.request.Request(
                url='http://acm.sgu.ru/teaminfo.php?id=' + str(temp),
                headers=self.headers
            )
            result = self.opener.open(req, timeout=10)
            html = str(result.read())
            submission = re.findall(r'Submitted: ([0-9]*?)', html, re.S)
            acProblem = re.findall(r'<font color=.*?>([0-9]*?)&#160</font>', html, re.S)
            # get all the information
            self.submitNum[oj] += int(submission[0])
            self.acArchive[oj] = self.acArchive[oj] | set(acProblem)
            return submission[0], acProblem
        except:
            self.wrongOJ[oj].append(name)
            return 0

    def getCodeforces(self, query_name=''):
        '''
        get JSON information from codeforces API and parser it
        :param query_name:
        :return: Boolean value which indicates success
        '''
        oj = 'codeforces'
        if query_name == '':
            name = self.getName(oj)
        else:
            name = query_name
        if name is None:
            return
        print('start ' + oj)
        loopFlag = True
        loopTimes = 0
        count = 200
        startItem = 1 + loopTimes * count
        endItem = (loopTimes + 1) * count
        while loopFlag:
            '''
            use cycle to travel the information
            '''
            loopTimes += 1
            website = 'http://codeforces.com/api/user.status?handle=%s&from=%s&count=%s' % (name, startItem, endItem)
            # try to get information
            startItem = 1 + loopTimes * count
            endItem = count
            # updating data...
            try:
               jsonString = urllib.request.urlopen(website, timeout=5).read().decode('utf-8')
            except:
                self.wrongOJ[oj].append(name)
                print('wa')
                return 0
            import json
            data = json.loads(jsonString)
            if data[u'status'] == u'OK':
                if len(data[u'result']) == 0:
                    break
                else:
                    pass
                # store the submit number
                self.submitNum[oj] += len(data[u'result'])
                # print self.subcf
                for i in data[u'result']:
                    # only accept AC problem
                    if i[u'verdict'] == 'OK':
                        problemInfo = i[u'problem']
                        problemText = '%s%s' % (problemInfo[u'contestId'], problemInfo[u'index'])
                        self.acArchive[oj].add(problemText)
            else:
                break
        print('submission: ', self.submitNum[oj])
        print('problems: ', self.acArchive[oj])
        return True

    def asyncGetCodeforces(self, query_name=''):
        '''
        get JSON information from codeforces API and parser it
        :param query_name:
        :return: Boolean value which indicates success
        '''
        import tornado.httpclient
        oj = 'codeforces'
        print('start CodeForce')
        if query_name == '':
            name = self.getName(oj)
        else:
            name = query_name
        if name is None:
            return
        loopFlag = True
        loopTimes = 0
        count = 300
        startItem = 1 + loopTimes * count
        endItem = (loopTimes + 1) * count
        # init async part
        client = tornado.httpclient.AsyncHTTPClient()

        # loop start
        while loopFlag:
            '''
            use cycle to travel the information
            '''
            loopTimes += 1
            website = 'http://codeforces.com/api/user.status?handle=%s&from=%s&count=%s' % (name, startItem, endItem)
            # try to get information
            startItem = 1 + loopTimes * count
            endItem = count
            # updating data...
            try:
                # use async to rewrite the getting process
                req = tornado.httpclient.HTTPRequest(website, headers=self.headers, request_timeout=5)
                # jsonString = urllib2.urlopen(website).read()
                response = yield tornado.gen.Task(client.fetch, req)
                if response.code == 200:
                    jsonString = response.body
                else:
                    # raise a exception
                    raise BaseException
            except:
                self.wrongOJ[oj].append(name)
                return
            import json
            data = json.loads(jsonString)
            if data[u'status'] == u'OK':
                if len(data[u'result']) == 0:
                    break
                else:
                    pass
                print(data[u'result'])
                # store the submit number
                self.submitNum[oj] += len(data[u'result'])
                # print self.subcf
                for i in data[u'result']:
                    # only accept AC problem
                    if i[u'verdict'] == 'OK':
                        problemInfo = i[u'problem']
                        problemText = '%s%s' % (problemInfo[u'contestId'], problemInfo[u'index'])
                        self.acArchive[oj].add(problemText)
            else:
                break

    def getCodechef(self, query_name=''):
        '''
        get JSON information from codechef Get Request and parser it
        :param query_name:
        :return: Boolean value which indicates success
        '''
        oj = 'codechef'
        if query_name == '':
            name = self.getName(oj)
        else:
            name = query_name
        if name is None:
            return
        req = urllib.request.Request(
            url='https://www.codechef.com/recent/user?page=0&user_handle=%s' % name,
            headers=self.headers
        )
        json_string = ''
        try:
            json_string = self.opener.open(req).read().decode('utf8')
        except:
            self.wrongOJ[oj].append(name)
            return 0
        dataDict = json.loads(json_string)
        max_page = dataDict['max_page']
        if max_page == 0:
            self.submitNum[oj] += 0
            self.acArchive[oj] = self.acArchive[oj] | set()
            return 0
        for page_num in range(0, max_page):
            req = urllib.request.Request(
                url='https://www.codechef.com/recent/user?page={}&user_handle={}'.format(page_num, name),
                headers=self.headers
            )
            json_string = ''
            try:
                json_string = self.opener.open(req).read().decode('utf8')
            except:
                self.wrongOJ[oj].append(name)
                return 0
            dataDict = json.loads(json_string)
            html = str(dataDict['content'])
            acProblems = []
            submitNum = 0
            try:
                submission = re.findall(r'_blank', html, re.S)
                submitNum += len(submission)
                acProblem = re.findall(r"a href='.*?' title='' target='_blank'>.*?</a></td><td ><span title='accepted'",
                                       html, re.S)
                acProblems += [re.findall(r"'.*?'", pro)[0].strip("'") for pro in acProblem]
                print("pages is {}".format(page_num))
            except:
                self.wrongOJ[oj].append(name)
                return 0
                # print(self.acArchive[oj],self.submitNum[oj])
        self.acArchive[oj] = self.acArchive[oj] | set(acProblems)
        self.submitNum[oj] += submitNum
        return len(self.submission[oj])

    def getVjudge(self, query_name=''):
        '''
        We will set up a cache pool to restore the cookie and keep it
        :param query_name:
        :return:
        '''
        import tornado.httpclient
        oj = 'vjudge'
        if query_name == '':
            name = self.getName(oj)
        else:
            name = query_name
        if name is None:
            return
        client = tornado.httpclient.AsyncHTTPClient()
        VJheaders = {
            'Host': 'vjudge.net',
            'Origin': 'http://vjudge.net',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'deflate',
        }
        VJCrawlerheaders = {
            'Host': 'vjudge.net',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'deflate',
            'upgrade-insecure-requests': '1'
        }
        publicAccountDict = {
            'username': '2013300116',
            'password': '8520967123'
        }
        loginReq = urllib.request.Request(
            url='https://vjudge.net/user/login',
            data=urllib.parse.urlencode(publicAccountDict).encode("utf-8"),
            headers=VJheaders,
            method='POST'
        )
        cookie = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
        try:
            # hold the cookie
            response = opener.open(loginReq, timeout=20).read().decode('utf-8')
        except Exception as e:
            self.wrongOJ[oj] = name
            return
        # query the API
        loopFlag = True
        maxId = ''
        pageSize = 500
        status = '%20'
        while loopFlag:
            req = urllib.request.Request(
                url='https://vjudge.net/user/submissions?username=%s&pageSize=%s&status=%s&maxId=%s' % (
                    name, pageSize, status, maxId),
                headers=VJCrawlerheaders
            )
            try:
                # buf = StringIO.StringIO( opener.open(req).read().content)
                # gzip_f = gzip.GzipFile(fileobj=buf)
                jsonString = opener.open(req).read()
                # jsonString = gzip_f.read()
                dataDict = json.loads(jsonString.decode('utf-8'))
                dataList = dataDict['data']
            except Exception as e:
                self.wrongOJ[oj].append(name)
                break
            for vID, orignID, ojName, probID, result, execSeconds, execMemory, languages, codeLength, submitTime in dataList:
                oj = ojName.lower()
                # only extract AC status
                if result == 'AC':
                    self.acArchive['vjudge'].add('{}:{}'.format(ojName, probID))
                    if self.acArchive.get(oj) is not None:
                        self.acArchive[oj].add(probID)
                    else:
                        # initialize the dict, insert value set
                        self.acArchive[oj] = set().add(probID)
                else:
                    pass
                if self.submitNum.get(oj) is None:
                    self.submitNum[oj] = 1
                    if self.acArchive.get(oj) is None:
                        self.acArchive[oj] = set()
                else:
                    self.submitNum[oj] += 1
                # vjudge's submit is not added to total number
                self.submitNum['vjudge'] += 1
            break
        return 1

    def asyncGetVjudge(self, query_name=''):
        '''
        We will set up a cache pool to restore the cookie and keep it
        tornado will use it
        :param query_name:
        :return:
        '''
        import tornado.gen
        oj = 'vjudge'
        if query_name == '':
            name = self.getName(oj)
        else:
            name = query_name
        if name is None:
            return
        VJheaders = {
            'Host': 'vjudge.net',
            'Origin': 'http://vjudge.net',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'deflate',
            # 'Cookie':'ga=GA1.3.1416134436.1469179876',
        }
        VJCrawlerheaders = {
            'Host': 'vjudge.net',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'deflate',
            'upgrade-insecure-requests': '1'
            # 'Cookie':'ga=GA1.3.1416134436.1469179876',
        }
        publicAccountDict = {
            'username': '2013300116',
            'password': '8520967123'
        }
        website = 'http://vjudge.net/user/login'
        # init non-block part
        client = tornado.httpclient.AsyncHTTPClient()
        # auth
        authData = urllib.parse.urlencode(publicAccountDict).encode('utf-8')
        req = tornado.httpclient.HTTPRequest(website, headers=self.headers, request_timeout=5, method='POST',
                                             body=authData)

        cookie = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
        # client fetch the data
        print('yes')
        response = yield tornado.gen.Task(client.fetch, req)
        # response = client.fetch(req)
        if response.code == 200:
            # auth successfully
            print(response)
            pass
        else:
            print(response)
            self.wrongOJ[oj] = name
            return
        # query the API
        loopFlag = True
        maxId = None
        pageSize = 100
        status = None
        while loopFlag:
            req = urllib.request.Request(
                url='http://vjudge.net/user/submissions?username=%s&pageSize=%s&status=%s&maxId=%s' % (
                    name, pageSize, status, maxId),
                headers=VJheaders
            )
            try:
                jsonString = opener.open(req).read()
                dataDict = json.loads(jsonString)
                dataList = dataDict['data']
            except Exception as e:
                self.wrongOJ[oj].append(name)
                break
            for vID, orignID, ojName, probID, result, execSeconds, execMemory, languages, codeLength, submitTime in dataList:
                oj = ojName.lower()
                # only extract AC status
                if result == 'AC':
                    if oj in self.acArchive:
                        self.acArchive[oj].add(probID)
                    else:
                        # initialize the dict, insert value set
                        self.acArchive[oj] = set().add(probID)
                else:
                    pass
                self.submitNum[oj] += 1
                # vjudge's submit is not added to total number
                self.submitNum['vjudge'] += 1
        return

    def getUestc(self, query_name=''):
        oj = 'uestc'
        if query_name == '':
            name = self.getName(oj)
        else:
            name = query_name
        if name is None:
            return
        req = urllib.request.Request(
            url='http://acm.uestc.edu.cn/user/userCenterData/%s' % name,
            headers=self.headers,
        )
        try:
            jsonString = self.opener.open(req).read().decode('utf8')
        except:
            self.wrongOJ[oj].append(name)
            return 0
        dataDict = json.loads(jsonString)
        # detect AC item
        if dataDict['result'] == 'error':
            self.wrongOJ[oj].append(name)
            return 0
        else:
            for dictItem in dataDict['problemStatus']:
                if dictItem['status'] == 1:
                    self.acArchive[oj].add(dictItem['problemId'])
                else:
                    pass
            self.submitNum[oj] += len(dataDict['problemStatus'])
        return 1

    def getAsyncUestc(self, jsonString):
        oj = 'uestc'
        name = self.getName(oj)
        if name is None:
            return
        dataDict = json.loads(jsonString)
        # detect AC item
        if dataDict['result'] == 'error':
            self.wrongOJ[oj].append(name)
            yield oj, 0, 0
        else:
            ac = 0
            for dictItem in dataDict['problemStatus']:
                if dictItem['status'] == 1:
                    self.acArchive[oj].add(dictItem['problemId'])
                    ac += 1
                else:
                    pass
            self.submitNum[oj] += len(dataDict['problemStatus'])
            yield oj, ac, len(dataDict['problemStatus'])

    def getTotalACNum(self):
        '''
        get the total number from dictionary that store the AC data.
        :return: the total AC's
        '''
        totalNum = 0
        for key, value in self.acArchive.items():
            # value should be a set
            totalNum += len(value)
        return totalNum

    def getTotalSubmitNum(self):
        '''
        get the total number from dictionary that store the submit data
        :return:
        '''
        totalNum = 0
        for key, value in self.submitNum.items():
            if key != 'vjudge':
                totalNum += int(value)
            else:
                # discard the submission data about vjudge
                pass
        return totalNum

    def changeCurrentName(self, name):
        self.dict_name = name
        self.name = self.dict_name['default']
        return True

    def getName(self, oj_name):
        return self.dict_name.get(oj_name)

    def run(self):
        self.getInfoNoAuth()
        self.getACdream()
        # self.getCodechef()
        self.getCodeforces()
        # self.asyncGetCodeforces()
        self.getUestc()
        self.getVjudge()

    def getProInfo(self, oj_name, pro_id):
        if oj_name not in self.supportedOJ:
            print('%s is not support' % oj_name)
            raise Exception('%s is not support' % oj_name)
        try:
            time.sleep(round(random.random(), 2))
            if oj_name == 'codeforces':
                res = self.getProInfoCodeforces(pro_id)
                return res
            res = self.getProInfoNoAuth(oj_name, pro_id)
            return res
        except BaseException:
            print('爬取oj%s题目%s相关信息时出错' % (oj_name, pro_id))
            return [None, None]

    def getProInfoNoAuth(self, oj_name, pro_id):
        import configparser
        cf = configparser.ConfigParser()
        cf.read("static/regexDict.ini")
        problemsite = cf.get(oj_name, 'problemsite')
        problemSubRegex = cf.get(oj_name, 'problemSubRegex')
        problemAcRegex = cf.get(oj_name, 'problemAcRegex')
        req = urllib.request.Request(
            url=problemsite % pro_id,
            headers=self.headers
        )
        html = str(self.opener.open(req, timeout=10).read())
        submission = re.findall(problemSubRegex, html, re.S)
        accept = re.findall(problemAcRegex, html, re.S)
        submission = int(submission[0]) if len(submission) > 0 else None
        accept = int(accept[0]) if len(accept) > 0 else None
        print('# accept : ', accept)
        print('# submission : ', submission)
        return [accept, submission]

    def getProInfoCodeforces(self, pro_id):
        origin_pro = self.getCodeforcesProNumbser(pro_id)
        if origin_pro > [100000]:
            return [None, None]
        print('start crawler cf pro %s' % pro_id)
        problems = 'http://codeforces.com/problemset/page/%s'
        req = urllib.request.Request(
            url=problems % 1,
            headers=self.headers
        )
        html = self.opener.open(req, timeout=10).read()
        left_page = 1
        right_page = etree.HTML(html).xpath('//div[@class="pagination"]//span[@class="page-index"]/@pageindex')[-1]
        right_page = int(right_page)
        page_index = None
        while left_page <= right_page:
            page_index = (left_page + right_page) // 2
            time.sleep(round(random.random(), 2))
            req = urllib.request.Request(
                url=problems % page_index,
                headers=self.headers
            )
            html = self.opener.open(req, timeout=10).read()
            table = etree.HTML(html).xpath('//table[@class="problems"][1]/*')[1:]
            if len(re.findall('[^0-9]%s[^0-9a-zA-Z]' % pro_id, str(html), re.S)) == 0:
                max_pro_id = table[0].xpath('td[1]/a[1]/text()')[0].strip()
                min_pro_id = table[-1].xpath('td[1]/a[1]/text()')[0].strip()
                print(max_pro_id, min_pro_id)
                max_pro = self.getCodeforcesProNumbser(max_pro_id)
                min_pro = self.getCodeforcesProNumbser(min_pro_id)
                if origin_pro > max_pro:
                    right_page = page_index - 1
                else:
                    left_page = page_index + 1
                continue
            for td in table:
                _pro_id = td.xpath('td[1]/a[1]/text()')
                _solved = td.xpath('td[last()]/a[1]/text()')
                _pro_id = _pro_id[0].strip() if len(_pro_id) > 0 else None
                _solved = int(_solved[0].strip('\xa0x')) if len(_solved) > 0 else None
                if _pro_id == pro_id:
                    return [_solved, None]
        return [None, None]


    @staticmethod
    def getCodeforcesProNumbser(pro_id):
        proRegex = "([a-zA-Z]+|[0-9]+)"
        return list(map(lambda x: int(x) if x.isdigit() else x, re.findall(proRegex, pro_id, re.S)))


if __name__ == '__main__':
    a = Crawler(query_name={'default': 'sillyrobot', 'zucc': '31601185', 'vjudge': 'hxamszi', 'codeforces': 'yjc9696'})
    a.getProInfoCodeforces()
