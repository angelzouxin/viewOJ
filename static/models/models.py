import datetime


class user:
    def __init__(self, userId, userName):
        self.userId = userId
        self.userName = userName


class oj:
    def __init__(self, ojName, ojId=None):
        self.ojId = ojId
        self.ojName = ojName


class user_info:
    def __init__(self, userId, ojId, userOjId, uesrInfoId=None):
        self.uesrInfoId = uesrInfoId
        self.userId = userId
        self.ojId = ojId
        self.userOjId = userOjId


class sub_info:
    def __init__(self, proId, acDate=datetime.date.today(), userInfoId=None):
        self.userInfoId = userInfoId
        self.proId = proId
        self.acDate = acDate


class daily_info:
    def __init__(self, userInfoId, acTimes, subTimes, countDate=datetime.date.today()):
        self.userInfoId = userInfoId
        self.acTimes = acTimes
        self.subTimes = subTimes
        self.countDate = countDate


class user_daily:
    def __init__(self, userId, userName, info):
        self.userId = userId
        self.userName = userName
        self.dailyInfo = []
        self.dailyInfo.append(info)

    def __eq__(self, other):
        return self.userId == other.userId

    def addInfo(self, info):
        self.dailyInfo.append(info)


class info:
    def __init__(self, acTimes, subTimes, countDate):
        self.acTimes = acTimes
        self.subTimes = subTimes
        self.countDate = countDate
