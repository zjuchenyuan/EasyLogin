from EasyLogin import EasyLogin
import re
from pprint import pprint
from urllib.parse import quote
a=EasyLogin.load("fangcloud.status")


def login(username,password):
    """
    使用账号(邮箱)和密码，选择“记住我”登录
    :param username:
    :param password:
    :return:
    """
    global a
    a.get("https://www.fangcloud.com/auth/login")
    token=a.b.find("input",{"name":"requesttoken"})["value"]
    x=a.post("https://www.fangcloud.com/auth/login",
             """{"identifier":"%s","password":"%s","remember_login":"1","scene":"login"}"""%(username,password),
             headers={"requesttoken":token,"X-Requested-With":"XMLHttpRequest"})
    result=x.json()
    if result["success"]!=True:
        return False
    else:
        return True

def islogin():
    """
    是否已经登录,如果已经登录返回token，否则False
    """
    global a
    a.get("https://www.fangcloud.com/apps/files/home")
    t=a.b.find("input",{"id":"oc_requesttoken"})
    if t is None:
        return False
    else:
        return t["value"]


def upload(token,filename,data):
    """
    上传文件，与浙大云盘的差异在于上传链接需要额外的请求
    token:islogin()返回的token
    filename: 存储的文件名
    data:文件二进制数据

    返回服务器端的文件id
    """
    global a
    filename=quote(filename)
    x=a.post("https://www.fangcloud.com/apps/files/presign_upload",
             """{"folder_id":0,"file_size":%d}"""%len(data),
             headers={"requesttoken": token, "X-Requested-With": "XMLHttpRequest"})
    result=x.json()
    if result["success"]!=True:
        return False
    upload_url=result["upload_url"]
    x=a.post(upload_url,
             data,
             headers={"requesttoken": token,"X-File-Name":filename})
    result=x.json()
    if result["success"]!=True:
        return False
    return result["new_file"]["typed_id"]

def share(token,fileid):
    """
    分享一个文件，fileid来自upload，返回文件分享链接file_unique_name
    可以反复执行，返回相同的分享链接
    """
    global a
    x=a.post("https://www.fangcloud.com/apps/files/share",
             """{"access": "public", "disable_download": "0", "due_time": "never_expire", "password_protected": false,"item_typed_id": "%s"}"""%fileid,
             headers={"requesttoken":token,"X-Requested-With": "XMLHttpRequest"})
    result=x.json()
    if result.get("success")!=True:
        return False
    else:
        return result["share_link"]["unique_name"]

finder=re.compile(r'''file_(\d+)''')

def download(file_uniqe_name):
    """
    获得一个分享链接的直接链接
    本函数可能被频繁调用，为优化性能不使用BeautifulSoup
    :param file_uniqe_name: 分享链接，来自share
    :return: 可以直接下载的url，一段时间后失效
    """
    a=EasyLogin()
    page=a.get("https://www.fangcloud.com/share/"+file_uniqe_name,result=False)
    fileid = finder.search(page).group(1)
    x=a.get("https://www.fangcloud.com/apps/files/download?file_id={}&scenario=share".format(fileid),o=True)
    return x.headers["Location"]


if __name__=="__main__":
    import sys
    token = islogin()
    if not token:
        print("Login!")
        login(sys.argv[2],sys.argv[3])
        a.save("fangcloud.status")
        token=islogin()
    fileid=upload(token,sys.argv[1],open(sys.argv[1],"rb").read())
    file_uniqe_name=share(token,fileid)
    print("fileid:")
    print(fileid)
    print()
    print("Share Link:")
    print("https://www.fangcloud.com/share/"+file_uniqe_name)
    print()
    print("Download Link (expire soon):")
    print(download(file_uniqe_name))
