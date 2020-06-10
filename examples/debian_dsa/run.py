import sys, gzip, csv, re
sys.path.append("../..")
cveinfo = {}
for line in csv.reader(open("cvss.csv")):
    cveinfo[line[0]] = line

from EasyLogin import EL
a=EL(proxy="socks5://127.0.0.1:10808", cachedir="cache")

def getdsa(year, name):
    if not name:
        return
    a.get("https://www.debian.org/security/"+str(year)+"/"+name, cache=True)
    data=[i.text for i in a.b.find_all("dd")]
    from dateutil.parser import parse
    dsadate = parse(data[0])
    cves = re.findall(r'(CVE-\d+-\d+)', data[3])
    #print(cves)
    try:
        cvedates = [parse(cveinfo[i][-1]) for i in cves if i in cveinfo]
        #print(cvedates)
        cvedate = min(cvedates)
    except:
        return
    #print(cvedate)
    distance = (dsadate-cvedate).days
    print(name, distance, sep="\t")
    return distance

def getyearlist(year, cache=True):
    a.get("https://www.debian.org/security/"+str(year)+"/", cache=cache)
    for strong in a.b.find_all("strong"):
        x = strong.find("a")
        if not x:
            continue
        name = x["href"][2:]
        #print(name)
        try:
            getdsa(year, name)
        except:
            continue

if __name__ == "__main__":
    #import sys
    #getyearlist(sys.argv[1])
    for year in range(2010,2021):
        getyearlist(year)
    #getdsa(2020, "dsa-4683")