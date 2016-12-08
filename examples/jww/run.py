# coding:utf-8
from EasyLogin import EasyLogin
import sys
from pprint import pprint
HOST="https://jw.zjuqsc.com"
a = EasyLogin()

def jww_islogin():
    global a
    p = a.get(HOST+'/xsdhqt.aspx?dl=iconjskb',result=False,o=True)
    if p and len(p.headers['Location'])>7: 
        return True
    else:return False
    
def jww_login(username=None,password=None):
    global a
    if username==None: 
        return False
    try:
        a.get(HOST)
        VIEWSTATE = a.VIEWSTATE()
        p = a.post(HOST+"/default2.aspx",data = '__EVENTTARGET=Button1&__EVENTARGUMENT=&__VIEWSTATE={}&TextBox1={}&TextBox2={}&Textbox3=&RadioButtonList1=%BD%CC%CA%A6&Text1='.format(VIEWSTATE,username,password))
        return "location" in p.headers
    except Exception as e:
        print(e)
        return False

def jww_kebiao(xh,password):
    """
    返回课表的数组，数据结构定义为[课程号，课程名称，老师，学期，时间，地点]
    如果密码错误，返回False
    """
    def lookup(x):#本函数用于对课表数组按照时间顺序排序
        week = {"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"日":7}
        try:
        	return week[x[4][1]]*10+int(x[4][3])
        except:
            return 0
            
    global a
    if not jww_islogin():
        if not jww_login(xh,password):
            print("Password Error")
            return False
    result=[]
    data = a.get(HOST+"/xskbcx.aspx?xh="+xh)
    soup=a.b.find("table",attrs={"class":"datagridstyle"})#找到第一个<table class="datagridstyle">
    for i in soup.find_all("tr"):#遍历所有的<tr>标签
        if i.get('class')!=['datagridhead']:#忽略class为datagridhead的（其实就是第一个）,注意这里的get方法，不会因为class不存在而抛出异常
            line = []
            t = 0
            for j in i.contents:#对tr里面的所有元素进行遍历
                if j.name=='td':
                    if(t>5):continue
                    t+=1
                    line.append(j.text)
            result.append(line)
    return sorted(result,key=lookup)


if __name__ == "__main__":
    if len(sys.argv)!=3:
        print("Usage: python3 {} 学号 密码".format(sys.argv[0]))
        exit(1)
    data = jww_kebiao(sys.argv[1],sys.argv[2])
    if not data or len(data)==0: 
        print("人家的课表是空的呢")
        exit(0)
    pprint(data)
    
    if 0:#按HTML格式输出
        print('<table>')
        for line in data:
            print('<tr>')
            for item in line:
                print('<td>')
                try:
                    print(item,end='')
                except:
                    pass
                print('</td>')
            print('</tr>')
        print('</table>')
