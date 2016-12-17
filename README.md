# EasyLogin

## Requirements 请先安装依赖

    pip3 install -U requests[socks] -i https://pypi.doubanio.com/simple
    pip3 install bs4 -i https://pypi.doubanio.com/simple
    
## Note 说明

Useful thing is only `EasyLogin.py`. All directories are examples, not needed for running.

只需要下载EasyLogin.py就够了，examples文件夹是使用EasyLogin开发的例子们

## Quickstart 来试试看吧~

Using EasyLogin is very EASY!

First, import it and create an object:  首先导入包并创建一个对象

    from EasyLogin import EasyLogin
    a = EasyLogin()
    
Then, make a get request or post request: 发起一个请求

    a.get("http://ip.cn")

Finally, I need the `code` tag: 我需要的东西在`<code>`标签里面，我们把它拿出来

    IP,location = a.f("code",attrs={})
    print(IP)
    print(location)

Moreover, I also need img, css, js and text: 我还需要网页中出现的图片、CSS、JS的链接以及文本

    print(a.img())
    print(a.css())
    print(a.js())
    print(";".join(a.text()))

## Documentation 文档

待完成...
    
简单地说，用get或post后self.b就是BeautifulSoup的对象