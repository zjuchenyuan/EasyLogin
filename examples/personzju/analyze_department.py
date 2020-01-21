data = []

for _line in open("personzju.txt"):
    dep = _line.split("\t")[1].split(" | ")[0]
    if "学院" in dep and dep.split("学院")[-1]!="":
        dep = dep.split("学院")[0]+"学院"
    data.append(dep)

from collections import Counter
from pprint import pprint
pprint(Counter(data))