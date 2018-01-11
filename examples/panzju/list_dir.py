# encoding: utf-8
from panzju import generate_fscache, login, APIDOMAIN, getshareid
from config import username,password #与upload_dir类似，也需要你的用户名密码进行登录
import sys
## 用于列出分享目录下的文件，显示出直接可以点击下载的Markdown
## FIXME: 目前仅支持目录\文件这种形式的正确层级显示

#首先调用login登录和generate_fscache生成文件系统缓存
assert login(username, password) is not False, "Login failed"
folder_id = sys.argv[1]
share_id = getshareid(folder_id)
assert share_id is not False, "share link does not exist, create it first!"
c = generate_fscache("",folder_id)

# import pickle
# open("test.pickle","wb").write(pickle.dumps(c))
# c = pickle.load(open("test.pickle","rb")) #已经导出了缓存就直接加载吧
keys = [i for i in sorted(c["fs"].keys()) if not i.endswith("/")]
result = []
for key in keys:
    if key.count("/")==0:
        result.append("\n----")
        result.append("### "+key)
    else:
        if key.endswith(".mp4"):
            apiname = "zjuvideo"
        else:
            apiname = "panzju"
        result.append("[{filename}]({APIDOMAIN}/{apiname}/{share_id}/{fileid})".format(filename=key.split("/")[-1], APIDOMAIN=APIDOMAIN, apiname=apiname, share_id=share_id,fileid=c["fs"][key][1]))
print("\n".join(result))