import sys
sys.path.append("__pycache__")
from EasyLogin import EasyLogin,mymd5
import ast
import time

a=EasyLogin()
def login(username, password):
    html = a.get("https://danjuanapp.com/account/login", result=False)
    headers = ast.literal_eval([i for i in html.splitlines() if i.startswith("  headers: {")][0].replace("  headers: ","")[:-1])
    headers = {i:str(j) for i,j in headers.items()}
    headers["x-real-ip"]=""
    x = a.post("https://fund.xueqiu.com/provider/oauth/token", {
        "telephone":username, "password":mymd5(password), 
        "client_id":"9zZ4KCeWoU",
        "client_secret":"cnmBaU2CKZRBHT2w",
        "grant_type":"password",
        "auto_signup":"true",
        "scope":"all",
        "channel":"1300100141",
    }, headers=headers)
    res = x.json()
    assert res["result_code"]==0, "login failed: "+str(res)
    a.setcookie("accesstoken="+res["data"]['access_token'])
    return True

def query():
    data = a.get("https://danjuanapp.com/djapi/fundx/activity/user/today?source=luosiding", o=True).json()["data"]
    return data["signin"], data["total_count"]

def signin():
    x = a.post("https://danjuanapp.com/djapi/fundx/activity/user/signin?source=luosiding", "")
    data = x.json()
    print(data)
    return data

def getpic():
    x = a.get("https://danjuanapp.com/djapi/fundx/activity/user/signin/finished?source=luosiding", o=True)
    data = x.json()["data"]["knowledge_view"]["question"]
    return data

if __name__ == "__main__":
    from config import USERNAME,PASSWORD,SENTRY,GITLAB_TOKEN, GITLAB_PROJECT_ID
    import sentry_sdk
    sentry_sdk.init(SENTRY)
    login(USERNAME,PASSWORD)
    print(query())
    signin()
    picurl = getpic()
    print(picurl)
    filename = time.strftime("%Y%m%d.png")
    x = a.get(picurl, result=False, o=True)
    from uptogitlab import gitlab_add_file
    folder = time.strftime("%Y%m")
    commit = gitlab_add_file(GITLAB_TOKEN, GITLAB_PROJECT_ID, filename, folder, x.content, picurl.split("/")[-1])
    print(commit)