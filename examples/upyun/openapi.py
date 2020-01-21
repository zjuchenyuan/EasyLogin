from upyun import login, islogin, a
import random, string
from config import USERNAME, PASSWORD

def createtoken(name):
    x=a.post("https://api.upyun.com/oauth/tokens", {
        "username":USERNAME, "password":PASSWORD,
        "code": "".join(random.sample(string.ascii_letters+string.digits, 21)),
        "name": name,
        "scope": "global"
    })
    #print(x.json())
    return x.json()['access_token']

def query(url):
    from config import ACCESS_TOKEN
    x=a.get("https://api.upyun.com/"+url, headers={"Authorization":"Bearer "+ACCESS_TOKEN}, o=True, result=False)
    print(x.request.url)
    return x.json()

def post(url, data):
    from config import ACCESS_TOKEN
    x=a.post("https://api.upyun.com/"+url, headers={"Authorization":"Bearer "+ACCESS_TOKEN}, result=False, data=data)
    return x.json()

def getalldomain():
    buckets = query("buckets?limit=100")["buckets"]
    res = []
    for b in buckets:
        res.extend([i["domain"] for i in b["domains"] if i["status"]=="NORMAL" and (not i["domain"].endswith(".upcdn.net")) and (not i["domain"].endswith(".upaiyun.com")) ])
    return res

def purge(urls):
    return post("purge", {"urls":"\n".join(urls)})

if __name__ == "__main__":
    from pprint import pprint
    pprint(getalldomain())
    #print(createtoken("downloadlog"))