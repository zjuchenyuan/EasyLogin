from EasyLogin import EasyLogin
from urllib.parse import unquote
import os
import base64

URL=base64.b64decode("aHR0cDovL3d3dy5jZW5zdXNpbmRpYS5nb3YuaW4vQ2Vuc3VzX0RhdGFfMjAwMS9DZW5zdXNfRGF0YV9PbmxpbmUvQXJlYV9Qcm9maWxlL0Rpc3RyaWN0X1Byb2ZpbGUuYXNweA==").decode()

a = EasyLogin()
a.get(URL,cache=True)
VIEWSTATE = a.VIEWSTATE()
EVENTVALIDATION = a.b.find("input", {"name": "__EVENTVALIDATION"})["value"]
state = {int(i["value"]): i.text for i in a.b.find("select", {"name": "ctl00$Body_Content$drpState"}).find_all("option")
         if i["value"] != ""}


def getDistrict(stateID):
    global a, VIEWSTATE, EVENTVALIDATION
    x = a.post_dict(
        URL, {
            "__EVENTTARGET": "ctl00$Body_Content$drpState",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": unquote(VIEWSTATE),
            "__VIEWSTATEGENERATOR": "2C266559",
            "__EVENTVALIDATION": EVENTVALIDATION,
            "ctl00$Body_Content$drpState": "%02d" % stateID,
            "ctl00$Body_Content$drpDistrict": ""
        }, cache="{stateID}.cache".format(stateID=stateID))
    VIEWSTATE = a.VIEWSTATE()
    EVENTVALIDATION = a.b.find("input", {"name": "__EVENTVALIDATION"})["value"]
    return {int(i["value"]): i.text for i in
            a.b.find("select", {"name": "ctl00$Body_Content$drpDistrict"}).find_all("option") if i["value"] != ""}


def post(stateID, districtID, filename):
    global a, VIEWSTATE, EVENTVALIDATION
    fp = open(filename, "w", encoding="utf-8")
    x = a.post_dict(
        URL, {
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": unquote(VIEWSTATE),
            "__VIEWSTATEGENERATOR": "2C266559",
            "__EVENTVALIDATION": EVENTVALIDATION,
            "ctl00$Body_Content$drpState": "%02d" % stateID,
            "ctl00$Body_Content$drpDistrict": "%02d" % districtID,
            "ctl00$Body_Content$btnSubmit": "Submit"
        }, cache="{stateID}_{districtID}.cache".format(stateID=stateID, districtID=districtID))
    VIEWSTATE = a.VIEWSTATE()
    EVENTVALIDATION = a.b.find("input", {"name": "__EVENTVALIDATION"})["value"]
    t1 = 0
    for tr in a.b.find("table", {"id": "Table2"}).find_all("tr"):
        t1 += 1
        if t1 == 1:
            continue  # skip the first title line
        t2 = 0
        for td in tr.find_all("td"):
            if t2 == 0 or t2 == 2:
                fp.write(td.text)
            elif t2 == 1 or t2 == 3:
                fp.write("\t" + td.text.strip() + "\n")
            t2 += 1
    fp.close()

for i in state:
    stateName=state[i]
    district=getDistrict(i)
    try:
        os.mkdir(a.safefilename(stateName))
    except FileExistsError:
        pass
    for j in district:
        districtName=district[j]
        filename=a.safefilename(stateName)+"\\"+a.safefilename(districtName)+".txt"
        print(filename)
        post(i,j,filename)

