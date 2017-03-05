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

### Before we continue...

Do you know about HTTP protocol? If not, look at [this](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol).

Here are some keywords for writing a spider: Cookie, User-Agent, Referer, Proxy

Here is a screenshot of using Chrome Developer Tools to inspect the http(s) request, in this picture, you can see some headers are sent to the server. Among these headers, `Cookie` and `User-Agent`(case-insensitive) are the most important for us writing a spider, by the way, sometimes the `Referer` is also essential.

![](img/chrome.jpg)


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

## Make a request: get/post

Here are a lot of useful methods in EasyLogin, but the essential ones must be `get` and `post`

```
def get(self, url, result=True, save=False, headers=None, o=False, cache=None, r=False, cookiestring=None,failstring=None)

def post(self, url, data, result=True, save=False, headers=None,cache=None)
```

__result__: use the BeautifulSoup to parse the html, default is True (if you care about time performance, please use `result=False` and use `re` module or whatever you want to extract information needed)

__save__: used in login request, if `save=True`, write the cookie to a file, filename is given by `cookiefile` during the object initialization(default is cookie.pickle)

__headers__: dict, like {"csrf-token":"xxxxxx"}, added to request headers

__cache__: filename to write cache, if already exists, use cache rather than really get; using cache=True to use md5(url) as cache file name

__failestring__: if failstring occurs in text, raise an exception

for each request, the url is the basic one, for example, if a website has taken no anti-crawler actions, the url itself is enough.

```
>>> page=a.get("http://ip.cn")
>>> print(len(page))
3133
```

### Need the request object?

this will get the source code of "ip.cn", we choose this as a demo, because it contains a useful information: your ip and your location.

the technique below the EasyLogin is `requests`, and this function is actually calling requests.get (more precisely, requests.Session().get). So you may wonder how to get the request object like you get by doing `x=requests.get("http://ip.cn")`, the method is as below:

```
>>> from EasyLogin import EasyLogin
>>> a=EasyLogin()
>>> x=a.get("http://ip.cn",o=True)
>>> print(x.headers)
{'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'Content-Type': 'text/html; charset=UTF-8', 'Content-Encoding': 'gzip', 'Server': 'nginx/1.10.0 (Ubuntu)', 'Date': 'Sun, 05 Mar 2017 14:05:57 GMT'}
>>> x=a.get("http://httpbin.org/redirect-to?url=http%3A%2F%2Fexample.com%2F", o=True)
>>> x.headers["Location"]
'http://example.com/'
```

### use cache to speed up!

Imaging you are crawling a website, you need to modify the information extracting rule many times, but you don't need to crawl the website that much, once you have find out the url needed to crawl, just request one time and reuse the cache afterwards. I strongly recommend using cache to save your time!

```
>>> for i in range(5):
...     a.get("http://httpbin.org/stream/{i}".format(i=i), cache=True)
...
>>> import os;os.listdir(".")
['189091a11fd93218d3f95b4365576163', '3647fa4f6df52ce929158bc88cffbc59', '4c1e81a0b25286d8582f650e3b71f3aa', '896fa92d285edffb17509f10218f8b6e', 'b9a9e3036d06219bca93b22889f31fec']
```

if you want to control the cache filename, just set the filename to cache, like `cache="%d.html"%i`, otherwise if you don't care about the filename, just use `cache=True`, EasyLogin will use the md5(url) as the filename in get request, and use the md5(url+request_data) in post request.

----

# Examples

You can take a look at my [examples](examples/)