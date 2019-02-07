from EasyLogin import EasyLogin
from ocrapi import ocr
import sys
assert len(sys.argv)==3, "python "+sys.argv[0]+" <username> <password>"
a=EasyLogin.load(filename=sys.argv[1]+".status")

def login(username, password, retry=3):
    global a
    print("login!", username)
    a.get("https://uim.infinitus.com.cn/login")
    captcha_src = "https://uim.infinitus.com.cn"+a.b.find("img", {"id":"loginCode"})["src"]
    status, text, conf = ocr(a.get(captcha_src, result=False, o=True).content)
    t=0
    while status!="success" and t<10:
        a.get("https://uim.infinitus.com.cn/login")
        captcha_src = "https://uim.infinitus.com.cn"+a.b.find("img", {"id":"loginCode"})["src"]
        status, text, conf = ocr(a.get(captcha_src, result=False, o=True).content)
        t+=1
    x = a.post("https://uim.infinitus.com.cn/login", "captchaId="+captcha_src.split("?id=")[1].split("&")[0]+"&userName="+str(username)+"&password="+str(password)+"&captchaResponse="+text+"&chkRememberUsername=on&loginsubmit=%E7%99%BB%E5%BD%95", headers={"Origin":"https://uim.infinitus.com.cn", 
"Referer":"https://uim.infinitus.com.cn/login"})
    if x.status_code!=302:
        if retry>0:
            return login(username, password, retry=retry-1)
        else:
            raise Exception('exceed retry limit')
    a.save(filename=sys.argv[1]+".status")

def islogin():
    global a
    x = a.get("https://uim.infinitus.com.cn/cas/usercenter/userinfo/index", result=False, o=True)
    return x.status_code==200

def checkin(retry=False):
    global a
    x = a.post("https://f-activity.infinitus.com.cn/activity/front/myAccount/sign/signInSave", "")
    if x.status_code == 302:
        if not retry:
            url = "https://uim.infinitus.com.cn/login?service=https://f-activity.infinitus.com.cn/login/cas&forward=https://f-activity.infinitus.com.cn/&form=https://f-activity.infinitus.com.cn/login&appId=DLPM-ACTIVITLY&nextstep=https://f-activity.infinitus.com.cn/front/retrievePassword/public/validateCardNo"
            x = a.get(url, o=True)
            assert "window.location.href" in x.text
            url = x.text.split("'")[1]
            a.get(url, o=True, allow_redirects=True)
            a.save(filename=sys.argv[1]+".status")
            return checkin(retry=True)
        else:
            raise Exception("login loop?")
    print(x.headers["Date"])
    data = x.json()["returnObject"]
    print(data)

if __name__ == "__main__":
    if not islogin():
        login(*sys.argv[1:3])
    checkin()