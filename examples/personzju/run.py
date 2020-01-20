from EasyLogin import EasyLogin, mymd5
from mpms import MPMS
import threading
thread_data = threading.local()

import time
myprint = lambda s: print("[{showtime}] {s}".format(showtime=time.strftime("%Y-%m-%d %H:%M:%S"), s=s))

import time
a=EasyLogin(cachedir="cache")
def sign(timestamp, url, params):
    t = "1f11192bd9d14a09b29fc59d556e24e3"
    o = [i[0]+str(i[1]) for i in sorted(params.items())]
    s = t+url+"".join(o)+str(timestamp)+" "+t
    return mymd5(s)

def get(url, params, **kwargs):
    global a
    t = int(time.time())*1000
    a.s.headers.update({"appKey":"50634610756a4c0e82d5a13bb692e257", "timestamp":str(t), "sign": sign(t, url, params)})
    x = a.get("https://person.zju.edu.cn/server"+url+"?"+"&".join(k+"="+str(v) for (k,v) in sorted(params.items())), o=True, result=False, **kwargs)
    return x.json()

def tprint(*args):
    print("\t".join([str(i) for i in args]))

def worker(item):
    global thread_data
    a = thread_data.__dict__.get("a")
    if not a:
        a = EasyLogin(cachedir="cache")
        thread_data.__dict__["a"] = a
    html = a.get("https://person.zju.edu.cn/"+item[3], result=False)
    uid = html.split("getQRcode.php?uid=",2)[1].split("&",2)[0]
    item.append(uid)
    return item

def handler(meta, item):
    meta["fp"].write("\t".join([str(i) for i in item])+"\n")

if __name__ == "__main__":
    #print(sign(1579490640000, "/api/front/psons/search", {"size": 12, "page":0, "lang": "cn"}))
    
    meta = {"fp": open("result_uid.txt","w",encoding="utf-8")}
    m = MPMS(worker, handler, 2, 2, meta=meta)
    m.start()
    for t in get("/api/front/psons/search", {"size":10000, "page":0, "lang":"cn"}, cache=True)["data"]["content"]:
       #tprint(t["cn_name"], t["college_name"], t["work_title"], t["mapping_name"], t["access_count"])
       m.put([t["cn_name"], t["college_name"], t["work_title"], t["mapping_name"], t["access_count"]])
       
    while len(m)>10:
        myprint("Remaning "+str(len(m)))
        time.sleep(2)
    m.join()
    myprint("Done!")