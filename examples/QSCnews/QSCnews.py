from EasyLogin import EasyLogin
a=EasyLogin()

def getone(url):
    a.get(url)
    content_html=a.find("div",""" id="article-content-container" class="article-content-container" """)[0]
    title=content_html.find("h1").text
    return title,content_html

print(getone("http://www.qsc.zju.edu.cn/news/article/2016/12/%E6%BD%AE%E6%B5%99%E7%9C%8B%E4%BA%BA%E7%89%A9%E5%B9%B2%E4%BA%86%E8%BF%99%E9%94%85%E7%84%96%E9%B8%A1"))