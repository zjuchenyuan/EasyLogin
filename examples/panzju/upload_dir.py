from panzju import islogin, login, upload_directory, getfilename, share, DOMAIN
from testconfig import username, password #fix this filename
import pickle
import sys

"""
Usage: python3 upload_dir.py src dst
src表示源文件夹路径，末尾的/会自动去除
dst表示上传的目标路径
如果目标文件夹路径(dst)以/结束，表示按源文件夹名称再创建一个子文件夹

Example:
python3 upload_dir.py D:\Desktop\ebook /学习资料/电子书
    这样所有ebook文件夹下的内容将被上传到 电子书 文件夹下
python3 upload_dir.py /var/www/html/mywebsite /网站备份/
    这样会创建并上传至/网站备份/mywebsite，方便少打一次mywebsite

目前的Bug:
在用户文件夹数量太多时，创建整个远程文件夹树非常耗时且无必要，应该调整缓存策略
"""

def UIuploaddir():
    token = islogin()
    if not token:
        login(username, password)
        token = islogin()
    assert token!=False, "login failed"
    try:
        cache = pickle.loads(open("cachefs.status","rb").read())
    except:
        cache = generate_fscache("/")
        open("cachefs.status","wb").write(pickle.dumps(cache))
    
    src = sys.argv[1].rstrip("/")
    dst = sys.argv[2]
    if dst.endswith("/"):
        dst += getfilename(sys.argv[1])
    fid=upload_directory(token, src, dst, cache, skip_existed=True, show_skip_info=False)
    sharelink=share(token,"folder_"+fid)
    print(DOMAIN+"/share/"+sharelink)
    open("cachefs.status","wb").write(pickle.dumps(cache))

if __name__ == '__main__':
    UIuploaddir()