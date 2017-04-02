from EasyLogin import EasyLogin
from pprint import pprint
a=EasyLogin()

def getlatest():
    a.get("http://www.qlmoney.com/gushi/",cache="cache_deleteme.html")
    res = []
    for i in a.b.find("div",{"class":"main_box news"}).find_all("li"):
        res.append([i.find("a").text,i.find("span").text,i.find("a")["href"]])
    return res

def getone(url):
    a.get(url,cache=True)
    abstract = a.b.find("div",{"class":"main_box descripition"}).text.strip()
    print(abstract)

if __name__=="__main__":
    getone(getlatest()[0][2])