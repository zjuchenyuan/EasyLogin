from panzju import islogin, login, upload_directory, getfilename, share, DOMAIN
from testconfig import username, password #fix this filename
import pickle
import sys

USEAGE="""
Usage: python3 upload_dir.py src dst
src表示源文件夹路径，末尾的/会自动去除
dst表示上传的目标路径
如果目标文件夹路径(dst)以/结束，表示按源文件夹名称再创建一个子文件夹

指定目标文件夹如果已经存在 会跳过已经存在的同名文件

Example:
python3 upload_dir.py D:\Desktop\ebook /学习资料/电子书
    这样所有ebook文件夹下的内容将被上传到 电子书 文件夹下
python3 upload_dir.py /var/www/html/mywebsite /网站备份/
    这样会创建并上传至/网站备份/mywebsite，方便少打一次mywebsite
"""

def UIuploaddir():
    token = islogin()
    if not token:
        login(username, password)
        token = islogin()
    assert token!=False, "login failed"
    src = sys.argv[1].rstrip("/")
    dst = sys.argv[2]
    if dst.endswith("/"):
        dst += getfilename(sys.argv[1])
    fid=upload_directory(token, src, dst, skip_existed=True, show_skip_info=True)
    sharelink=share(token,"folder_"+fid)
    print(DOMAIN+"/share/"+sharelink)

if __name__ == '__main__':
    if len(sys.argv)<3:
        print(USEAGE)
    else:
        UIuploaddir()