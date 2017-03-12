from EasyLogin import EasyLogin
a=EasyLogin()
# make a GET request, and use cache to speed up
a.get("http://www.shanghairanking.com/ARWU2016.html",cache=True)
# this is the table we need
table=a.b.find("table",{"id":"UniversityRanking"})
count=0
# delete first <tr>, which is unneccesary
a.d("tr",{})
print("Ranking\tName\tScore")
for tr in table.find_all("tr"):
    data=a.text(tr) # get all text in this tr, this method return a list of strings
    print("\t".join( [ data[0],data[1],data[3] ]))
    count+=1
    if count==20:# only need the first 20 school
        break
