# The most popular dog breeds in america

![dog](http://cdn.akc.org/social/Lab-puppies.jpg)

## 数据来源

http://www.akc.org/news/the-most-popular-dog-breeds-in-america/

## 怎么写出这个爬虫

打开网页，看到我们需要的数据在table里面

查看源代码，搜索表格的第一行的dog name：`RETRIEVERS (LABRADOR)`，发现数据果然在table中，而这个table的属性是这样的：

```
<table border="0" cellpadding="0" cellspacing="0" style="width:100%">
```

准备做好了，就开始写代码咯，已经写好的代码戳[dog.py](dog.py)

    首先初始化EasyLogin，指定要走代理翻墙
    
    然后用get拿到网页，并存储缓存到cache.html
    
    用find方法搜索table，find只需要把table的参数原样丢进去，指定text=True表示只要文本，注意搜索是find_all的，这个表单需要[0]

    这里我没有处理数据，简单print出来，用int(i)的方法判断是整数还是dog名称