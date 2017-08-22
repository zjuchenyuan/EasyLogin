# encoding:utf-8
from EasyLogin import EasyLogin
from urllib.parse import quote

from PIL import Image
from ocr import ocr
import io
import sys
import time
a=EasyLogin()

"""
author: zjuchenyuan

EasyLogin: https://github.com/zjuchenyuan/EasyLogin
"""

nowyear = int(time.strftime("%Y"))
a.get("https://isisn.nsfc.gov.cn/egrantindex/funcindex/prjsearch-list")
from all import titles

def timestamp():
    import time
    return str(int(time.time() * 1000))

def getyzm():
    try:
        fp=io.BytesIO(a.get("https://isisn.nsfc.gov.cn/egrantindex/validatecode.jpg",result=False,o=True).content)
        image=Image.open(fp)
        yzm = ocr(image)
        if len(yzm)!=4:
            return False,''
        return  'success' in a.post("https://isisn.nsfc.gov.cn/egrantindex/funcindex/validate-checkcode","checkCode="+yzm).text, yzm
    except Exception as e:
        print("Error:",e)
        return False,''

def fuckyzm():
    status = False
    while not status:
        status, yzm = getyzm()
    return yzm

def post1(title_name, title_id, year, yzm, grant_code=220):
    title_name_quoted = quote(title_name)
    data = [
        ('resultDate',
         'prjNo:,ctitle:,psnName:,orgName:,subjectCode:,f_subjectCode_hideId:{title_id},subjectCode_hideName:,keyWords:,checkcode:{yzm},grantCode:{grant_code},subGrantCode:,helpGrantCode:,year:{year},sqdm:{title_id}'.format(**locals())),
        ('checkcode', yzm),
    ]
    a.post("https://isisn.nsfc.gov.cn/egrantindex/funcindex/prjsearch-list", data)
    data = [
        ('_search', 'false'),
        ('nd', timestamp()),
        ('rows', '100'),
        ('page', '1'),
        ('sidx', ''),
        ('sord', 'desc'),
        ('searchString',
         'resultDate^:prjNo%3A%2Cctitle%3A%2CpsnName%3A%2CorgName%3A%2CsubjectCode%3A{title_name_quoted}'
         '%2Cf_subjectCode_hideId%3A{title_id}%2CsubjectCode_hideName%3A{title_name_quoted}'
         '%2CkeyWords%3A%2Ccheckcode%3A{yzm}%2CgrantCode%3A{grant_code}%2CsubGrantCode%3A%2ChelpGrantCode%3A%2Cyear%3A{year}'
         '%2Csqdm%3A{title_id}[tear]sort_name1^:psnName[tear]sort_name2^:prjNo[tear]sort_order^:desc'.format(**locals())),
    ]
    a.post("https://isisn.nsfc.gov.cn/egrantindex/funcindex/prjsearch-list?flag=grid&checkcode=", data, headers={"Referer":"https://isisn.nsfc.gov.cn/egrantindex/funcindex/prjsearch-list","Content-Type":"application/x-www-form-urlencoded","X-Requested-With":"XMLHttpRequest"})
    res = []
    for row in a.b.find_all("row"):
        one = [year, title_name]
        another = [i.text for i in row.find_all("cell")]
        one.extend(another)
        res.append(one)
    return res

yzm = fuckyzm()
#x=post1("F020801.计算机网络体系结构", "F020801", "2014", yzm)
#print(x)

# x=post1("F020106.形式化方法", "F020106", "2015", yzm)


grant_codes ={
    "218": "all_mianshang",
    "220": "all_important220",
    "222": "all_zhongda",
    "339": "all_zhongdayanjiu",
    "429": "all_jieqing",
    "2699": "youqing2699",
    "432": "chuangxinyanjiu_quntixiangmu432",
    "433": "guoji_hezuo433",
    "649": "zhuanxiang649",
    "579": "lianhe579",
    "630": "qingnian630",
    "631": "diqu631",
    "632": "haiwai_gangao632",
    "635": "guojia_jichukexue_rencaipeiyang635",
    "51": "yiqishebei_yanzhi51",
    "52": "yiqi_yanzhi52",
    "70": "yingjiguanli70",
    "7161": "kexuezhongxin7161",
}

count = 0
grant_code = sys.argv[1]

try:
    progress = set(open('progress_'+grant_code+'.txt', 'r').read().split('\n'))
except:
    progress = []
for title in titles:
    title_id = title["id"]
    if len(title_id)==1 or title_id in progress:
        continue
    title_name = title["name"]
    
    assert sys.argv[1] in grant_codes, "please run with one of them: "+",".join(grant_codes.keys())
    startyear = nowyear
    if len(sys.argv)>2:
        startyear = int(sys.argv[2])
    if 1:
    #for grant_code in grant_codes:
        for year in range(startyear,nowyear+1): #only nowyear(2017), but you can change startyear to sys.argv[2]
            year = str(year)
            yzm = fuckyzm()
            #print(grant_codes[grant_code], title_name, year,yzm)
            print(grant_code, title_id, year, yzm)
            try:
                x = post1(title_name,title_id,year,yzm, grant_code)
            except Exception as e:
                print(e)
                try:
                    x = post1(title_name,title_id,year,yzm, grant_code)
                except Exception as e:
                    print(e)
                    open('error.txt','a', encoding='utf-8').write("\t".join([title_name,title_id,year,grant_code])+"\n")
            count += 1
            if count % 100 ==0:
                _a = EasyLogin()
                try:
                    _a.get("https://isisn.nsfc.gov.cn/egrantindex/funcindex/prjsearch-list")
                    a = _a
                except:
                    pass
            if len(x)>0:
                print(">>>ok: ", grant_code, title_id, year)
                #print(x)
                lines = []
                for one in x:
                    line = "\t".join(one)
                    lines.append(line)
                open(grant_codes[grant_code]+"_{startyear}-{nowyear}.txt".format(**locals()),"a", encoding='utf-8').write("\n".join(lines)+"\n")
    open('progress_'+grant_code+'.txt','a', encoding='utf-8').write(title_id+"\n")
