from EasyLogin import EasyLogin
from urllib.parse import unquote
import re
from os.path import getsize
from urllib.parse import quote
import ntpath

__all__ = ['download', 'upload_by_collection', 'dirshare_listdir', 'dirshare_download']

a=EasyLogin.load("panzju.status")
BLOCKSIZE=1024*1024*10
BLOCKHINT="0MB" # 10MB as an unit

DOMAIN = "https://pan.zju.edu.cn"
APIDOMAIN = "https://api.chenyuan.me"
APIDEFNITION = {
    "direct_download": "panzju", #only this one is used in this file
    "html5_video_play": "zjuvideo",
    "vlc_plugin_play": "zjuvideomkv",
}
"""
API使用说明：
1) 单文件分享 302直接下载 
    /panzju/分享链接
    如：我们得到的分享链接如果是https://pan.zju.edu.cn/share/541849698040958b8b47d7b4d0
        则可以改写为这样来使用API服务：https://api.chenyuan.me/panzju/541849698040958b8b47d7b4d0
2) 文件夹分享 302直接下载其中一个文件 
    /panzju/分享链接/文件id
    如：https://api.chenyuan.me/panzju/55cce61ebbb6cbec43f7f3e26f/455003481647
3) 视频文件使用HTML5的video标签直接播放
    /zjuvideo/分享链接
    /zjuvideo/分享链接/文件id
    如：https://api.chenyuan.me/zjuvideo/35123e0bf9a42834b40eb4159b
    再如：https://api.chenyuan.me/zjuvideo/28c25672a486641f094c98f999/455001622253
4) 视频文件使用VLC网页控件播放，目前这个API不会检查输入的合法性
    /zjuvideomkv/分享链接
    /zjuvideomkv/分享链接/文件id
    如：https://api.chenyuan.me/zjuvideomkv/d29eb06ce5ef4e432a3e811119
你可以自行部署api服务器，可以自行修改API定义
TODO: 支持缩短API网址，提供API服务器部署说明
"""

"""
登录部分
"""
def login(username,password):
    """
    使用统一通行证登录新版浙大云盘pan.zju.edu.cn
    """
    global a
    x=a.get("https://pan.zju.edu.cn/sso/login",o=True)
    login_page=x.headers["Location"]
    login_service=unquote(login_page.split("service=")[1])
    x=a.post_dict("https://pan.zju.edu.cn/zjuLogin/SessionClient/login",{"username":username,"password":password,"service":login_service})
    login_status=x.json()
    if login_status["status"]!="success":
        return False
    login_service = login_status["service"]
    x=a.get(login_service,o=True)
    if "apps" in x.headers["Location"]:
        return True
    else:
        return False

def islogin():
    """
    是否已经登录,如果已经登录返回token，否则False
    """
    global a
    x=a.get(DOMAIN+"/apps/files/desktop/own",o=True)
    t=a.b.find("input",{"id":"request_token"})
    if t is None:
        return False
    else:
        return t["value"]

"""
上传 分享 下载
"""

def getfilename(path):
    """
    从可能的路径名中提取文件名
    """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def upload(token,filename,data,filesize=None):
    """
    上传文件，与亿方云基本一致，但需要引入dont_change_cookie
    token:islogin()返回的token
    filename: 存储的文件名
    data:文件二进制数据, 也可以为block generator
    filesize: 文件总大小，如果data为block generator，必须填入

    返回服务器端的文件id
    """
    global a
    filename=quote(getfilename(filename))
    if filesize is None:
        filesize = len(data)
    x=a.post(DOMAIN+"/apps/files/presign_upload",
             """{"folder_id":0,"file_size":%d}"""%filesize,
             headers={"requesttoken": token, "X-Requested-With": "XMLHttpRequest"})
    result=x.json()
    if result["success"]!=True:
        return False
    upload_url=result["upload_url"]
    x=a.post(upload_url,
             data,
             headers={"requesttoken": token,"X-File-Name": filename},dont_change_cookie=True)
    result=x.json()
    #print(result)
    if result["success"]!=True:
        return False
    return result["new_file"]["typed_id"]

def share(token,fileid):
    """
    分享一个文件，fileid来自upload，返回文件分享链接file_unique_name
    可以反复执行，返回相同的分享链接
    """
    global a
    x=a.post(DOMAIN+"/apps/files/share",
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
    page=a.get(DOMAIN+"/share/"+file_uniqe_name,result=False)
    tmp = finder.search(page)
    assert tmp is not None, "share link does not exist"
    fileid = tmp.group(1)
    x=a.get(DOMAIN+"/apps/files/download?file_id={}&scenario=share".format(fileid),o=True)
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

"""
文件管理部分
"""

def timestamp_to_string(timestamp):
    from datetime import datetime
    local_str_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return local_str_time

def mkdir(token, name, parent_id=0):
    """
    创建文件夹
    参数为：request_token、文件夹名称、文件夹父节点id（0表示根目录）
    返回新创建的文件夹str(id)，如"455000335224"
    """
    global a
    x = a.post(DOMAIN+"/apps/files/new_folder",
        """{"parent_folder_id":%s,"name":"%s"}"""%(str(parent_id), name),
        headers={"requesttoken":token,"X-Requested-With": "XMLHttpRequest"}
        )
    data = x.json()
    assert data["success"], "mkdir failed"
    return str(data["new_folder"]["id"])

def file_info(token, typed_id):
    """
    查询文件/文件夹信息
    typed_id: "folder_455000087071"
    返回[文件名称, 创建时间戳, 最后修改时间戳, 大小]
    """
    global a
    x = a.get(DOMAIN+"/apps/files/get_info?item_typed_id="+typed_id, 
        headers={"requesttoken":token,"X-Requested-With": "XMLHttpRequest"},
        result=False, o=True
        )
    data = x.json()
    assert data["success"], "get file info failed"
    item = data["item"]
    return [item["name"], item["created_at"], item["modified_at"], item["size"]]

def lsdir(a, folder_id, from_share=False, onlyneed=None, onlydirs=False):
    """
    a: EasyLogin的对象，可以为登录后的a也可以是访问分享页面后的a
    folder_id: 文件夹id, int和str类型均可
    from_share: 是否来自于分享
    
    返回[[名字, typed_id, 大小], ...]
    如果给出了onlyneed,则只返回这个元素的typed_id
    如果给定onlydirs=True,则只返回目录元素
    """
    print("lsdir: folderid="+str(folder_id))
    pageid = 1
    from_share_string = "scenario=share&" if from_share else ""
    data = a.get(DOMAIN+"/apps/files/file_list/{folder_id}?page_number={pageid}&{from_share_string}page_size=100".format(pageid=pageid, folder_id=folder_id, from_share_string=from_share_string),result=False,o=True).json()
    page_count = data["page_count"]
    result = []
    while pageid <= page_count:
        if pageid>1:
            data = a.get(DOMAIN+"/apps/files/file_list/{folder_id}?page_number={pageid}&{from_share_string}page_size=100".format(pageid=pageid, folder_id=folder_id, from_share_string=from_share_string),result=False,o=True).json()
        for child in data["children"]:
            one = [child["name"], child["typed_id"], child["size"]]
            if child["name"] == onlyneed:
                return child["typed_id"]
            if onlydirs and child["typed_id"].startswith("file_"):
                continue
            result.append(one)
        pageid+=1
    #sumsize = sum(i[2] for i in result)
    #print("Whole size: %f GB"%(sumsize/1024/1024/1024))
    return result

def path_to_typed_id(filepath):
    """
    将虚拟文件路径转为typed_id
    filepath: "/test/test2/test3"
    the last test3 can be folder or file
    return 'file_455003487756' or 'folder_455000086301', specially when path == '/', it returns '0' 
    """
    global a
    fid = "0"
    for name in filepath.split("/")[1:]:
        if name=="":
            continue
        fid = lsdir(a, fid, onlyneed=name).replace("folder_","")
    result = "folder_"+fid if not fid.startswith("f") else fid
    return result
    
def lsdir_recursive(path, fid=None, onlydirs=False):
    """
    输入路径或folder id，返回文件系统
    如果onlydirs=True，则返回文件夹的部分
    
    path: "/"
    return: {
        "目录名称": ("folder", "目录id", 整个文件夹字节数int),
        "文件名称": ("file", "文件id", 文件字节数int),
        "目录id": {又一个目录结构}
        ...
    }
    TODO: 我需要的数据结构应该是，需要平坦的数据结构而不是递归的模式:
    {
        "a": ("file", "文件id", 文件字节数),
        "b": ("folder", "目录id", 目录字节数),
        "b/c": ("file", ...)
    }
    """
    global a
    if fid is None:
        fid = path_to_typed_id(path).replace("folder_","")
    result = {}
    for item in lsdir(a, fid, onlydirs=onlydirs):
        type, fileid = item[1].split("_")
        if type=="folder":
            result[item[0]] = ("folder", fileid, item[2])
            result[fileid] = lsdir_recursive("", fileid, onlydirs=onlydirs)
        elif type=="file":
            result[item[0]] = ("file", fileid, item[2])
    return result

def path_to_id_via_cache(relative_path, cached_fs):
    """
    查询缓存得到(类型"file"或者"folder", fileid)
    """
    fs = cached_fs
    type, fileid = "folder", "0"
    for name in relative_path.split("/"):
        if name=="":
            continue
        if name not in fs:
            return False
        type, fileid, size = fs[name]
        if type=="file":
            return type,fileid
        else:
            fs = fs[fileid]
    return type,fileid

def mkdir_and_update_cache(token, name, parent_path, cached_fs):
    pass

"""
匿名上传部分
"""

def upload_by_collection(upload_link, path_to_file):
    """
    upload_link: 文件收集的链接，例如"abbee5b422f7a072b3bdaba4dba4ad3b"
    path_to_file: 路径名
    返回上传文件得到的服务器端的文件id
    """
    global a
    a.get(DOMAIN+"/collection/"+ upload_link)
    token = a.b.find("input",{"id":"request_token"})["value"]
    processid=a.b.find("input",{"id":"process"})["value"].split(":")[1].split(",")[0]
    filename=quote(getfilename(path_to_file))
    return upload_by_collection_detailed(token, processid, filename, getsize(path_to_file), block(open(path_to_file,"rb")))
    
def upload_by_collection_detailed(token, processid, filename, filesize, data):
    """
    详细的真实匿名上传过程 通过文件收集任务上传
    需要先从上传页面中得到token和processid
    上传过程类似upload. 但多了一步collection_submit的操作
    返回上传文件得到的服务器端的文件id
    """
    global a
    x = a.post(DOMAIN + "/apps/processes/presign_upload",
            """{"process_id":%s,"file_name":"%s","file_size":%d,"total_size":%d}"""%(processid, filename, filesize, filesize),
            headers={"requesttoken":token,"X-Requested-With": "XMLHttpRequest"}
        )
    result=x.json()
    if result["success"]!=True:
        print("[FAILED] presign_upload")
        print(result)
        return False
    upload_url=result["upload_url"]
    x=a.post(upload_url,
             data,
             headers={"requesttoken": token,"X-File-Name": filename},dont_change_cookie=True)
    result=x.json()
    if result["success"]!=True:
        print("[FAILED] upload")
        print(result)
        return False
    fileid = result["new_file"]["id"]
    x = a.post(DOMAIN+"/apps/processes/collection_submit", 
        """{"user_name":".","process_id":%s,"file_ids":[%s]}"""%(processid,fileid),
        headers={"requesttoken":token,"X-Requested-With": "XMLHttpRequest"},
        dont_change_cookie=True
        )
    result=x.json()
    if result["success"]!=True:
        print("[FAILED] collection_submit")
        print(result)
        return False
    return fileid

def dirshare_listdir(share_link):
    """
    share_link: 分享链接，例如"28c25672a486641f094c98f999"
    return [ [filename, file_typedid, filesize], ... ]
    """
    a = EasyLogin()
    a.get(DOMAIN+"/share/"+share_link)
    typed_id = a.b.find("input",{"id":"typed_id"})["value"]
    if "folder_" not in typed_id:
        return False
    folder_id = typed_id.split("folder_")[1]
    return lsdir(a, folder_id, from_share=True)

def dirshare_download(share_link, fileid):
    """
    获得一个文件夹分享链接的直接链接
    :param share_link: 分享链接
    :param fileid: 要下载的文件id，可以从dirshare_listdir查到
    :return: 可以直接下载的url，一段时间后失效
    """
    a=EasyLogin()
    page=a.get(DOMAIN+"/share/"+share_link,result=False)
    x=a.get(DOMAIN+"/apps/files/download?file_id={}&scenario=share".format(fileid),o=True)
    assert x.status_code==302, "download failed, please check misspelling or privilege setting"
    return x.headers["Location"]

def anonymous_upload(config_uploadlink, config_sharelink, path_to_file):
    """
    输入上传链接和分享链接和需要上传的文件，完成上传过程并测试下载API
    """
    import sys
    fileid = upload_by_collection(config_uploadlink, sys.argv[1])
    print(fileid)
    print("\nDownload Link:")
    print(getfilename(path_to_file))
    print("{APIDOMAIN}/{APINAME}/{sharelink}/{fileid}".format(APIDOMAIN=APIDOMAIN, APINAME=APIDEFNITION["direct_download"], sharelink=config_sharelink,fileid=fileid))
    print("\nTemporary download link:")
    print(dirshare_download(config_sharelink, fileid))

def logined_upload(token, path_to_file):
    """
    已经登录，执行上传流程
    """
    block_generator=block(open(path_to_file,"rb"))
    filesize=getsize(path_to_file)
    fileid=upload(token,path_to_file,block_generator,filesize)
    sharelink=share(token,fileid)
    return fileid, sharelink

def UI_login_upload(username=None, password=None):
    """
    上传sys.argv[0]文件，并输出分享链接
    这个函数不应该被import
    当username没有给出时将读取sys.argv[2]和sys.argv[3]
    """
    import sys
    token = islogin()
    if not token:
        if username is None:
            if len(sys.argv)<4:
                print("Usage: python3 {} filename username password".format(sys.argv[0]))
                exit(1)
            username = sys.argv[2]
            password = sys.argv[3]
        print("Login!")
        assert login(username, password)!=False, "Login failed"
        a.save("panzju.status")
        token=islogin()
    fileid, sharelink = logined_upload(token, sys.argv[1])
    print("fileid:")
    print(fileid)
    print()
    print("Share Link:")
    print("{DOMAIN}/share/{sharelink}".format(DOMAIN=DOMAIN,sharelink=sharelink))
    print("{APIDOMAIN}/{APINAME}/{sharelink}".format(APIDOMAIN=APIDOMAIN, APINAME=APIDEFNITION["direct_download"], sharelink=sharelink))
    print()
    print("Download Link (expire soon):")
    print(download(sharelink))

if __name__=="__main__":
    """
    如果没有config.py或者config.anonymous==False 将使用登录上传，登录需要的用户名密码可以从命令行给定或config给定
    相反地 config.anonymous==True 则意味着使用配置的上传链接和分享链接启动上传
    """
    import os
    import sys
    if len(sys.argv)<2:
        print("Usage: python3 {} filename".format(sys.argv[0]))
        exit(1)
    try:
        import config
        if getattr(config,"anonymous",False):
            print("anonymous upload!")
            anonymous_upload(config.uploadlink, config.sharelink, sys.argv[1])
            exit()
        if getattr(config,"username",None) is not None:
            UI_login_upload(config.username, config.password)
            exit()
    except ImportError:
        UI_login_upload()