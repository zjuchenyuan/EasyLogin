from EasyLogin import EasyLogin
from config import USERNAME,PASSWORD
a=EasyLogin.load("wbu.status")

def login(USERNAME,PASSWORD):
    global a
    print("Login!")
    a.get("http://ids.wbu.edu.cn/authserver/login?service=http://my.wbu.edu.cn/index.portal")
    lt = a.b.find("input",{"name":"lt"})["value"]
    execution = a.b.find("input",{"name":"execution"})["value"]
    x=a.post_dict("http://ids.wbu.edu.cn/authserver/login?service=http://my.wbu.edu.cn/index.portal",{
        "username":USERNAME,
        "password":PASSWORD,
        "lt":lt,
        "execution":execution,
        "_eventId":"submit",
        "rmShown":"1"}
    )
    ticket_url = x.headers.get("Location","")
    if ticket_url == "":
        return False # 登录失败，一般为密码错误
    x=a.get(ticket_url,o=True)
    if x.headers.get("Location","")!="http://my.wbu.edu.cn/index.portal":
        return False
    a.save("wbu.status")
    return True

def get_card_balance():
    global a
    from pprint import pprint
    import json
    x=a.get("http://my.wbu.edu.cn/pnull.portal?action=informationCenterAjax&.pen=information",o=True).content.decode()
    false = False
    true = True
    null = None
    x=eval(x[1:-1])
    amount = x[1]["description"].split("<span>")[1].split("<")[0]
    return amount

def islogin():
    global a
    x=a.get("http://my.wbu.edu.cn/pnull.portal?action=informationCenterAjax&.pen=information",o=True)
    if(x.status_code!=200):
        return False
    else:
        return True

if __name__ == "__main__":
    if islogin() or login(USERNAME,PASSWORD):
        print(get_card_balance())