import sys
sys.path.append("../..")
from EasyLogin import EasyLogin
a=EasyLogin(cookiefile="upyun.status")

def login(username,password):
    global a
    data={"username":username,"password":password}
    print("Login...",end="")
    x=a.post_json("https://console.upyun.com/accounts/signin/",data,save=True)
    status=(x.get("location","")=="/#/dashboard/")
    if status:
        print("Success")
    else:
        print("Failed")
        print(x)
    return status

def islogin():
    global a
    x=a.get("https://console.upyun.com/api/",o=True)
    return "location" not in x.headers

def purge_rule_request(urls):
    """
    :param urls: "\n".join([url1,url2])
    """
    global a
    x=a.get("https://console.upyun.com/purge/purge_rule/",o=True)
    xsrftoken=a.s.cookies["XSRF-TOKEN"]
    x=a.post_json("https://console.upyun.com/api/buckets/purge/batch/",{"source_url": urls, "nofi": 0, "delay": 3600},headers={"x-xsrf-token":xsrftoken})
    return [i["status"] for i in x["data"]]

if __name__=="__main__":
    import config
    if not islogin():
        login(config.USERNAME,config.PASSWORD)
    print(purge_rule_request("https://py3.io/*"))