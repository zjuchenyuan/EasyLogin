# The most popular dog breeds in america

![dog](http://cdn.akc.org/social/Lab-puppies.jpg)

## 数据来源

http://www.akc.org/news/the-most-popular-dog-breeds-in-america/

## 怎么写出这个爬虫

1. 打开网页，看到我们需要的数据在table里面

2. 查看源代码，搜索RETRIEVERS (LABRADOR)，发现table属性是这样的：

```
<table border="0" cellpadding="0" cellspacing="0" style="width:100%">
```

3. 写代码咯，戳[dog.py](dog.py)

    首先初始化EasyLogin，指定要走代理翻墙
    
    然后用get拿到网页，并存储缓存到cache.html
    
    用f方法搜索table，指定text=True只要文本，注意搜索是find_all的，这个表单需要[0]

    这里我没有处理数据，简单print出来，用int(i)的方法判断是整数还是dog名称