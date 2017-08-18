from EasyLogin import EasyLogin
a=EasyLogin()

def get_question(qid):
    global a
    html=a.get("http://gre.kmf.com/question/{qid}.html".format(qid=qid), cache=True)
    soup = a.b
    question_type = soup.find("input",{"id":"GlobeQUESTIONNAME"})["value"]
    question_from = soup.find("span",{"class":"gray"}).text
    good_count = soup.find("span",{"class":"actionbg good-ico"}).find_next_sibling("span",{"class":"count"}).text
    bad_count = soup.find("span",{"class":"actionbg bad-ico"}).find_next_sibling("span",{"class":"count"}).text
    passage = ""
    if question_type=='填空':
        div_body = "exa-question"
        next_link = soup.find("div",{"class":"clearfix exa-que-bottom"}).find("a")["href"]
    elif question_type=='阅读':
        div_body = "queanswer"
        passage = soup.find("div",{"class":"quecontent"}).find("div",{"class":"content"}).text.strip()
        next_link = soup.find("div",{"class":"queanswer"}).find("li",{"class":"current"}).find_next_sibling("li")
        if next_link is not None:
            next_link = next_link.find("a")["href"]
    question_body = soup.find("div",{"class":div_body}).find("div",{"class":"mb20"}).text.strip()
    question_selections = [""]
    try:
        # 普通的单选题/多选题
        for i in soup.find("form", {"id":"QuestionSubmit"}).find_all("li"):
            question_selections.append(". ".join((i.find("strong").text, i.text.lstrip(i.find("strong").text))))
    except:
        # 有多个空
        t = 0
        for ul in soup.find("div",{"id":"QuestionSubmit"}).find_all("ul"):
            t+=1
            question_selections.append("Blank"+str(t))
            question_selections.extend([". ".join((i.find("strong").text, i.text.lstrip(i.find("strong").text))) for i in ul.find_all("li")])
    question_body += "\n".join(question_selections)
    answer = soup.find("b",{"class":"que-anser-right"}).text
    explain = soup.find("div",{"id":"Explain"}).text.strip()
    return {
        "id": qid,
        "type": question_type,
        "from": question_from,
        "good_count": good_count,
        "bad_count": bad_count,
        "passage":passage,
        "body": question_body,
        "answer": answer,
        "explain": explain,
        "next_id": next_link.replace("/question/","").replace(".html","") if next_link else None
    }
from pprint import pprint
import string
theloop = (string.digits+string.ascii_lowercase)[::-1]
data = get_question("42nkhj")#92nm4j
while data["next_id"]:
    data = get_question(data["next_id"])
    print(data["body"][:20].replace("题真题","日真题").replace("（","\t").replace("）","\t").replace("年","\t").replace("月","\t").replace("日","\t"))
#for x1 in theloop[theloop.find('k'):]:
#    for x2 in theloop:
#        id = "a2n{x1}{x2}j".format(**locals())
#        print(id)
#        data = get_question(id)
#        print(data["body"][:20])