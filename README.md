# EasyLogin.py

One file package `EasyLogin.py`, for writing spiders more easily

Just forget UserAgent, Cookies, and Cache... Let EasyLogin take care of all these things, so you can focus on your core code.

[中文版文档](README_ZH.md)

## Requirements, only support Python3

    pip3 install -U requests[socks] bs4 -i https://pypi.doubanio.com/simple/ --trusted-host pypi.doubanio.com

## Quickstart

Using EasyLogin is very EASY!

First, import it and create an object:

    from EasyLogin import EasyLogin
    a = EasyLogin()
    
Then, make a get request or post request:

    html = a.get("http://ip.cn") # you can look up the source code of this "http://ip.cn"

What I need are in the `<code>` tag, extract these `<code>` tag:

Tip: use `a.b` as a BeautifulSoup object

    code_tags = a.b.find_all("code",attrs={}) #find_all is a method of BeautifulSoup object
    myIP = code_tags[0].text
    mylocation = code_tags[1].text

> To simplify this, I created a `f` method, return text of all tags that match tag name and attrs: 

>    myIP,mylocation = a.f("code",attrs={})

Finally, just print them~

    print(myIP) #this will print your own IP
    print(mylocation)

Moreover, I also need img, css, js and text:

    print(a.img())
    print(a.css())
    print(a.js())
    print(";".join(a.text()))

## Documentation

You can take a look at my [examples](examples/)

### Object Initialization

```
def __init__(self, cookie=None, cookiestring=None, cookiefile=None, proxy=None, session=None)
```

Example:

```
from EasyLogin import EasyLogin
a=EasyLogin(cookie={"a":"b","c":"d"},cookiestring="e=f;g=h",cookiefile="my.status",proxy="socks5://127.0.0.1:1080")
```

When you create the object, you can specify cookie by using `cookie` or `cookiestring`, or even restore cookie status from a file `cookiefile`. And for debug or bypass GFW, you can set the proxy.

__cookie__ : a dict, key-value

__cookiestring__: You can copy this string from Chrome

__cookiefile__: this file is created by `save=True`, which we will talk about later. If this file does not exist, nothing will happen.

## get/post

Here are a lot of useful methods in EasyLogin, but the essential one must be `get` and `post`

```
def get(self, url, result=True, save=False, headers=None, o=False, cache=None, r=False, cookiestring=None,failstring=None)

def post(self, url, data, result=True, save=False, headers=None,cache=None)
```