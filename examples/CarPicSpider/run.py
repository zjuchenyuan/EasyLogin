from EasyLogin import EasyLogin
a=EasyLogin()
a.get("http://m.autohome.com.cn/")
brands = a.b.find("div",{"class":"brand"})
for one in brands.find_all("a"):
    print(one.text,one["href"])