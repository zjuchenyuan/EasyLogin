from EasyLogin import EasyLogin
from pypinyin import lazy_pinyin
a=EasyLogin()

def gethot():
    a.get("http://m.autohome.com.cn/")
    brands = a.b.find("div",{"class":"brand"})
    result = {}
    for one in brands.find_all("a"):
        name = one.text
        pinyin = ''.join(lazy_pinyin(name))
        href = "http://"+one["href"][2:] #url地址是形如//car.m.autohome.com.cn/brand/1/#pvareaid=100239，需要去掉前置的//
        result[one.text]=[href, pinyin]
    return result

def getbrand(url):
    """
    返回数组，其元素为：[名称，价格，类型，图片url，详情url]
    """
    a.get(url)
    items = a.b.find_all("li")
    result = []
    for one in items:
        name = one.find("h4").text
        price = one.find("p",{"class":"price"}).text
        leixin = one.find("p",{"class":"infor"}).text
        picture_url = "http://"+one.find("img")["src"][2:]
        detail_url = "http://"+one.find("a")["href"][2:]
        result.append([name,price,leixin,picture_url,detail_url])
    return result

if __name__ == "__main__":
    from pprint import pprint
    #print(gethot())
    pprint(getbrand("http://car.m.autohome.com.cn/brand/1/#pvareaid=100239"))