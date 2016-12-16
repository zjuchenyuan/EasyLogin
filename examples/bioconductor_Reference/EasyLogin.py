# coding:utf-8

# TODO:
#   support for json object post; support file upload
#   more document is also needed
# UPDATE_LOG:
#  2016/12/16
#    Using PyCharm to write better code
#  2016/12/15
#    BeautifulSoup using "content" rather than "text" which requests returned
#  2016/12/02
#    adding w function; multiple User-Agent choice; proxies applied to https, get function can have a cachefile
#  2016/11/25
#    adding VIEWSTATE,save,load function
#  2016/10/28
#    "result=True" by default, delete "from_encoding=x.encoding"


try:
    from urllib.parse import urlencode, quote
except ImportError:
    print("Please Use Python3")
    exit()
import requests
import pickle
import os
import random
from bs4 import BeautifulSoup

UALIST = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36"]


class EasyLogin:
    def __init__(self, cookie="", cookiefile=None, proxy=None):
        self.b = None
        self.s = requests.Session()
        self.s.headers.update({'User-Agent': random.choice(UALIST)})
        self.s.cookies.update(cookie)
        self.proxies = {'http': proxy, 'https': proxy} if proxy is not None else None
        self.cookiefile = 'cookie.pickle'
        if cookiefile is not None:
            self.cookiefile = cookiefile
            try:
                self.s.cookies = pickle.load(open(cookiefile, "rb"))
            except FileNotFoundError:
                pass

    @property
    def cookie(self):
        c = ""
        for i in self.s.cookies:
            c += i.name + '=' + i.value + ";"
        return c

    def get(self, url, result=True, save=False, headers=None, o=False, cache=None):
        """
        HTTP GET method, default save soup to self.b
        :param url: a url, example: "http://ip.cn"
        :param result: using BeautifulSoup to handle the page, save to self.b (default True)
        :param save: save cookie or not
        :param headers: more headers to be sent
        :param o: return object or just page text
        :param cache: filename to write cache, if already exists, use cache rather than really get
        :return page text or object(o=True)
        """
        if cache is not None and os.path.exists(cache):
            if o:
                return pickle.load(open(cache, "rb"))
            else:
                return open(cache, "rb").read().decode()
        x = self.s.get(url, headers=headers, allow_redirects=False, proxies=self.proxies)
        if result:
            if not o and 'Location' in x.headers or len(x.text) == 0:
                return False
            else:
                page = x.content.replace(b"<br>", b"\n").replace(b"<BR>", b"\n")
                self.b = BeautifulSoup(page, 'html.parser')
        if save:
            open(self.cookiefile, "wb").write(pickle.dumps(self.s.cookies))
        if o:  # if you need object returned
            if cache is not None:
                open(cache, "wb").write(pickle.dumps(x))
            return x
        else:
            if cache is not None:
                open(cache, "wb").write(x.content)
            return x.text

    def post(self, url, data, result=True, save=False, headers=None):
        postheaders = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        if headers is not None:
            # postheaders.update(headers)
            postheaders = headers
        # print(data)
        x = self.s.post(url, data, headers=postheaders, allow_redirects=False, proxies=self.proxies)
        if result:
            page = x.content.replace(b"<br>", b"\n").replace(b"<BR>", b"\n")
            self.b = BeautifulSoup(page, 'html.parser')
        if save:
            open(self.cookiefile, "wb").write(pickle.dumps(self.s.cookies))
        return x

    def post_dict(self, url, dict, result=True, save=False, headers=None):
        data = urlencode(dict)
        return self.post(url, data, result=result, save=save, headers=headers)

    def f(self, name, attrs):
        """
        find all tags matches name and attrs
        :param name: Tag name
        :param attrs: dict, exmaple: {"id":"content"}
        :return: list of str(Tag text)
        """
        if self.b is None: return []
        return [i.text.replace('\r', '').replace('\n', '').replace('\t', '').replace('  ', '')
                for i in self.b.find_all(name, attrs)]

    def getlist(self, searchString, elementName="a", searchTarget="href", returnType=None):
        """
        get all urls which contain searchString
        Examples:
        get all picture:
            a.getlist("","img","src")
        get all css and js:
            a.getlist("css","link","href")
            a.getlist("js","script","src")

        :param searchString: keywords to search
        :param elementName: Tag name
        :param searchTarget: "href", "src", etc...
        :param returnType: "element" to return the Tag object, None to return element[searchTarget]
        :return: list
        """
        if returnType is None:
            returnType = searchTarget
        if self.b is None:
            return []
        result = []
        for element in self.b.find_all(elementName):
            if searchString in element.get(searchTarget, ""):
                result.append(element[returnType] if returnType != "element" else element)
        return result

    getList = getlist

    def VIEWSTATE(self):
        """
        Useful when you crack the ASP>NET website
        :return: quoted VIEWSTATE str
        """
        if self.b is None: return ""
        x = self.b.find("input", attrs={"name": "__VIEWSTATE"})
        if x is None: return ""
        return quote(x["value"])

    def save(self, filename="EasyLogin.status"):
        """
        save the object to file using pickle
        :param filename:
        :return:
        """
        open(filename, "wb").write(pickle.dumps(self))

    def load(filename='EasyLogin.status'):
        """
        load an object from file
        :param filename: file saved by pickle
        :return: the object
        """
        return pickle.load(open(filename, "rb"))

    @staticmethod
    def w(filename, content, method='w', overwrite=False):
        """
        just for write more simplely
        :param filename: str
        :param content: str or bytes
        :param method: 'w' or 'wb'
        :param overwrite: boolean
        :return: None
        """
        if not overwrite and os.path.exists(filename):
            return
        with open(filename, method) as fp:
            fp.write(content)

    def text(self, target=None):
        """
        Get all text in HTML, skip script and comment
        :param target: the BeatuifulSoup object, default self.b
        :return: list of str
        """
        if target is None:
            target = self.b
        from bs4 import Comment
        from bs4.element import NavigableString
        result = []
        for descendant in target.descendants:
            if not isinstance(descendant, NavigableString) or descendant.parent.name == "script" or isinstance(
                    descendant, Comment):
                continue
            data = descendant.strip()
            if len(data) > 0:
                result.append(data)
        return result

if __name__ == '__main__':  # sample code for get ip by "http://ip.cn"
    a = EasyLogin()
    page = a.get("http://ip.cn/")
    IP, location = a.f("code", attrs={})
    print(IP)
    print(location)

