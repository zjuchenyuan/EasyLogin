#coding:utf-8
"""
使用fangcloud.py提供的download函数提供网页服务
Example:
https://api.chenyuan.me/fangcloud/448eb45f0d08cbf37c33f35419
"""

from cyserver import CYServer
from fangcloud import download

def do_GET(self):
    path = self.path.split("/")
    if path[1]=="fangcloud":
        try:
            url = download(path[2])
            return self._302(url)
        except Exception as e:
            return self._fail(e)
    else:
        return self._hello()


if __name__=="__main__":
    CYServer(8080,do_GET).run()