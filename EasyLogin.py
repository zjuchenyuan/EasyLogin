# coding:utf-8
#TODO:
#support for json object post; support file upload
#more document is also needed
##UPDATE_LOG:
#2016/12/02
#adding w function; multiple User-Agent choice; proxies applied to https, get function can have a cachefile
#2016/11/25
#adding VIEWSTATE,save,load function
#2016/10/28
#"result=True" by default, delete "from_encoding=x.encoding"

import requests,pickle,os,random
from bs4 import BeautifulSoup
try:
    from urllib.parse import urlencode
except:
    print("Please Use Python3")
    exit()

UALIST=[
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
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36"
]

class EasyLogin():
    def __init__(self,cookie="",cookiefile=None,proxy=None):
        self.b = None
        self.s = requests.Session()
        UA=random.choice(UALIST)
        self.s.headers.update({'User-Agent': UA})
        self.s.cookies.update(cookie)
        self.proxies={'http':proxy,'https':proxy} if proxy is not None else None
        self.cookiefile='cookie.pickle'
        if cookiefile is not None:
            self.cookiefile = cookiefile
            try:
                self.s.cookies = pickle.load(open(cookiefile,"rb"))
            except:
                pass
                
    def showcookie(self):
        c = ""
        for i in self.s.cookies:
            c+= i.name+"="+i.value+";"
        return c
        
    def get(self,url,result=True,save=False,headers=None,o=False,cache=None):
        """
        url: a url, example: "http://ip.cn"
        result: using BeautifulSoup to handle the page, save to self.b
        save: save cookie or not
        headers: more headers to be sent
        o: return object or just page text
        cache: filename to write cache, if already exists, use cache rather than really get
        """
        if cache is not None and os.path.exists(cache):
          #try:
            if o:
                return pickle.load(open(cache,"rb"))
            else:
                return open(cache,"rb").read().decode()
          #except:
          #    pass
        x = self.s.get(url,headers=headers,allow_redirects=False,proxies=self.proxies)
        if result: 
            if 'Location' in x.headers or len(x.text)==0: return False
            else:self.b = BeautifulSoup(x.text.replace("<br>","\n").replace("<BR>","\n"),'html.parser')
        if save:  open(self.cookiefile,"wb").write(pickle.dumps(self.s.cookies))
        if o:#if you need object returned
            if cache is not None:
                open(cache,"wb").write(pickle.dumps(x))
            return x
        else:
            if cache is not None:
                open(cache,"wb").write(x.content)
            return x.text

    def post(self,url,data,result=True,save=False,headers=None):
        postheaders={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        if headers is not None:
            #postheaders.update(headers)
            postheaders=headers
        #print(data)
        x = self.s.post(url,data,headers=postheaders,allow_redirects=False,proxies=self.proxies)
        if result: self.b = BeautifulSoup(x.text.replace("<br>","\n").replace("<BR>","\n"),'html.parser')
        if save:  open(self.cookiefile,"wb").write(pickle.dumps(self.s.cookies))
        return x

    def post_dict(self,url,dict,result=True,save=False,headers=None):
        data = urlencode(dict)
        return self.post(url,data,result=result,save=save,headers=headers)
    
    def f(self,name,attrs):
        """
        find all tags matches name and attrs
        return text array
        """
        if self.b == None: return []
        return [i.text.replace('\r','').replace('\n','').replace('\t','').replace('  ','') for i in self.b.find_all(name,attrs=attrs)]
        
    def getList(self,searchString,elementName="a",searchTarget="href",returnType="href"):
        if self.b == None: return []
        result = []
        for element in self.b.find_all(elementName):
            #print(element)
            if searchString in element.get(searchTarget,""):
                result.append(element[returnType] if returnType!="element" else element)
        return result
     
    def VIEWSTATE(self):
         if self.b == None: return ""
         x = self.b.find("input",attrs={"name":"__VIEWSTATE"})
         if x == None: return ""
         return x["value"]
         
    def save(self,filename="EasyLogin.status"):
        open(filename,"wb").write(pickle.dumps(self))
    
    def load(filename="EasyLogin.status"):
        return pickle.load(open(filename,"rb"))

    def w(self,filename,content,method='w',overwrite=False):
        """
        just for write more simplely
        """
        if not overwrite and os.path.exists(filename):
            return
        with open(filename,method) as fp:
            fp.write(content)

if __name__ == '__main__':#sample code for get ip by "http://ip.cn"
    a = EasyLogin()
    page =a.get("http://ip.cn")
    IP,location = a.f("code",attrs={})
    print(IP)
    print(location)