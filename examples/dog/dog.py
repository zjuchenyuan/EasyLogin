from EasyLogin import EasyLogin
a=EasyLogin(proxy="socks5://127.0.0.1:1080")
a.get("http://www.akc.org/news/the-most-popular-dog-breeds-in-america/",cache="dog.html")
data=a.find("table","""border="0" cellpadding="0" cellspacing="0" style="width:100%" """,text=True)[0]
for i in data:
    try:
        int(i)
        print("\t"+i,end="")
    except:
        print("\n"+i,end="")
print()