from EasyLogin import EasyLogin
from collections import OrderedDict
from pprint import pprint

a=EasyLogin()

def getiso(id,justlink=False):
    while 1:
        try:
            a.get("http://10.15.61.7:8080/poweb/showpage.do?status=show&METAID={}".format(id),failstring="错误提示",cache=True)
            break
        except:
            print("Oops...Retry...")
    if justlink:
        return [i.split("isoid=")[1] for i in a.getlist("downloadisofile")]
    title = a.b.find("input",{"id":"thetitle"})["value"]
    result=OrderedDict()
    t=0
    for tr in a.b.find_all("tr"):
        gp = tr.find("span",text="光盘：")
        if gp is None:
            continue
        isoid=gp.find_next("a",{"class":"link_f"})["href"].split("=")[1]
        if isoid in result:
            continue
        t+=1
        name="{}_{}_{}".format(title,t,gp.next_sibling.strip())
        result[isoid]=a.safefilename(name)+".iso"
    return result

def curl(url, name):
    command = 'curl "{url}" -o "{name}" -C -'.format(url=url,name=name)
    return command

def gethot(page=1):
    result=[]
    url = "http://10.15.61.7:8080/poweb/hitcount.do?status=morehitcount&PageCount={}".format(page)
    a.get(url,cache=True)
    return [i.split("=")[2] for i in a.getlist("showpage")]

def main():
    for page in range(1,6):
        for i in gethot(page=page):
            data = getiso(i)
            for j in data:
                print(curl("http://10.15.61.7:8080/poweb/downloadisofile?isoid="+j,data[j]))

if __name__ == "__main__":
    main()