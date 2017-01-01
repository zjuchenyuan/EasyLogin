from EasyLogin import EasyLogin
from mpms import MultiProcessesMultiThreads
import requests

def createsession():
    global session
    session=requests.Session()
    session.headers.update({"Connection":"keep-alive",'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36" })
    return session

session=createsession()
    
def worker(id):
    global session
    if id%500==0:
        session=createsession()
        print("requesting",id)
    a=EasyLogin(session=session)
    a.get("http://cn.epubee.com/files.aspx?action=add&bookid={}".format(id),r=True,cookiestring="identify=99{};user_localid=ip_8.8.8.8;uemail=;isVip=1;leftshow=0".format(id))
    result = a.getlist("getFile.ashx")
    return [result,len(result),id]

def handler(meta,result,len_result,id):
    if id%1000==0:
        meta["f1"].flush()
        meta["f2"].flush()
    if(len_result==0):
        return
    for i in result:
        #print(i)
        meta["f1"].write(i+"\n")
        meta["f2"].write("{}\t{}\n".format(id,i))

def main():
    f1 = open("downloadlink.txt","a")
    f2 = open("record.txt","a")
    m = MultiProcessesMultiThreads(
        worker,
        handler,
        processes=2,
        threads_per_process=5,
        meta={"f1":f1,"f2":f2},
    )
    for i in range(38501,2000000):
        m.put(i)
    m.join()
    f1.close()
    f2.close()

if __name__ == '__main__':
    main()
    #print(worker(9998))