import datetime
import sys
import time
from EasyLogin import EasyLogin, quote
from pprint import pprint

__author__ = 'zjuchenyuan'

"""
CC98 单帖用户回复数量统计， 可用于刷帖判断或水楼统计
命令行运行 参数为板块id和帖子id，输出该帖子回帖用户统计
输出格式为markdown表格，按用户频率降序 和 用户注册时间升序
依赖于EasyLogin, 欢迎Star: https://github.com/zjuchenyuan/EasyLogin
"""

DOMAIN = 'https://www.cc98.org/'  # 使用安全的https
COOKIE = ''  # 这里可能需要设置为你的cookie


def string2timestamp(s):
    """
    将时间字符串转为timestamp int
    可以用于对时间排序
    参考：https://stackoverflow.com/questions/9637838/convert-string-date-to-timestamp-in-python
    """
    return time.mktime(datetime.datetime.strptime(s, "%Y/%m/%d %H:%M:%S").timetuple())


def getpostuser_page(a, boardid, postid, page=None, cache=None):
    """
    获取特定页面发帖/回复用户名称列表
    本函数会利用EasyLogin提供的缓存机制以减少网络请求
    这基于回复者的帖子不会被删除的假设，如果该假设不成立你需要手工删除缓存文件
    """
    #print("getpostuser_page", page, cache)
    if page is not None:
        a.get(DOMAIN + "dispbbs.asp?BoardID={boardid}&id={postid}&page=&star={page}".format(**locals()), cache=cache)
    users = [i.find('b').text for i in a.b.find_all("span", {"style": "color: #000066;"})]
    return users


def getreplycount(a, boardid, postid):
    """
    返回帖子目前回帖数目 int
    楼主的发帖也计入其中（没人回复就是1）
    """
    a.get(DOMAIN + "dispbbs.asp?BoardID={boardid}&id={postid}&page=&star=1".format(**locals()))
    result = a.b.find("span", {"id": "topicPagesNavigation"}).find('b').text
    return int(result)


def getpagecount(a, boardid, postid):
    """
    这个帖子一共有多少页
    """
    number = getreplycount(a, boardid, postid)
    return (number // 10 + 1) if number % 10 != 0 else number // 10 # 参考自： https://github.com/zjuchenyuan/cc98/blob/e5922f9f3e523de68ba2faffbb469a83821f91e8/xinling.py#L211


def getpostuser_frequencydict(a, boardid, postid, pagefromto=None):
    """
    输入板块boardid，帖子postid和页面范围pagefromto，返回发帖频率dict
    如果不指定pagefromto，则会自动选择全部页面
    如果一个页面是完整的(不是最后一页), 将启用缓存 详见getpostuser_page函数
    """
    result = []
    if pagefromto is None:
        pagefromto = list(range(1, getpagecount(a, boardid, postid) + 1))
    lastpage = pagefromto.pop()
    for i in pagefromto:
        result.extend(getpostuser_page(a, boardid, postid, page=i, cache=True))
    result.extend(getpostuser_page(a, boardid, postid, page=lastpage, cache=None))
    return {i: result.count(i) for i in set(result)}


def getuserregistertime(a, quoted_username):
    """
    输入用户名(已经urlencode过的)，返回注册时间字符串
    """
    x = a.get(DOMAIN + "dispuser.asp?name={quoted_username}".format(**locals()), result=False, cache=True)
    result = x.split("注册时间：")[1].split("<", maxsplit=2)[0].strip()
    return result


def display(a, data):
    """
    将统计数据生成markdown表格，print到屏幕
    """
    display = "|username|count|registertime|\n|--|--|--|\n"
    for username, count in data:
        quoted_username = quote(bytes(username, encoding='utf-8'))
        regtime = getuserregistertime(a, quoted_username)
        display += "|[{username}](/dispuser.asp?name={quoted_username})|{count}|`{regtime}`|\n".format(
            **locals()) 
    print(display)


def main():
    a = EasyLogin(cookie=COOKIE)
    if len(sys.argv) < 3:
        print("Usage: python3 {filename} boardid postid".format(filename=sys.argv[0]))
        return
    _data = getpostuser_frequencydict(a, sys.argv[1], sys.argv[2])
    data = sorted(_data.items(), key=lambda i: i[1], reverse=True)
    print("# 帖数统计（截至目前{count}帖）".format(count=sum([j for i, j in data])))
    print("## 按照发帖频率排序")
    display(a, data)
    data = sorted(_data.items(),
                  key=lambda i: string2timestamp(getuserregistertime(a, quote(bytes(i[0], encoding='utf-8')))))
    print("## 按注册时间排序")
    display(a, data)


if __name__ == '__main__':
    main()
