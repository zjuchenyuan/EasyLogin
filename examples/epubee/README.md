# epubee电子书下载

本例子对cn.epubee.com上的电子书下载地址进行穷举，使用mpms多进程多线程执行爬虫任务

## 请先准备依赖

[简易Python多进程-多线程任务队列 mpms](https://github.com/aploium/mpms)

## 代码说明

这个代码主要参考mpms给出的例子，而这个例子基本就定下了整个文件的框架，mpms的设计不在此处的讨论范围

```
worker函数：
    爬虫函数，使用EasyLogin简单完成爬取任务
    接受页面id参数，返回一个结果的list

handler函数：
    除第一个meta外需要接受worker的所有返回值
    所有的线程同时只会有一个handler在执行，所以只应该完成写文件等耗时较少的操作

main函数：
    打开文件，创建队列，用循环把任务塞入队列，join等待完成
```

## 随便写写

多线程能显著提高效率，mpms是做得挺简单的，只要抄模板就好了23333

注意print函数也是一个非常耗时的操作，应该尽量少print

本代码仅仅生成了下载链接，具体的下载需要下一步的处理：对downloadlink.txt加上域名前缀后，用wget --content-disposition -nc -i downloadlink.txt

每写一个例子就发现EasyLogin还有需要改进的地方，这次对EasyLogin的init函数加入了session参数，防止每次worker都创建Session对象而浪费时间

想了想这个EasyLogin对象还是不能共享的，否则，在高并发的时候可能多个线程同时修改a.b，之后的a.getlist就是瞎扯了Orz 所以退而求其次选择在进程级别共享Session对象（注意worker函数是拿不到全局所有线程共享的变量的）

至于这样改动EasyLogin以支持高并发有没有效果，待测试咯

使用wget下载似乎有中文乱码问题，一旦产生了乱码的文件名就很难删除，还是用python一个个调用curl -OJ吧

## Example Code for further download

```
c=input()
while True:
    print("http://cn.epubee.com/"+c)
    try:
        c=input()
    except:
        break
```

```
from os import system
for line in open("filelist.txt"):
    url=line.replace("\n","")
    print(url)
    system("curl -OJ \"{}\"".format(url))
```
