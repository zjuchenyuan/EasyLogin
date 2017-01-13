# EasyLogin.py

对requests和BeautifulSoup进一步封装，写爬虫代码更轻松~

不用再考虑UserAgent, Cookies, and Cache，让您专注于爬虫核心代码

## 请先安装依赖，仅支持Python3

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

2. 打开Chrome开发者工具或者Burp，查看关键性的请求包

3. 写点初始化的代码，引入包，a=EasyLogin()

4. 分析请求内容，从网页源代码或者其他请求中找到蛛丝马迹，拼凑出正确的请求包

    这一步就也许需要先get，从源代码得到token的操作和得到cookie
    
    （EasyLogin会自己处理好cookie，无需费心）

5. 发出post请求，分析返回的内容

    或许是个json？可以x.json()
    
    一般可能就是个页面，那就a.b.find吧
    
    （a是EasyLogin的对象，a.b是BeautifulSoup的对象，戳→[这里](http://cuiqingcai.com/1319.html)←看看BeautifulSoup怎么用）

6. 服务器能正确响应就基本完事啦，不妨再提取成函数、封装成类、给我发起一个Pull请求？

## 例子们

[戳我看看例子们](examples/) 

基于EasyLogin开发了很多有趣的爬虫，这是一些我写的项目，如浙大云盘API、浙大教务网课表查询、汽车之家图片下载，供您参考~