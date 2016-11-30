# coding:utf-8
#TODO:
#multiple User-Agent; support for json object post; support file upload
#more document is also needed
#UPDATE_LOG:
#2016/11/25
#adding VIEWSTATE,save,load function
#2016/10/28
#"result=True" by default, delete "from_encoding=x.encoding"

import requests,pickle
from bs4 import BeautifulSoup
try:
    from urllib.parse import urlencode
except:
    print("Please Use Python3")
    exit()

class EasyLogin():
    def __init__(self,cookie="",cookiefile=None,proxy=None):
        self.b = None
        self.s = requests.Session()
        self.s.headers.update({'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"})
        self.s.cookies.update(cookie)
        self.proxies={'http':proxy} if proxy is not None else None
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
        
    def get(self,url,result=True,save=False,headers=None,o=False):
        x = self.s.get(url,headers=headers,allow_redirects=False,proxies=self.proxies)
        if result: 
            if 'Location' in x.headers or len(x.text)==0: return False
            else:self.b = BeautifulSoup(x.text.replace("<br>","\n").replace("<BR>","\n"),'html.parser')
        if save: open(self.cookiefile,"wb").write(pickle.dumps(self.s.cookies))
        if o:#if you need object returned
            return x
        else:
            return x.text

    def post(self,url,data,result=True,save=False,headers=None):
        postheaders={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        if headers is not None:
            #postheaders.update(headers)
            postheaders=headers
        #print(data)
        x = self.s.post(url,data,headers=postheaders,allow_redirects=False,proxies=self.proxies)
        if result: self.b = BeautifulSoup(x.text,'html.parser')
        if save:  open(self.cookiefile,"wb").write(pickle.dumps(self.s.cookies))
        return x

    def post_dict(self,url,dict,result=True,save=False,headers=None):
        data = urlencode(dict)
        return self.post(url,data,result=result,save=save,headers=headers)
    
    def f(self,name,attrs):#find_all
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
        
if __name__ == '__main__':#sample code for get ip by "http://ip.cn"
    a = EasyLogin()
    page =a.get("http://ip.cn")
    IP,location = a.f("code",attrs={})
    print(IP)
    print(location)