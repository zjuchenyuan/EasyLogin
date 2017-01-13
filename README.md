# EasyLogin.py

[ÖÐÎÄ°æÎÄµµ](README_ZH.md)

## Requirements, only support Python3

    pip3 install -U requests[socks] bs4 -i https://pypi.doubanio.com/simple/ --trusted-host pypi.doubanio.com
    
## Notes

Useful thing is only `EasyLogin.py`. All directories are examples, not needed for running.

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

To be finished...

You can take a look at my [examples](examples/)