# 又拍云非官方API

本文件提供又拍云网页控制台的部分功能，以弥补现有API的不足

由于需要明文存储账号密码，不建议在生产环境使用

目前功能包含：**规则刷新**， **https证书更新**

## config.py

需要写入网页控制台的登录需要的用户名和密码，请一定保密这个config.py

config.py的格式：

```
USERNAME="你的用户名"
PASSWORD="你的密码"
```

## 规则刷新 用法

写入好config.py后，运行`python3 upyun.py http://py3.io/*`即可刷新py3.io的缓存

支持同时刷新多个域名，只需要在命令行参数给出即可

![](screenshot.jpg)

## https证书更新 用法

```
# 查看所有证书，只显示当前正在使用的自有证书+正在使用的已经过期的证书
python3 upyun.py https list

# 更新所有 30 天之内过期的证书
python3 upyun.py https renew
```

更新证书除了需要在 config.py 中提供登录的USERNAME和PASSWORD之外，还需要提供一个 api_func(domain_name)函数，这个函数需要返回证书信息

```
 {"certificate":"-----BEGIN CERTIFICATE-----\n...", 
  "private_key":"-----BEGIN RSA PRIVATE KEY-----\n..."}
```

我是使用函数计算用 dns 验证自动更新证书： https://py3.io/Nginx/#https_1

这个函数就是这个样子：(注意到传入的域名可能是子域名 需要判断后缀）

```
def renew_api(domain):
    namedict = {
      'py3.io': 'py3io_ATxx', 
    }
    for k, v in namedict.items():
        if domain.endswith(k):
            return get_from_oss(v)
    return False

import requests
sess = requests.session()
def get_from_oss(name):
    crt = sess.get("https://OSSNAME.oss-cn-REGION.aliyuncs.com/{name}.crt".format(name=name), headers={"Referer":"Referer_STRING"})
    key = sess.get("https://OSSNAME.oss-cn-REGION.aliyuncs.com/{name}.key".format(name=name), headers={"Referer":"Referer_STRING"})
    return {"certificate": crt.text, "private_key": key.text}
```

## 日志下载 [downloadlogs.py](downloadlogs.py)

使用upyun提供的api下载config.py中mydomains的30天内的日志

需要在config.py中提供mydomains和ACCESS_TOKEN

ACCESS_TOKEN可以通过调用openapi.py得到:

```
from openapi import createtoken
print(createtoken("downloadlog"))
```
