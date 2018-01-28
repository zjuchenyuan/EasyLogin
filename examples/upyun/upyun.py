import sys
sys.path.append("../..")
from EasyLogin import EasyLogin
a=EasyLogin(cookiefile="upyun.status")

def login(username,password):
    global a
    data={"username":username,"password":password}
    print("Login...",end="")
    x=a.post_json("https://console.upyun.com/accounts/signin/",data,save=True)
    status=(x.get("msg",{}).get("messages",["error"])[0]=="登录成功")
    if status:
        print("Success")
    else:
        print("Login Failed")
        print(x)
        exit()
    return status

def islogin():
    global a
    x=a.get("https://console.upyun.com/api/",o=True)
    return "location" not in x.headers

def purge_rule_request(urls):
    """
    urls is multiple urls(must contain *) separated by '\n'
    :param urls: "\n".join([url1,url2])
    """
    global a
    x=a.post_json("https://console.upyun.com/api/buckets/purge/batch/",{"source_url": urls, "nofi": 0, "delay": 3600})
    try:
        result = [i["status"] for i in x["data"]]
    except:
        print(x)
        return "Error"
    return result

if __name__=="__main__":
    try:
        import config
        config.USERNAME
        config.PASSWORD
    except:
        print("Please write your USERNAME and PASSWORD in config.py")
        exit(1)
    if len(sys.argv)<2:
        print("Example: python3 upyun.py https://py3.io/*")
        print("Or you can: python3 upyun.py https://py3.io/@.html, @ stands for *")
    else:
        if not islogin():
            login(config.USERNAME,config.PASSWORD)
        # you can pass @ instead of *
        urls = "\n".join(sys.argv[1:]).replace("@", "*")
        print(purge_rule_request(urls))