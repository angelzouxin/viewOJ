from static.utils import userUtil, subInfoUtil, userRatingInfoUtil, ojProblemUtil
from datetime import date, timedelta
from static.utils.countOJUtil import Crawler
from decimal import Decimal

OJ_RATIO = {'default': 1, 'bzoj': 1.3, 'codeforces': 1.1}
OJ_AC_NUMS_RATIO = {'default': 1, 'bzoj': 1.3, 'codeforces': 2, 'zucc': 0.5, 'hdu': 1.3}
GRADIENT_NUMS = [50, 100, 200, 500]
GRADIENT_AC_RATIO = [0.1, 0.15, 0.35, 0.45]
GRADIENT_RATING_RATIO = [1500, 2500, 4000, 6000]
# 无系数最高5分
DEFAULT_RATE = 3
DEFAULT_RATIO = 1
DEFAULT_OJ_AC_NUMS_RATIO = 1
crawler = Crawler()


def getProblemRate(oj_name, ac_nums, sub_nums, rating):
    pro_rating = 5
    oj_ratio = getOjRatio(oj_name)
    oj_ac_nums_ratio = getOjACNumsRatio(oj_name)
    rating_influence_ratio = 1.5
    index = 1
    for rating_threshold in GRADIENT_RATING_RATIO:
        if rating_threshold > rating:
            break
        rating_influence_ratio -= 0.12 * index
        index += 1
    print(rating_influence_ratio)
    # 使用默认分数*oj分数系数
    if sub_nums == -1 and ac_nums == -1:
        pro_rating = DEFAULT_RATE
        return pro_rating * oj_ratio
    # 使用梯度人群计算题目分值
    for num in GRADIENT_NUMS:
        if num * oj_ac_nums_ratio > ac_nums:
            break
        pro_rating -= 1
    print(pro_rating)
    pro_rating = pro_rating * oj_ratio * rating_influence_ratio
    print(pro_rating)
    ac_ratio_threshold = GRADIENT_NUMS[1] * oj_ac_nums_ratio
    # 无提交总数或低于提交数影响最小阈值，只通过梯度做题目分值判断
    if sub_nums == -1 or sub_nums < ac_ratio_threshold:
        return pro_rating
    ac_ratio = ac_nums / sub_nums
    ac_ratio_influence = 1.2
    for ratio in GRADIENT_AC_RATIO:
        if ratio > ac_ratio:
            break
        ac_ratio_influence -= 0.1
    print(ac_ratio_influence)
    return pro_rating * ac_ratio_influence


def getOjRatio(oj_name):
    ratio = OJ_RATIO.get(oj_name)
    if ratio is None:
        ratio = DEFAULT_RATIO
    return ratio


def getOjACNumsRatio(oj_name):
    ratio = OJ_AC_NUMS_RATIO.get(oj_name)
    if ratio is None:
        ratio = DEFAULT_OJ_AC_NUMS_RATIO
    return ratio


def calculateUsersRating():
    users = userUtil.list_by_filter(yn=1)
    for user in users:
        user_id = user.userId
        user_yesterday_rating = userRatingInfoUtil.query(user_id, date.today() - timedelta(1))
        user_now_rating = userRatingInfoUtil.DEFAULT_RATING
        if user_yesterday_rating:
            user_now_rating = user_yesterday_rating.rating
        print('开始计算%s:%s今日rating，当前rating%s' % (user_id, user.userName, user_now_rating))
        increment_rating = calculateUserRating(user_id, user_now_rating)
        user_now_rating += increment_rating
        userRatingInfoUtil.upsert(user_id, user_now_rating)
        print('计算结束，当前rating为%s' % user_now_rating)


def calculateUserRating(user_id, rating):
    sub_infos = subInfoUtil.query(user_id)
    res = 0
    for sub_info in sub_infos:
        oj_id = sub_info.get('ojId')
        oj_name = sub_info.get('ojName')
        pro_id = sub_info.get('proId')
        pro_info = ojProblemUtil.query(oj_id, pro_id)
        ac_nums, sub_nums = None, None
        print(user_id, oj_id, oj_name, pro_id)
        if oj_name == 'vjudge':
            continue
        if pro_info and pro_info.crawlerDate == date.today():
            ac_nums = pro_info.acNums
            sub_nums = pro_info.subNums
        else:
            _pro_info = crawler.getProInfo(oj_name, pro_id)
            ac_nums = _pro_info[0] if _pro_info[0] is not None else -1
            sub_nums = _pro_info[1] if _pro_info[1] is not None else -1
            try:
                ojProblemUtil.upsert(oj_id, pro_id, ac_nums, sub_nums, date.today())
            except BaseException:
                print('插入oj%s题目%s相关信息时出错' % (oj_name, pro_id))
        res += getProblemRate(oj_name, ac_nums, sub_nums, rating)
    return (res + 1) // 1 if res - res // 1 >= 0.5 else res // 1
