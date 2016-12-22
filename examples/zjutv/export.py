#coding:utf-8

"""
在使用浙大云盘API上传文件后，产生了upload.txt，文件格式：id.mp4 \t share_link
本程序将share_link写入数据库，并导出可以发帖的形式
"""

import pymysql
import sys
sys.stdout=open(1, 'w', encoding='utf-8', closefd=False) #在win下此行挺重要的

def db():
    global conn
    conn = pymysql.connect(user='root',passwd='123456',host='127.0.0.1',port=3306,db='zjutv',charset='utf8',init_command="set NAMES utf8")
    conn.encoding = "utf8"
    return conn

def runsql(sql):
    global conn
    conn=db()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return cur.fetchall()

def update_share():
    for line in open("upload.txt"):
        line=line.replace("\n","").split("\t")
        id = line[0].split(".mp4")[0]
        share = line[1]
        runsql("update `data` set share='{}' where id={}".format(share,id))

def export():
    for i in (runsql("select * from `data` where length(share)>0")):
        print(i[1])#i[1] 视频标题；i[0] id；i[2] 详细描述；i[3] 原始下载链接
        print("http://api.chenyuan.me/video/"+i[4])#i[4] share_link
        print()

if __name__=="__main__":
    update_share()
    export()