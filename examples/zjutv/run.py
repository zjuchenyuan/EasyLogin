from EasyLogin import EasyLogin
import pymysql

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

def createsql(id,name,description,mp4):
    return "insert ignore into `data` (id,name,description,mp4) values({},'{}','{}','{}');".format(id,name,description,mp4)

a = EasyLogin()

def get(id):
    a.get("https://www.zdgd.zju.edu.cn/index.php?s=/home/player/index/id/{}.html".format(id))
    name=a.b.find("div",{"class":"col-md-4 col-sm-4"}).text.strip()
    description=a.b.find("div",{"class":"col-md-3"}).text.strip().replace("\t","").replace("  ","").replace("\r","").replace("\n\n","\n").replace("\n\n","\n")
    try:
        mp4=a.b.find("source",{})["src"]
    except TypeError:
        mp4=""
    return [id,name,description,mp4]

for i in range(1,751):
    try:
        runsql(createsql(*get(i)))
    except AttributeError:
        pass