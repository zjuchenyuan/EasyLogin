# EasyLogin

## Requirements

    pip3 install -U requests[socks] -i https://pypi.doubanio.com/simple
    pip3 install bs4 -i https://pypi.doubanio.com/simple
    
## Note

Useful thing is only `EasyLogin.py`. All directories are examples, not needed for running.
    
## Quickstart

Using EasyLogin is very EASY!

First, import it and create an object: 

    from EasyLogin import EasyLogin
    a = EasyLogin()
    
Then, make a get request or post request:

    a.get("http://ip.cn")

Finally, I need the `code` tag:

    IP,location = a.f("code",attrs={})
    print(IP)
    print(location)