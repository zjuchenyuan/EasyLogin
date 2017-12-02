# EasyLogin.py

对requests和BeautifulSoup进一步封装，写爬虫代码更轻松~

不用再考虑UserAgent, Cookies, and Cache，让您专注于爬虫核心代码

## 请先安装依赖，建议使用Python3

    pip3 install -U requests[socks] bs4 -i https://pypi.doubanio.com/simple/ --trusted-host pypi.doubanio.com
    
## 说明

只需要下载EasyLogin.py就够了，examples文件夹是使用EasyLogin开发的例子们

## 来试试看吧~

首先导入包并创建一个对象

    from EasyLogin import EasyLogin
    a = EasyLogin()
    
然后发起一个请求

    html = a.get("http://ip.cn") #该网页源代码中的code标签内含有我们需要的 `自己的IP` 和 `自己所处的地理位置`

我需要的东西在`<code>`标签里面，我们把它拿出来

核心：在执行了get或post后，a.b就是一个BeautifulSoup对象

    #find_all是BeautifulSoup的方法，传入 `标签名称` 和 `标签属性的字典`
    code_tags = a.b.find_all("code",attrs={}) 
    myIP = code_tags[0].text
    mylocation = code_tags[1].text

> 为了简化这个操作我提供了f方法（其实一般用不着这个东西），为了提取符合条件的所有标签的文本内容

>    myIP,mylocation = a.f("code",attrs={})

获得了IP和location就能print啦~

    print(myIP) #将输出自己的IP
    print(mylocation) #例如“浙江省杭州市 电信”

我还需要网页中出现的图片、CSS、JS的链接以及文本，这些方法也不常用，看看就好

    print(a.img())
    print(a.css())
    print(a.js())
    print(";".join(a.text()))

## 文档

待完成...
    
简单地说，用get或post后self.b就是BeautifulSoup的对象

## 开发方法

> 论爬虫是怎么简单地被写出来的

1. 先完成一遍手动的不带工具流程，观察把握整体感觉

2. 打开Chrome开发者工具或者Burp，查看关键性的请求包，具体开发者工具截图见下文

3. 写点初始化的代码，引入包，a=EasyLogin()

4. 分析请求内容，从网页源代码或者其他请求中找到蛛丝马迹，拼凑出正确的请求包

    这一步就也许需要先get，从源代码得到token的操作和得到cookie
    
    （EasyLogin会自己处理好cookie，无需费心）

5. 发出post请求，分析返回的内容

    或许是个json？可以x.json()
    
    一般可能就是个页面，那就a.b.find吧
    
    （a是EasyLogin的对象，a.b是BeautifulSoup的对象，戳→[这里](http://cuiqingcai.com/1319.html)←看看BeautifulSoup怎么用）

6. 服务器能正确响应就基本完事啦，不妨再提取成函数、封装成类、给我发起一个Pull请求？

### 在我们继续之前

你是否足够了解HTTP协议？来看看[HTTP协议入门](http://www.ruanyifeng.com/blog/2016/08/http.html)吧

书写爬虫的时候有几个关键词需要理解：Cookie, User-Agent, Referer, Proxy，如果不理解没关系，Google就好了嘛

这里展示一个使用Chrome开发人员工具的屏幕截图，图中显示出了一个请求中浏览器向服务器发送了一些请求头(Headers)，其中就有关键的`Cookie`与`User-Agent` (大小写不敏感)，有时候如果对方有反爬虫措施，表示请求来源的`Referer`也是必要的。

![](img/chrome.jpg)

### 比较用与不用EasyLogin的代码区别

这个比较的例子其实就是我写`EasyLogin`的原因，BeautifulSoup这么长的单词，还有User-Agent的好烦噢... 本例子仅仅比较了最基础的用法

#### 不用EasyLogin，仅仅使用requests和BeautifulSoup：

```
import requests
from bs4 import BeautifulSoup
x = requests.get("http://ip.cn",headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"})
soup = BeautifulSoup(x.content.decode(),"html.parser")
for i in soup.find_all("code"):
    print(i.text)
```

#### 使用EasyLogin

```
from EasyLogin import EasyLogin
a=EasyLogin()
a.get("http://ip.cn")
for i in a.b.find_all("code"):
    print(i.text)
```

### 对象初始化

```
def __init__(self, cookie=None, cookiestring=None, cookiefile=None, proxy=None, session=None)
```

举个例子：

```
from EasyLogin import EasyLogin
a=EasyLogin(cookie={"a":"b","c":"d"},cookiestring="e=f;g=h",cookiefile="my.status",proxy="socks5://127.0.0.1:1080")
```

EasyLogin的构造时，可以提供`cookie`字典,`cookiestring`字符串或者一个`cookiefile`文件。另外，为了调试或网络加速，你也可以指定代理，这个代理将用于以后所有的http和https请求。

_cookie_ : 一个字典，键-值

_cookiestring_ : 你可以从Chrome开发者工具复制这个字符串

_cookiefile_ : 本参数传入一个文件名，这个文件由之后提到的`save=True`生成。如果指定的这个文件不存在，没有任何警告/异常。

### 发起一个http请求：get或者post

EasyLogin类提供了很多方法，但最重要的还是get和post

```
def get(self, url, result=True, save=False, headers=None, o=False, cache=None, r=False, cookiestring=None,failstring=None)

def post(self, url, data, result=True, save=False, headers=None,cache=None)
```

__result__: 得到的结果是否要使用BeautifulSoup解析，默认为True，解析产生的soup对象交给self.b；如果你在乎运行速率，请设置result=False，之后自行使用re模块或任何你喜欢的模块去解析你得到的东西。

__save__: 用于登录请求，默认为False，如果设置则将得到的cookie写入文件，写入的文件名由初始化时的cookiefile参数给定（默认是cookie.pickle）

__headers__: 类似于这样的字典 {"csrf-token":"xxxxxx"}, 将加入到请求的headers中; 默认的headers有Content-Type: application/x-www-form-urlencoded; charset=UTF-8，如果需要覆盖这个值，切记注意Content-Type的大小写 否则会导致不稳定的覆盖

__cache__: 缓存文件名或者True时将写入缓存文件，如果文件已经存在则将直接读取缓存而不真正发起请求；为了偷懒可以设置cache=True，则将采用md5(url)或md5(url+postdata)作为缓存文件名

__failestring__: 如果failstring出现在返回的网页中，抛出一个异常

对于每个请求，url都是必须的；如果对方没有任何反爬措施，只给定url就能发起GET，get方法将返回得到的HTML（如果需要get方法返回requests对象，设置o=True）

```
>>> page=a.get("http://ip.cn")
>>> print(len(page))
3133
```



## 例子们

[戳我看看例子们](examples/) 

基于EasyLogin开发了很多有趣的爬虫，这是一些我写的项目，如浙大云盘API、浙大教务网课表查询、汽车之家图片下载，供您参考~