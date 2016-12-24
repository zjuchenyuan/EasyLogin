from EasyLogin import EasyLogin
a=EasyLogin(cookiestring=YOUR_COOKIE_HERE)
for page in range(0,162):
    a.get("http://www.nexushd.org/log.php?action=funbox&page={}".format(page))
    for i in a.find("table","""width=940 border=1 cellspacing=0 cellpadding=5""",skip=1):
        print(i)