from EasyLogin import EasyLogin
from pprint import pprint

def peptidecutter(oneprotein):
    a = EasyLogin(proxy="socks5://127.0.0.1:1080") #speed up by using proxy
    a.post("http://web.expasy.org/cgi-bin/peptide_cutter/peptidecutter.pl",
        "protein={}&enzyme_number=all_enzymes&special_enzyme=Chym&min_prob=&block_size=60&alphtable=alphtable&cleave_number=all&cleave_exactly=&cleave_range_min=&cleave_range_max=".format(oneprotein)
        )
    table=a.b.find("table",{"class":"proteomics2"})
    tds=table.find_all("td")
    
    result = []
    oneline = []
    
    i = 0
    for td in tds:
        i+=1
        if i==1:
            content = td.text
        elif i==2:
            content = int(td.text)
        else:
            content = [int(i) for i in td.text.split()]
        oneline.append(content)
        if i==3:
            result.append(oneline)
            oneline=[]
            i=0
    return result

def fasta_reader(filename):
    filecontents = open(filename).read().split("\n")
    name = ""
    thedata = ""
    result=[]
    for line in filecontents:
        if not len(line): continue
        if line[0]=='>':
            if len(thedata):
                result.append([name,thedata])
                thedata = ""
            name = line
        else:
            thedata += line
    result.append([name,thedata])#don't forget the last one
    return result

def peptidecutter_more(filename):
    return [ [name,peptidecutter(oneprotein)] for name,oneprotein in fasta_reader(filename) ]

if __name__ == "__main__":
    #pprint(peptidecutter("SERVELAT"))
    import sys
    pprint(peptidecutter_more(sys.argv[1]))

