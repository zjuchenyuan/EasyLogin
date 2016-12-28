from EasyLogin import EasyLogin
import re
from urllib.parse import quote
a=EasyLogin.load("fangcloud.status")
BLOCKSIZE=10*1024*1024
BLOCKHINT="0MB" #upload unit is 10MB

def login(xh,password):
    """
    统一通行证的用户名密码
    """
    global a
    a.post("http://team.zju.edu.cn/xstd/zjulogin","uid={}&pwd={}&postflag=1&cmd=login".format(xh,password),result=False)
    x=a.get("http://fangcloud.zju.edu.cn/zju_sso/login",o=True,result=False)
    return x.headers["Location"]!="http://team.zju.edu.cn"

def islogin():
    """
    是否已经登录,如果已经登录返回token，否则False
    """
    global a
    a.get("http://fangcloud.zju.edu.cn/apps/files/home")
    t=a.b.find("input",{"id":"oc_requesttoken"})
    if t is None:
        return False
    else:
        return t["value"]


def upload(token,filename,data):
    """
    上传文件
    token:islogin()返回的token
    filename: 存储的文件名
    data:文件二进制数据

    返回服务器端的文件id
    """
    global a
    filename=quote(filename)
    x=a.post("http://fangcloud.zju.edu.cn:26/html5_upload/own",data,headers={"requesttoken":token,"X-File-Name": filename})
    result=x.json()
    if result.get("success")!=True:
        return False
    else:
        return result["new_file"]["typed_id"]

def share(token,fileid):
    """
    分享一个文件，fileid来自upload，返回文件分享链接file_unique_name
    可以反复执行，返回相同的分享链接
    """
    global a
    x=a.post("http://fangcloud.zju.edu.cn/apps/files/share",
             """{"access":"public","disable_download":"0","due_time":"never_expire","password_protected":false,"item_typed_id":"%s"}"""%fileid,
             headers={"requesttoken":token})
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
    page=a.get("http://fangcloud.zju.edu.cn/share/"+file_uniqe_name,result=False)
    x = finder.search(page)
    if x is None:
        raise Exception("share link does not exist")
    fileid = x.group(1)
    x=a.get("http://fangcloud.zju.edu.cn/apps/files/download?file_id={}&scenario=share".format(fileid),o=True)
    return x.headers["Location"]

def download_usingbeautifulsoup(file_uniqe_name):
    """
    使用BeautifulSoup的版本，看起来更易懂一点
    """
    a=EasyLogin()
    page=a.get("http://fangcloud.zju.edu.cn/share/"+file_uniqe_name)
    fileid = a.b.find("input",{"id":"typed_id"})["value"].split("file_")[1]
    x=a.get("http://fangcloud.zju.edu.cn/apps/files/download?file_id={}&scenario=share".format(fileid),o=True)
    return x.headers["Location"]

def block(fp):
    """
    使用分块上传解决大文件传输的内存问题
    每次产生一个BLOCKSIZE的数据进行传输，传输好后再读取下一个BLOCK
    :param fp: 文件读入，传入open(filename,"rb")
    :return: 用yield产生的generator，可以被EasyLogin(requests)正常处理
    """
    x = fp.read(BLOCKSIZE)
    i = 1
    while len(x):
        print("{}{}".format(i,BLOCKHINT))
        i+=1
        yield x
        del x
        x = fp.read(BLOCKSIZE)

def showdemo(fileid,file_unique_name):
    print("fileid:")
    print(fileid)
    print()
    print("Share Link:")
    print("http://fangcloud.zju.edu.cn/share/"+file_unique_name)
    print()
    print("Download Link (expire soon):")
    print(download(file_unique_name))

def save_to_file(uploadfilename,file_unique_name,logfilename):
    open(logfilename,"a").write("{}\t{}\n".format(uploadfilename,file_unique_name))

if __name__=="__main__":
    import sys
    token = islogin()
    if not token:
        print("Login!")
        login(sys.argv[2],sys.argv[3])
        a.save("fangcloud.status")
        token=islogin()
    block_generator=block(open(sys.argv[1],"rb"))
    fileid=upload(token,sys.argv[1],block_generator)
    file_unique_name=share(token,fileid)
    if(len(sys.argv)==5):
        from os import pathsep
        uploadfilename=sys.argv[1].split(pathsep)[-1]
        save_to_file(uploadfilename,file_unique_name,sys.argv[4])
        #Better print for md write
        print("![{}](http://api.chenyuan.me/fangcloud/{})".format(uploadfilename,file_unique_name))
    else:
        showdemo(fileid,file_unique_name)