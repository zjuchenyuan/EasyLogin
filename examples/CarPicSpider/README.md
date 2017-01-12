# CarPicSpider

爬取汽车之家的汽车车身图片

Inspired by https://github.com/FindHao/CarPicSpider

![screenshot](screenshot.jpg)

[pic_result.rar](https://api.chenyuan.me/fangcloud2/210001485088) 427.63MB，**下载前请先Star本项目**

## 直接运行

直接运行将生成两个文件：`record.txt`和`download_command.bat`

    record.txt的格式为：品牌名\t车型名称\t图片url

    download_command.bat：调用curl.exe执行下载命令

`result.zip`提供这两个文件，**下载前请先Star本项目**，[戳我下载](https://raw.githubusercontent.com/zjuchenyuan/EasyLogin/master/examples/CarPicSpider/result.zip)

## Cache缓存

本example使用了`Cache=True`参数，表示将`md5(url)`作为`缓存文件的文件名`

提供`cache_files.zip`，解压至本目录后即可不发起任何网络请求，从而实现快速循环，[戳我下载](https://raw.githubusercontent.com/zjuchenyuan/EasyLogin/master/examples/CarPicSpider/cache_files.zip)

## 函数说明

### gethot

    从汽车之家官网手机版获得热门品牌

    返回一个dict：{ 品牌名称:[详情url，品牌拼音]}

### getbrand(url):

    输入一个品牌的url，此url可以从gethot函数获得

    返回数组，其元素为：[名称，价格，类型，图片url，详情url，id]

    其中图片url做了替换，输出的为640x480（已知最高清）的图片url

### morepic(id):

    从一个车型得到更多的车身图片，id来自getbrand函数的输出

    返回图片url的数组

    其中url做了替换，输出的为640x480（已知最高清）的图片url

