from EasyLogin import EasyLogin, quote
from config import auth, school, UA, REFERER
a=EasyLogin(cachedir="cache")
a.s.headers["Authorization"] = auth
a.s.headers["referer"]="https://servicewechat.com/wxa2fcebe559478c18/6/page-frame.html"

def get(url):
    global a
    x = a.get("https://kefou.topless.tech"+url, result=False, o=True, cache=True, headers={"Referer":REFERER, "User-Agent":UA})
    res = x.json()
    #print(res)
    return res

def new_comments(schoolid=school):
    return get("/comments/new?school="+schoolid)["data"]["comments"]

def search_teacher(name, schoolid=school):
    name = quote(name)
    return get("/teachers/?q={name}&limit_type=school&limit_id={schoolid}&per_page=1000&page=1".format(**locals()))["data"]['teachers']

def search_courses(name, schoolid=school):
    name = quote(name)
    return get("/courses/?q={name}&limit_type=school&limit_id={schoolid}&per_page=1000&page=1".format(**locals()))["data"]["courses"]

def list_faculties(schoolid=school):
    return get("/faculties/?q=&limit_type=school&limit_id={schoolid}&per_page=1000&page=1".format(**locals()))["data"]['faculties']

def list_faculty_teachers(facultyid):
    return get("/teachers/?q=&limit_type=faculty&limit_id={facultyid}&per_page=1000&page=1".format(**locals()))["data"]['teachers']

def teacher_comments(teacherid):
    x = get("/teacher/{teacherid}/comments?page=1&per_page=10000&sort_by=hot".format(**locals()))
    #print(x)
    return x["data"]["comments"]

def tprint(*args):
    print("\t".join([str(i) for i in args]))

if __name__ == "__main__":
    from pprint import pprint
    #x = new_comments(school)
    #x = search_teacher("白", school)
    #x = search_courses("白", school)
    #x = list_faculties(school)
    #x = list_faculty_teachers("5dd6422301a48535f3ff6f0e")
    #pprint(x)
    #exit()
    from config import consumer
    for f in list_faculties():
        #print(f)
        for t in list_faculty_teachers(f["_id"]):
            res = []
            for c in teacher_comments(t["_id"]):
                assert c["teacher"] == t["_id"]
                c["teacher"] = t
                if not res:
                    print(t["name"], c["content"], "", sep="\n")
                #print(c)
                res.append(c)
            #tprint(f["name"], t["name"], t["gpaScore"], t["rateScore"], t["rateNum"])
            #break
            consumer(res)
