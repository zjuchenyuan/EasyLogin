# coding=utf-8
from EasyLogin import EasyLogin, unquote, quote
import re
from os.path import getsize
import ntpath
import os
import sys
import json
try:
    import err_hunter as traceback
except:
    import traceback

__all__ = ['download', 'upload_by_collection', 'dirshare_listdir', 'dirshare_download', 'upload_directory']


try:
    import config as _config
    _statusfile = _config.statusfile
except:
    _statusfile = "./panzju.status"

try:
    a = EasyLogin.load(_statusfile)
except:
    a = EasyLogin()
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
def login(username,password, _a=None):
    """
    使用统一通行证登录新版浙大云盘pan.zju.edu.cn
    """
    if _a is None:
        global a
    else:
        a = _a
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

def islogin(_a=None):
    """
    是否已经登录,如果已经登录返回token，否则False
    """
    if _a is None:
        global a
    else:
        a = _a
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

def safefilename(filename):
    for x in r"""\/?:*"'><|""":
        filename = filename.replace(x,"")
    return filename

def upload(token, filename, data, filesize=None, folder_id=0, retry=5, fencrypt=None, _a=None):
    """
    上传文件，与亿方云基本一致，但需要引入dont_change_cookie
    token:islogin()返回的token
    filename: 存储的文件名
    data:文件二进制数据, 也可以为block generator
    filesize: 文件总大小，如果data为block generator，必须填入
    folder_id: 上传的目的文件夹id
    fencrypt: { #4个元素的dict
        fencrypt_filename(filename): 对文件名进行加密的函数，返回加密后的文件名ASCII 建议base64
        fencrypt_data(data_generator): 对文件内容进行加密的函数，输入文件内容的generator，返回密文的generator；即使输入的data不是生成器也会被转为list传入
        fencrypt_addlen: int 由于文件加密增加的字节数，一般就是iv的长度
        fencrypt_callback(filename_plaintext, filename_ciphertext, folder_id, fileid): 上传成功后进行回调，便于存储加密信息，传入原文件名、加密文件名、上传目标目录id、上传得到的文件ID， 返回None
    }
    返回服务器端的文件id
    """
    if fencrypt is not None:
        fencrypt_filename = fencrypt.get("fencrypt_filename",None)
        fencrypt_data = fencrypt.get("fencrypt_data",None)
        fencrypt_addlen = fencrypt.get("fencrypt_addlen",0)
        fencrypt_callback = fencrypt.get("fencrypt_callback",None)
    else:
        fencrypt_filename = fencrypt_data = fencrypt_callback = None
        fencrypt_addlen = 0
    
    if _a is None:
        global a
    else:
        a = _a
    print("upload: filename={filename}, folder_id={folder_id}".format(**locals()))
    _filename = safefilename(getfilename(filename))
    
    if fencrypt_filename is not None: # for encrypting filename
        filename_plaintext = _filename
        _filename = fencrypt_filename(_filename)
        filename_ciphertext = _filename
    else:
        filename_plaintext = filename_ciphertext = _filename
    
    try:
        filename=quote(_filename)
    except:
        print("[ERROR] filename encoding is not utf-8! \nYou may need to convert filename encoding to utf-8 before we can continue. Have a look at https://py3.io/code/fixgbknames.py")
        raise
    if filesize is None:
        filesize = len(data)
    filesize += fencrypt_addlen
    x=a.post(DOMAIN+"/apps/files/presign_upload",
             """{"folder_id":%s,"file_size":%d}"""%(str(folder_id),filesize),
             headers={"requesttoken": token, "X-Requested-With": "XMLHttpRequest", "Content-Type":"text/plain;charset=UTF-8"})
    try:
        result=x.json()
    except json.JSONDecodeError:
        if retry>0:
            return upload(token, filename, data, filesize, folder_id, retry = retry-1, fencrypt=fencrypt)
        else:
            raise
    if result["success"]!=True:
        print(result)
        return False
    upload_url=result["upload_url"]
    
    if fencrypt_data is not None: # add support for data encryption
        is_stream = all([
            hasattr(data, '__iter__'),
            not isinstance(data, (str, bytes, list, tuple, dict))
        ])
        if not is_stream:
            data_to_encrypt = [data] # change data to a list for calling fencrypt_data
        else:
            data_to_encrypt = data
        data = fencrypt_data(data_to_encrypt)
    
    x=a.post(upload_url,
             data,
             headers={"requesttoken": token,"X-File-Name": filename},dont_change_cookie=True)
    result=x.json()
    if "success" not in result or result["success"]!=True:
        print(result)
        return False
    ret = result["new_file"]["typed_id"]
    
    if fencrypt_callback is not None:
        try:
            fencrypt_callback(filename_plaintext, filename_ciphertext, folder_id, ret)
        except:
            traceback.print_exc()
            pass # exception happened in callback should not have no influence
    return ret

def share(token,fileid):
    """
    分享一个文件，fileid来自upload，返回文件分享链接file_unique_name
    可以反复执行，返回相同的分享链接
    """
    global a
    data = """{"access": "public", "disable_download": "0", "due_time": "never_expire", "password_protected": false,"item_typed_id": "%s"}"""%fileid
    x=a.post(DOMAIN+"/apps/files/share",
             data,
             headers={"requesttoken":token,"X-Requested-With": "XMLHttpRequest", "Content-Type":"text/plain;charset=UTF-8"})
    try:
        result=x.json()
    except:
        print(x.text)
        raise
    if result.get("success")!=True:
        return False
    else:
        return result["share_link"]["unique_name"]

def getshareid(folder_id):
    """
    输入一个目录id，如"455000399429"
    返回其已经存在的分享链接，如"11385b2387f890c195abd7ac14"
    """
    global a
    x = a.get("{DOMAIN}/apps/files/get_share_info?item_typed_id=folder_{folder_id}".format(DOMAIN=DOMAIN, folder_id=folder_id), result=False, o=True)
    result = x.json()
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
    x=a.get(DOMAIN+"/apps/files/download?file_id={}&scenario=share".format(fileid), o=True, result=False)
    return x.headers["Location"]

def delete_files(token, fileids, _a=None):
    if _a is None:
        global a
    else:
        a = _a
    fileids = list(fileids)
    data = """{"item_typed_ids":["%s"]}"""%('", "'.join(fileids))
    x=a.post(DOMAIN+"/apps/files/delete",
             data,
             headers={"requesttoken":token,"X-Requested-With": "XMLHttpRequest", "Content-Type":"text/plain;charset=UTF-8"})
    return x.json()["success"]
    

class NotLoginException(Exception):
    pass

class SharelinkNotExistsException(Exception):
    pass

class LoginedDownload_UnknownError(Exception):
    pass

def logined_download(sharelink, a):
    """
    在已经登录的情况下获取下载直链
    这是一个在download失败情况下的替补方案，可以下载到权限设置为仅学校成员访问的分享链接
    :param a: 已经登录的EasyLogin对象
    :param sharelink: 分享链接
    :return: 可以直接下载的url，一段时间后失效
    """
    x = a.get(DOMAIN+"/share/"+sharelink, o=True, result=False)
    if "Location" in x.headers:
        """
        发生跳转，自己发布的分享链接或者没有登录
        """
        if "login" in x.headers["Location"]:
            raise NotLoginException()
        else:
            fileid = x.headers["Location"].split("file/")[1]
            x = a.get("{DOMAIN}/apps/files/download?file_id={fileid}".format(DOMAIN=DOMAIN,fileid=fileid), o=True, result=False)
            if x.status_code != 302:
                raise LoginedDownload_UnknownError(x.text)
            return x.headers["Location"]
    else:
        """
        没有跳转，是别人的链接
        """
        page = x.text
        tmp = finder.search(page)
        assert tmp is not None, "share link does not exist"
        fileid = tmp.group(1)
        x=a.get(DOMAIN+"/apps/files/download?file_id={}&scenario=share".format(fileid), o=True, result=False)
        return x.headers["Location"]

def block(fp, showhint=True):
    """
    使用分块上传解决大文件传输的内存问题
    每次产生一个BLOCKSIZE的数据进行传输，传输好后再读取下一个BLOCK
    :param fp: 文件读入，传入open(filename,"rb")
    :param showhint: 是否显示上传进度提示，默认设置为每上传10MB前提示一次
    
    :return: 用yield产生的generator，可以被EasyLogin(requests)正常处理
    """
    x = fp.read(BLOCKSIZE)
    i = 1
    while len(x):
        if showhint:
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
    如果重名文件夹已经存在，抛出FileExistsError异常
    """
    global a
    print("mkdir: name={name}, parent_id={parent_id}, token={token}".format(**locals()))
    data = ("""{"parent_folder_id":%s,"name":"%s"}"""%(str(parent_id), name)).encode('utf-8')
    x = a.post(DOMAIN+"/apps/files/new_folder",
        data,
        headers={"requesttoken":token,"x-requested-with": "XMLHttpRequest", "Content-Type":"text/plain;charset=UTF-8"}
        )
    try:
        data = json.loads(x.text)
    except:
        data = {"success": False}
    if "success" not in data or data["success"]!=True:
        assert "name_conflicts" in x.text, "Unkown error"+x.text
        raise FileExistsError("failed to create {name} under folder_{parent_id}. data={data}".format(**locals()))
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

def lsdir(a, folder_id, from_share=False, onlyneed=None, onlydirs=False, onlyneed_return_size=False):
    """
    a: EasyLogin的对象，可以为登录后的a也可以是访问分享页面后的a
    folder_id: 文件夹id, int和str类型均可
    from_share: 是否来自于分享
    
    返回[[名字, typed_id, 大小], ...]
    如果给出了onlyneed,则只返回这个元素的typed_id; 如果同时又给出了onlyneed_return_size=True，则返回(type, fileid, size)
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
                if not onlyneed_return_size:
                    return child["typed_id"]
                else:
                    return (one[1].split("_")[0], one[1].split("_")[1], one[2])
            if onlydirs and child["typed_id"].startswith("file_"):
                continue
            result.append(one)
        pageid+=1
    #sumsize = sum(i[2] for i in result)
    #print("Whole size: %f GB"%(sumsize/1024/1024/1024))
    if onlyneed is not None:
        raise FileNotFoundError(onlyneed+" does not exist in folder "+folder_id)
    return result

def path_to_typed_id(filepath, cache=None, onerror="raise"):
    """
    将路径path转为(type,fileid)
    如果有缓存且缓存的path匹配，则只查询缓存, 此时的输入应该为相对路径, 也支持输入绝对路径自动替换
    filepath: "/test/test2/test3" #the last test3 can be folder or file
    cache: 缓存的文件系统，由generate_fscache得到
    onerror: 默认为"raise"，表示没找到文件时抛出异常；改为"skip"其他值表示没找到文件时返回False
    
    return ('file','455003487756') or ('folder','455000086301'), specially when path == '/', it returns ('folder','0')
    """
    global a
    if cache is not None:
        if filepath == '':
            return 'folder', cache["fid"]
        if filepath.startswith(cache["path"]):
            filepath = filepath.replace(cache["path"],"",1)
        assert not filepath.startswith("/"), "cache not matched: filepath='%s', while cache['path']='%s'"%(filepath,cache['path'])
        if filepath in cache["fs"]:
            return cache["fs"][filepath][0:2]
        else: #缓存中不存在
            if onerror=="raise":
                raise FileNotFoundError(filepath+" not in cache")
            elif onerror=="returnFalse":
                return False
            else:
                # 缓存没有命中就继续吧
                pass
    type, fid = 'folder', '0'
    for name in filepath.split("/"):
        if name=="":
            continue
        try:
            type,fid = lsdir(a, fid, onlyneed=name).split("_")
        except FileNotFoundError:
            if onerror=="returnFalse":
                return False #lsdir都没发现 还是raise吧，除非特意指定returnFalse
            else:
                raise
    return type, fid
    
def generate_fscache(path, fid=None, onlydirs=False, prefix = None, only1depth = False, cache=None):
    """
    输入路径或folder id，返回文件系统
    path: 必须以"/"开头，递归时如果fid给出了就可以为""
    fid: 如"0"
    onlydirs: 如果为True，则返回文件夹的部分
    prefix: 必须以"/"结束，用于递归过程，如果给定了则只返回fs的部分 方便用于cache["fs"].update
    only1depth: 如果为True， 则仅仅返回一层,不递归进入下层
    cache: 本函数是用来生成缓存的，为啥还要输入缓存呢。。。为了让path_to_typed_id加速执行呗
    
    path: "/"
    return: 
    {
        "fs": { #扁平化的文件系统
            "a": ("file", "文件id", 文件字节数),
            "b": ("folder", "目录id", 目录字节数),
            "b/c": ("file", ...), #注意没有开头的/
            ...
        }, 
        "path": 输入的路径,
        "fid": 输入路径对应的id，特别地 根目录为"0"
    }
    """
    global a
    if prefix is None:
        prefix = ""
    if fid is None:
        typetmp, fid = path_to_typed_id(path, cache=cache, onerror='when_cache_fails_continue_search_by_using_lsdir')
        assert typetmp == "folder", "lsdir only accept folder"
    fs = {}
    fs[prefix if len(prefix) else "/"]=True
    for item in lsdir(a, fid, onlydirs=onlydirs):
        type, fileid = item[1].split("_")
        if type=="folder":
            fs[prefix+item[0]] = ("folder", fileid, item[2])
            if not only1depth:
                fs.update(generate_fscache("", fileid, onlydirs = onlydirs, prefix = prefix+item[0]+"/"))
        elif type=="file":
            fs[prefix+item[0]] = ("file", fileid, item[2])
    if prefix != "": #用于递归的返回，只返回文件系统部分
        return fs
    else:
        if not path.endswith("/"):
            path += '/'
        result = {
            "fs": fs,
            "path": path,
            "fid": fid
        }
        return result #被其他函数调用则返回这个包含path和fid的数据结构

def mkdir_and_update_cache(token, name, parent_relative_path, cache, onerror='raise'):
    """
    通过缓存层来创建目录，以减少缓存的强制更新，并且能阻止重复的创建
    token: request_token
    name: 需要创建的文件夹名称
    parent_relative_path: 相对于cache["path"]的相对目录, 这个文件夹应该存在，否则返回False
    cache: 缓存的文件系统，由generate_fscache生成
    onerror: 如果待创建的文件夹已经存在，'raise'表示抛出FileExistsError异常, 其他表示读取/更新缓存后返回已存在的fileid
    
    返回生成的文件夹的fileid，当onerror='skip'时可能返回False
    """
    abspath=(cache["path"]+parent_relative_path+"/"+name).replace("//","/")
    key = parent_relative_path+"/"+name
    if key in cache['fs']:
        if onerror=='raise':
            raise FileExistsError("{abspath} already exists".format(**locals()))
        else:
            return cache['fs'][key][1]
    parent_folder = path_to_typed_id(parent_relative_path,cache, onerror='skip')
    if parent_folder == False:
        print("[Error] parent_folder {parent_folder} does not exist".format(**locals()))
        return False
    parent_id = parent_folder[1]
    size = 0
    try:
        fileid = mkdir(token, name, parent_id)
    except FileExistsError:
        if onerror=='raise':
            raise
        else:
            _, fileid, size = lsdir(a, parent_id, onlyneed=name,onlyneed_return_size=True)
    cache["fs"][key] = ("folder", fileid, size)
    return fileid

def mkdir_p(token, path, cache):
    """
    给出相对路径（绝对路径也支持），以mkdir -p的方式同时创建父文件夹
    """
    if path.startswith(cache["path"]):
        path = path.replace(cache["path"],"",1)
    assert not path.startswith("/"), "cache not matched! path={path}".format(**locals())
    fid = cache["fid"]
    type = "folder"
    key = ""
    for name in path.split("/"):
        key += "/{name}".format(**locals())
        if key[1:] in cache["fs"]:
            type, fid, _ = cache["fs"][key[1:]]
            assert type=="folder", "there is a file {cache_path}{key} in the way".format(cache_path=cache["path"], key=key[1:])
        else:
            try:
                fid = mkdir(token, key.split("/")[-1], fid)
                cache["fs"][key[1:]] = ("folder", fid, 0)
            except FileExistsError:
                type, fid, size = lsdir(a, fid, onlyneed=name, onlyneed_return_size=True)
                cache["fs"][key[1:]] = (type, fid, size)
                assert type=="folder", "there is a file {cache_path}{key} in the way".format(cache_path=cache["path"], key=key[1:])
    return fid


def fillup_cache(abs_path, cache=None):
    """
    输入绝对目录路径(需要已经存在)，返回按路径沿路更新后的cache
    abs_path: "/a/b" 最后的/会被忽略
    将通过lsdir更新根目录、a、b文件夹的缓存
    
    为简化问题复杂度，目前只支持cache为根目录的情况
    由于mkdir_p本身就会沿着路径得到fid，真正需要关注的不是父目录缓存而是已经存在的目录的缓存，所以这个函数目前没有用处
    为了支持这个函数给generate_fscache加上了only1depth参数
    """
    if abs_path.endswith("/"):
        abs_path = abs_path[:-1]
    if cache is None:
        cache = {"fs":{}, "path":"/", "fid":"0"}
    assert cache["path"] == "/", "cache invalid, cache path must be /"
    assert abs_path.startswith("/"), "build_cache need absolute path"
    abs_path = abs_path[1:]
    
    root_cache = generate_fscache("/", only1depth = True)
    cache["fs"].update(root_cache["fs"])
    path_splited = abs_path.split("/")
    for i in range(len(path_splited)):
        nowpath = "/".join(path_splited[:i+1])
        cache["fs"].update(generate_fscache("/"+nowpath, prefix=nowpath+"/", only1depth = True, cache=cache))
    return cache

def upload_directory_targetid(token, local_dir, target_folder_id, skip_existed=False, show_skip_info=True, fencrypt=None):
    """
    token: request_token
    local_dir: 需要上传的文件夹, 如r"d:\to_be_uploaded"
    target_folder_path: 上传的目标位置的父文件夹id
    
    这个函数不是递归函数，使用os.walk mkdir_p upload完成上传任务
    如果目标文件夹已经存在，会print一行[WARN]; 如果目标文件已经存在，会以在文件末尾添加(1)的形式上传 而不是替换！
    """
    #检查本地目录要是一个目录
    global a
    assert os.path.isdir(local_dir), "expected a folder, local_dir={local_dir}".format(**locals())
    name = getfilename(local_dir) #要上传的文件夹名称
    
    fid = str(target_folder_id)
    target_folder_lsdir = lsdir(a, fid)
    # 对父目录进行了列目录，现在直接mkdir_p生成文件夹吧, sh*t cache! 
    try:
        targetfid = mkdir(token, name, parent_id = fid)
    except FileExistsError:
        targetfid = [i[1].split("_")[1] for i in target_folder_lsdir if i[0]==name and i[1].split("_")[0]=="folder"][0]
    print(targetfid)
    
    cache = {"fs":{}, "path":"/", "fid": targetfid}
    cache["fs"].update(generate_fscache("", fid = targetfid, prefix="/", cache=cache))
    #print(cache["fs"])
    target_folder_path = ""
    for root, dirs, files in os.walk(local_dir):
        for dir in dirs:
            dirname = root.replace(local_dir,"",1).replace("\\",'/')+"/"+dir #"/Image/aha"
            mkdir_p(token, target_folder_path+dirname, cache)
        for filename in files:
            relative_root = root.replace(local_dir,"",1).replace("\\",'/') #"/Image/aha"或者""
            remote_abs_folder = target_folder_path+relative_root #"uploaded/Image/aha"或者"uploaded" 注意虽然叫做abs实际上还是相对于cache["path"]的相对目录
            remote_abs_filepath = remote_abs_folder+"/"+safefilename(filename) #"uploaded/Image/aha/example.jpg"或者"uploaded/example.jpg"
            #print(remote_abs_folder, cache)
            type, folder_id = path_to_typed_id(remote_abs_folder, cache)
            assert type=="folder", "expected folder {remote_abs_folder}".format(**locals())
            local_filepath = os.path.join(local_dir, relative_root[1:], filename)
            if skip_existed and remote_abs_filepath in cache["fs"]:
                if show_skip_info:
                    print("skip existed file: {remote_abs_filepath}".format(**locals()))
                continue
            filesize = getsize(local_filepath)
            if filesize>BLOCKSIZE:
                data=block(open(local_filepath,"rb"), showhint=False)
            else:
                data=open(local_filepath,"rb").read()
            newfileid = upload(token,filename,data,filesize,folder_id=folder_id,fencrypt=fencrypt)
            cache["fs"][remote_abs_filepath] = ("file", newfileid, filesize)
    return targetfid
    
def upload_directory(token, local_dir, target_folder_path, cache=None, skip_existed=False, show_skip_info=True, fencrypt=None):
    """
    token: request_token
    local_dir: 需要上传的文件夹, 如r"d:\to_be_uploaded"
    target_folder_path: 上传的目标位置(相对路径,也支持绝对路径)，不能以/结尾，如"/uploaded"，注意应该加上本地的文件夹名称，否则将文件夹内容合并到已存在的文件夹下
    
    这个函数不是递归函数，使用os.walk mkdir_p upload完成上传任务
    如果目标文件夹已经存在，会print一行[WARN]; 如果目标文件已经存在，会以在文件末尾添加(1)的形式上传 而不是替换！
    """
    
    #缓存如果没有给出，使用默认缓存
    if cache is None:
        try:
            cache = fillup_cache(target_folder_path)
        except FileNotFoundError:
            cache = {"fs":{}, "path":"/", "fid":"0"}
    
    #检查target_folder_path的合理性：与cache匹配，末尾不是/
    if target_folder_path.startswith(cache["path"]):
        target_folder_path = target_folder_path.replace(cache["path"],"",1)
    assert not target_folder_path.startswith("/"), "cache not matched! path={target_folder_path}".format(**locals())
    assert not target_folder_path.endswith("/"), "target_folder_path should not end with /"
    
    #检查本地目录要是一个目录
    assert os.path.isdir(local_dir), "expected a folder, local_dir={local_dir}".format(**locals())
    
    fid = mkdir_p(token, target_folder_path, cache)
    cache["fs"].update(generate_fscache("", fid = fid, prefix=target_folder_path+"/", cache=cache))
    if target_folder_path in cache["fs"] and cache["fs"][target_folder_path][2]>0:
        print("[WARN] folder {target_folder_path} alreay exsits".format(**locals()))
    for root, dirs, files in os.walk(local_dir):
        for dir in dirs:
            dirname = root.replace(local_dir,"",1).replace("\\",'/')+"/"+dir #"/Image/aha"
            mkdir_p(token, target_folder_path+dirname, cache)
        for filename in files:
            relative_root = root.replace(local_dir,"",1).replace("\\",'/') #"/Image/aha"或者""
            remote_abs_folder = target_folder_path+relative_root #"uploaded/Image/aha"或者"uploaded" 注意虽然叫做abs实际上还是相对于cache["path"]的相对目录
            if fencrypt.get("fencrypt_filename", None) is not None:
                remote_abs_filepath = remote_abs_folder+"/"+fencrypt["fencrypt_filename"](safefilename(filename)) # filename encrypted
            else:
                remote_abs_filepath = remote_abs_folder+"/"+safefilename(filename) #"uploaded/Image/aha/example.jpg"或者"uploaded/example.jpg"
            type, folder_id = path_to_typed_id(remote_abs_folder, cache)
            assert type=="folder", "expected folder {remote_abs_folder}".format(**locals())
            local_filepath = os.path.join(local_dir, relative_root[1:], filename)
            if skip_existed and remote_abs_filepath in cache["fs"]:
                if show_skip_info:
                    print("skip existed file: {remote_abs_filepath}".format(**locals()))
                continue
            filesize = getsize(local_filepath)
            if filesize>BLOCKSIZE:
                data=block(open(local_filepath,"rb"), showhint=False)
            else:
                data=open(local_filepath,"rb").read()
            newfileid = upload(token,filename,data,filesize,folder_id=folder_id, fencrypt=fencrypt)
            cache["fs"][remote_abs_filepath] = ("file", newfileid, filesize)
    return fid


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
    filename=getfilename(path_to_file) #注意不能quote
    return upload_by_collection_detailed(token, upload_link, filename, getsize(path_to_file), block(open(path_to_file,"rb")))
    
def upload_by_collection_detailed(token, collection_code, filename, filesize, data):
    """
    详细的真实匿名上传过程 通过文件收集任务上传
    需要先从上传页面中得到token
    collection_code即为配置文件中的upload_link
    上传过程类似upload. 但多了一步collection_submit的操作
    返回上传文件得到的服务器端的文件id
    
    如果失败，抛出Exception
    """
    global a
    x = a.post(DOMAIN + "/apps/processes/presign_upload",
            ("""{"code":"%s","file_name":"%s","file_size":%d}"""%(collection_code, filename, filesize)).encode('utf-8'), #在格式化字符串之后再进行编码
            headers={"requesttoken":token,"X-Requested-With": "XMLHttpRequest", "Content-Type":"text/plain;charset=UTF-8"}
        )
    result=x.json()
    if "success" not in result or result["success"]!=True:
        print("[FAILED] presign_upload")
        print(result)
        raise Exception("presign_upload failed")
    upload_url=result["upload_url"]
    x=a.post(upload_url,
             data,
             headers={"requesttoken": token,"X-File-Name": quote(filename), "Content-Type":"text/plain;charset=UTF-8"},dont_change_cookie=True) #header中的还是需要quote的
    result=x.json()
    if "success" not in result or result["success"]!=True:
        print("[FAILED] upload")
        print(result)
        raise Exception("upload failed")
    fileid = result["new_file"]["id"]
    x = a.post(DOMAIN+"/apps/processes/collection_submit", 
        """{"user_name":".","code":"%s","file_ids":[%s]}"""%(collection_code,fileid),
        headers={"requesttoken":token, "X-Requested-With": "XMLHttpRequest", "Content-Type":"text/plain;charset=UTF-8"},
        dont_change_cookie=True
        )
    result=x.json()
    if "success" not in result or result["success"]!=True:
        print("[FAILED] collection_submit")
        print(result)
        raise Exception("collection_submit failed")
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
    print("\nDownload Markdown:")
    apitype = "zjuvideo" if path_to_file.endswith(".mp4") else "panzju"
    print("[{filename}]({APIDOMAIN}/{apitype}/{sharelink}/{fileid})".format(filename=getfilename(path_to_file), APIDOMAIN=APIDOMAIN, apitype=apitype, sharelink=config_sharelink, fileid=fileid))
    print("\nTemporary download link:")
    print(dirshare_download(config_sharelink, fileid))


def logined_upload(token, path_to_file, fencrypt=None):
    """
    已经登录，执行上传流程
    """
    block_generator=block(open(path_to_file,"rb"))
    filesize=getsize(path_to_file)
    fileid=upload(token,path_to_file,block_generator,filesize, fencrypt=fencrypt)
    sharelink=share(token,fileid)
    return fileid, sharelink

def copy_from_share(token, sharelink, targetid, _a=None):
    """
    已经登录，从分享复制到指定目录
    """
    if _a is None:
        global a
    else:
        a = _a
    x = a.get(DOMAIN+"/share/"+sharelink, o=True, result=False)
    if "Location" in x.headers:
        """
        发生跳转，自己发布的分享链接或者没有登录
        """
        if "login" in x.headers["Location"]:
            raise NotLoginException()
        else:
            fileid = x.headers["Location"].split("file/")[1]
    else:
        """
        没有跳转，是别人的链接
        """
        page = x.text
        tmp = finder.search(page)
        assert tmp is not None, "share link does not exist"
        fileid = tmp.group(1)
    postdata = """{"target_folder_id":%s,"item_typed_ids":"file_%s","scenario":"share"}"""%(str(targetid), fileid)
    x = a.post(DOMAIN+"/apps/files/copy?scenario=share", postdata, headers={"Content-Type":"text/plain;charset=UTF-8","requesttoken":token})
    try:
        data = x.json()
        print(data["files_and_folders"][0]["name"])
    except:
        print(x.text)
    return data["success"]

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
        a.save(_statusfile)
        token=islogin()
    fencrypt = getattr(config, "fencrypt", {})
    fileid, sharelink = logined_upload(token, sys.argv[1], fencrypt=fencrypt)
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