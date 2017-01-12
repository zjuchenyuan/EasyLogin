from EasyLogin import EasyLogin
from pypinyin import lazy_pinyin
a=EasyLogin()

def gethot():
    """
    从汽车之家官网手机版获得热门品牌
    返回一个dict：{ 品牌名称:[详情url，品牌拼音]}
    """
    a.get("http://m.autohome.com.cn/",cache=True)
    brands = a.b.find("div",{"class":"brand"})
    result = {}
    for one in brands.find_all("a"):
        name = one.text
        pinyin = ''.join(lazy_pinyin(name))
        href = "http://"+one["href"][2:] #url地址是形如//car.m.autohome.com.cn/brand/1/#pvareaid=100239，需要去掉前置的//
        result[one.text]=[href, pinyin]
    return result

def getbrand(url):
    """
    输入一个品牌的url，此url可以从gethot函数获得
    返回数组，其元素为：[名称，价格，类型，图片url，详情url，id]
    其中图片url做了替换，输出的为640x480（已知最高清）的图片url
    """
    a.get(url,cache=True)
    items = a.b.find_all("li")
    result = []
    for one in items:
        name = one.find("h4").text
        price = one.find("p",{"class":"price"}).text
        leixin = one.find("p",{"class":"infor"}).text
        picture_url = "http://"+one.find("img")["src"][2:].replace("192x144_0_q30_","640x480_0_q40_")
        detail_url = "http://"+one.find("a")["href"][2:]
        id = detail_url.replace("http://m.autohome.com.cn/","").split("/")[0]
        result.append([name,price,leixin,picture_url,detail_url,id])
    return result

def morepic(id):
    """
    从一个车型得到更多的车身图片，id来自getbrand函数的输出
    返回图片url的数组
    其中url做了替换，输出的为640x480（已知最高清）的图片url
    """
    a.get("http://car.m.autohome.com.cn/pic/series/{}-0-1-0-i0.html".format(id),cache=True)
    items = a.b.find("div",{"id":"listPic"}).find_all("img")
    result = []
    for one in items:
        url = "http://"+one["src"][2:].replace("280x210_0_q30","640x480")
        result.append(url)
    return result
        
if __name__ == "__main__":
    fp1=open("record.txt","w")
    fp2=open("download_command.bat","w")
    for brand_name,brand_href_and_pinyin in gethot().items():
        url = brand_href_and_pinyin[0]
        for detail in getbrand(url):
            print(brand_name,detail[0])
            #创建目录并切换至子目录，这是BAT命令，only for windows
            fp2.write("""md "{}\\{}" & cd "{}\\{}" \n""".format(brand_name,detail[0],brand_name,detail[0]))
            chexin_id = detail[5]
            for pic_url in morepic(chexin_id):
                fp1.write("{}\t{}\t{}\n".format(brand_name,detail[0],pic_url))
                #调用curl.exe完成下载操作，您需要下载curl，我的notebook提供下载
                fp2.write("curl -O {}\n".format(pic_url))
            fp2.write("cd ..\\..\\ \n")#切换到上级目录
    fp1.close()
    fp2.close()
    