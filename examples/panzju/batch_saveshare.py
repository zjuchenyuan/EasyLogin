from config import username, password
from panzju import islogin, login, copy_from_share

def UI_batch_save():
    token = islogin()
    if not token:
        login(username, password)
        token = islogin()
    targetid = input("目标文件夹ID: ")
    print("请复制包含分享链接的文本，按Ctrl+C退出：")
    while True:
        line = input()
        if "pan.zju.edu.cn/share/" in line:
            sharelink = line.split("pan.zju.edu.cn/share/")[1].split()[0]
            copy_from_share(token, sharelink, targetid)

if __name__ == "__main__":
    UI_batch_save()