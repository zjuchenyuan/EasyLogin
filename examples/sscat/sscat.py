from EasyLogin import EasyLogin
a= EasyLogin.load("sscat.status")

def islogin():
    global a
    if len(a.get("https://sscat.cn/control/"))<10:
        return False
    else:
        return True

def login(username,password):
    global a
    print("Login!")
    a.post("https://sscat.cn/index/login/",data="swapname={}&swappass={}".format(username,password))
    a.save("sscat.status")

def service_ids():
    global a
    a.get("https://sscat.cn/control/")
    service_ids=[i.split("/")[-2] for i in a.getlist("a") if "detail" in i]
    return service_ids

def liuliang(id):
    a.get("https://sscat.cn/control/detail/{}/".format(id))
    return a.b.find("th",text="流量使用状态").find_next("td").text
    
if not islogin():
    import sys
    login(sys.argv[1],sys.argv[2])

for i in service_ids():
    print(liuliang(i))
