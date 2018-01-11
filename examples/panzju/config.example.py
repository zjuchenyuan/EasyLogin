anonymous = False
# 如果匿名上传为True 则使用此处的上传链接和分享链接
uploadlink = "086fefe52532650b40341..........."
sharelink = "28c25672a486641f0........."

# 非匿名上传则使用此用户名密码登录
username = ".........."
password = ".........."
assert username!="..........", "please modify config.py"

# 如果需要加密则引入以下几行
ENCRYPTION_PASSWORD = "b@dPassw0rd_CHANGEME!" # 文件加密用的密码
ENCRYPTION_METHOD = "aes-256-cfb" # 使用的加密方式
ENCRYPTION_IVLEN = 16 #这种加密方式导致的密文文件长度增加的字节数 就是IV的长度

from encryption_example import fencrypt # 引入加密函数，这一行必须放在最后
## 如果你不需要加密，删掉上一行即可

# 使用绝对目录存储登录状态文件 方便在任意目录调用共享登录状态
from os import name as osname
if osname=="nt":
    statusfile = "d:\\panzju.status" 
else:
    statusfile = "/tmp/panzju.status"
