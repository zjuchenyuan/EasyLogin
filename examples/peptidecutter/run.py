from EasyLogin import EasyLogin

data="SERVELAT"

a = EasyLogin()
a.post_dict("http://web.expasy.org/cgi-bin/peptide_cutter/peptidecutter.pl",{
    "protein":data,
    "enzyme_number":"all_enzymes",
    "special_enzyme":"Chym",
    "min_prob":"",
    "block_size":"60",
    "alphtable":"alphtable",
    "cleave_number":"all",
    "cleave_exactly":"",
    "cleave_range_min":"",
    "cleave_range_max":""}
    )
table=a.b.find("table",{"class":"proteomics2"})
tds=table.find_all("td")
i = 0
for td in tds:
    i+=1
    print(td.text,end='\t' if i!=3 else '\n')
    if i==3:
        i=0

