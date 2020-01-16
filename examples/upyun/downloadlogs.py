from config import mydomains
from openapi import query, a
import datetime, calendar

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def now():
    return datetime.datetime.now()


def getpast30date():
    return (now()-datetime.timedelta(days=30)).strftime("%Y-%m-%d")

def getcurrentdate():
    return (now()).strftime("%Y-%m-%d")

def getdaterange():
    date1 = getpast30date()
    date1_year = int(date1.split("-")[0])
    date1_month = int(date1.split("-")[1])
    lastday = calendar.monthrange(date1_year, date1_month)[1]
    date2 = getcurrentdate()
    date2_year = int(date2.split("-")[0])
    date2_month = int(date2.split("-")[1])
    if date1_month == date2_month:
        return [(date1, date2),]
    else:
        return [(date1, "%d-%02d-%02d"%(date1_year,date1_month, lastday)), ("%d-%02d-%02d"%(date2_year,date2_month, 1), date2)]

def getloglist_range(domain, start, end):
    #[{"file", "size", "url"}]
    return query("analysis/archives?domain={domain}&start_date={start}&end_date={end}&useSsl=true".format(**locals()))["data"]

def saveurl(url):
    urls = url.split("/")
    date, domain, filename = urls[3], urls[5].replace("*","_"), urls[-1].replace("*","_")
    savepath = "/".join(["logs", domain, date, filename])
    folder = "/".join(["logs", domain, date])
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    if os.path.exists(savepath):
        return
    x = a.get(url, result=False, o=True)
    print(savepath, x)
    open(savepath, "wb").write(x.content)
    

if __name__ == "__main__":
    from pprint import pprint
    for domain in mydomains:
        for range in getdaterange():
            for item in (getloglist_range(domain, *range)):
                saveurl(item["url"])