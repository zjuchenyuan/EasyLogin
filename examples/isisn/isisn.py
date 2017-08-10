# encoding:utf-8
from EasyLogin import EasyLogin
from urllib.parse import quote

from PIL import Image
from ocr import ocr
import io
a=EasyLogin()

"""
author: zjuchenyuan

EasyLogin: https://github.com/zjuchenyuan/EasyLogin
"""


a.get("https://isisn.nsfc.gov.cn/egrantindex/funcindex/prjsearch-list")

# titles from: https://isisn.nsfc.gov.cn/egrantindex/cpt/ajaxload-tree?locale=zh_CN&key=subject_code_index&cacheable=true&sqlParamVal=
titles = [{"id":"F02","title":"F02.计算机科学","name":"F02.计算机科学","pid":"F"},{"id":"F0201","title":"F0201.计算机科学的基础理论","name":"F0201.计算机科学的基础理论","pid":"F02"},{"id":"F020101","title":"F020101.理论计算机科学","name":"F020101.理论计算机科学","pid":"F0201"},{"id":"F020102","title":"F020102.新型计算模型","name":"F020102.新型计算模型","pid":"F0201"},{"id":"F020103","title":"F020103.计算机编码理论","name":"F020103.计算机编码理论","pid":"F0201"},{"id":"F020104","title":"F020104.算法及其复杂性","name":"F020104.算法及其复杂性","pid":"F0201"},{"id":"F020105","title":"F020105.容错计算","name":"F020105.容错计算","pid":"F0201"},{"id":"F020106","title":"F020106.形式化方法","name":"F020106.形式化方法","pid":"F0201"},{"id":"F020107","title":"F020107.机器智能基础理论与方法","name":"F020107.机器智能基础理论与方法","pid":"F0201"},{"id":"F0202","title":"F0202.计算机软件","name":"F0202.计算机软件","pid":"F02"},{"id":"F020201","title":"F020201.软件理论与软件方法学","name":"F020201.软件理论与软件方法学","pid":"F0202"},{"id":"F020202","title":"F020202.软件工程","name":"F020202.软件工程","pid":"F0202"},{"id":"F020203","title":"F020203.程序设计语言及支撑环境","name":"F020203.程序设计语言及支撑环境","pid":"F0202"},{"id":"F020204","title":"F020204.数据库理论与系统","name":"F020204.数据库理论与系统","pid":"F0202"},{"id":"F020205","title":"F020205.系统软件","name":"F020205.系统软件","pid":"F0202"},{"id":"F020206","title":"F020206.并行与分布式软件","name":"F020206.并行与分布式软件","pid":"F0202"},{"id":"F020207","title":"F020207.实时与嵌入式软件","name":"F020207.实时与嵌入式软件","pid":"F0202"},{"id":"F020208","title":"F020208.可信软件","name":"F020208.可信软件","pid":"F0202"},{"id":"F0203","title":"F0203.计算机体系结构","name":"F0203.计算机体系结构","pid":"F02"},{"id":"F020301","title":"F020301.计算机系统建模与模拟","name":"F020301.计算机系统建模与模拟","pid":"F0203"},{"id":"F020302","title":"F020302.计算机系统设计与性能评测","name":"F020302.计算机系统设计与性能评测","pid":"F0203"},{"id":"F020303","title":"F020303.计算机系统安全与评估","name":"F020303.计算机系统安全与评估","pid":"F0203"},{"id":"F020304","title":"F020304.并行与分布式处理","name":"F020304.并行与分布式处理","pid":"F0203"},{"id":"F020305","title":"F020305.高性能计算与超级计算机","name":"F020305.高性能计算与超级计算机","pid":"F0203"},{"id":"F020306","title":"F020306.新型计算系统","name":"F020306.新型计算系统","pid":"F0203"},{"id":"F020307","title":"F020307.计算系统可靠性","name":"F020307.计算系统可靠性","pid":"F0203"},{"id":"F020308","title":"F020308.嵌入式系统","name":"F020308.嵌入式系统","pid":"F0203"},{"id":"F0204","title":"F0204.计算机硬件技术","name":"F0204.计算机硬件技术","pid":"F02"},{"id":"F020401","title":"F020401.测试与诊断技术","name":"F020401.测试与诊断技术","pid":"F0204"},{"id":"F020402","title":"F020402.数字电路功能设计与工具","name":"F020402.数字电路功能设计与工具","pid":"F0204"},{"id":"F020403","title":"F020403.大容量存储设备与系统","name":"F020403.大容量存储设备与系统","pid":"F0204"},{"id":"F020404","title":"F020404.输入输出设备与系统","name":"F020404.输入输出设备与系统","pid":"F0204"},{"id":"F020405","title":"F020405.高速数据传输技术","name":"F020405.高速数据传输技术","pid":"F0204"},{"id":"F0205","title":"F0205.计算机应用技术","name":"F0205.计算机应用技术","pid":"F02"},{"id":"F020501","title":"F020501.计算机图形学","name":"F020501.计算机图形学","pid":"F0205"},{"id":"F020502","title":"F020502.计算机图像与视频处理","name":"F020502.计算机图像与视频处理","pid":"F0205"},{"id":"F020503","title":"F020503.多媒体与虚拟现实技术","name":"F020503.多媒体与虚拟现实技术","pid":"F0205"},{"id":"F020504","title":"F020504.生物信息计算","name":"F020504.生物信息计算","pid":"F0205"},{"id":"F020505","title":"F020505.科学工程计算与可视化","name":"F020505.科学工程计算与可视化","pid":"F0205"},{"id":"F020506","title":"F020506.人机界面技术","name":"F020506.人机界面技术","pid":"F0205"},{"id":"F020507","title":"F020507.计算机辅助技术","name":"F020507.计算机辅助技术","pid":"F0205"},{"id":"F020508","title":"F020508.模式识别理论及应用","name":"F020508.模式识别理论及应用","pid":"F0205"},{"id":"F020509","title":"F020509.人工智能应用","name":"F020509.人工智能应用","pid":"F0205"},{"id":"F020510","title":"F020510.信息系统技术","name":"F020510.信息系统技术","pid":"F0205"},{"id":"F020511","title":"F020511.信息检索与评价","name":"F020511.信息检索与评价","pid":"F0205"},{"id":"F020512","title":"F020512.知识发现与知识工程","name":"F020512.知识发现与知识工程","pid":"F0205"},{"id":"F020513","title":"F020513.新应用领域中的基础研究","name":"F020513.新应用领域中的基础研究","pid":"F0205"},{"id":"F0206","title":"F0206.自然语言理解与机器翻译","name":"F0206.自然语言理解与机器翻译","pid":"F02"},{"id":"F020601","title":"F020601.计算语言学","name":"F020601.计算语言学","pid":"F0206"},{"id":"F020602","title":"F020602.语法分析","name":"F020602.语法分析","pid":"F0206"},{"id":"F020603","title":"F020603.汉语及汉字信息处理","name":"F020603.汉语及汉字信息处理","pid":"F0206"},{"id":"F020604","title":"F020604.少数民族语言文字信息处理","name":"F020604.少数民族语言文字信息处理","pid":"F0206"},{"id":"F020605","title":"F020605.机器翻译理论方法与技术","name":"F020605.机器翻译理论方法与技术","pid":"F0206"},{"id":"F020606","title":"F020606.自然语言处理相关技术","name":"F020606.自然语言处理相关技术","pid":"F0206"},{"id":"F0207","title":"F0207.信息安全","name":"F0207.信息安全","pid":"F02"},{"id":"F020701","title":"F020701.密码学","name":"F020701.密码学","pid":"F0207"},{"id":"F020702","title":"F020702.安全体系结构与协议","name":"F020702.安全体系结构与协议","pid":"F0207"},{"id":"F020703","title":"F020703.信息隐藏","name":"F020703.信息隐藏","pid":"F0207"},{"id":"F020704","title":"F020704.信息对抗","name":"F020704.信息对抗","pid":"F0207"},{"id":"F020705","title":"F020705.信息系统安全","name":"F020705.信息系统安全","pid":"F0207"},{"id":"F0208","title":"F0208.计算机网络","name":"F0208.计算机网络","pid":"F02"},{"id":"F020801","title":"F020801.计算机网络体系结构","name":"F020801.计算机网络体系结构","pid":"F0208"},{"id":"F020802","title":"F020802.计算机网络通信协议","name":"F020802.计算机网络通信协议","pid":"F0208"},{"id":"F020803","title":"F020803.网络资源共享与管理","name":"F020803.网络资源共享与管理","pid":"F0208"},{"id":"F020804","title":"F020804.网络服务质量","name":"F020804.网络服务质量","pid":"F0208"},{"id":"F020805","title":"F020805.网络安全","name":"F020805.网络安全","pid":"F0208"},{"id":"F020806","title":"F020806.网络环境下的协同技术","name":"F020806.网络环境下的协同技术","pid":"F0208"},{"id":"F020807","title":"F020807.网络行为学与网络生态学","name":"F020807.网络行为学与网络生态学","pid":"F0208"},{"id":"F020808","title":"F020808.移动网络计算","name":"F020808.移动网络计算","pid":"F0208"},{"id":"F020809","title":"F020809.传感网络协议与计算","name":"F020809.传感网络协议与计算","pid":"F0208"}]
# print([i["name"] for i in titles])

def timestamp():
    """
    返回当前时间戳字符串，毫秒数
    """
    import time
    return str(int(time.time() * 1000))

def getyzm():
    """
    获取验证码并识别，返回(本次识别是否成功, 识别结果)
    """
    fp=io.BytesIO(a.get("https://isisn.nsfc.gov.cn/egrantindex/validatecode.jpg",result=False,o=True).content)
    image=Image.open(fp)
    yzm = ocr(image)
    try:
        return  'success' in a.post("https://isisn.nsfc.gov.cn/egrantindex/funcindex/validate-checkcode","checkCode="+yzm).text, yzm
    except:
        return False,''

def fuckyzm():
    """
    不断尝试，直到返回一个正确的验证码
    """
    status = False
    while not status:
        status, yzm = getyzm()
    return yzm

def post1(title_name, title_id, year, yzm, grant_code=220):
    """
    发起一次查询，参数：
        title_name: "F020801.计算机网络体系结构"
        title_id : "F020801"
        year: "2014"
        yzm: 验证码，传入fuckzym()即可
        grant_code: 见下方的grant_codes的说明
    """
    title_name_quoted = quote(title_name)
    data = [
        ('resultDate',
         'prjNo:,ctitle:,psnName:,orgName:,subjectCode:,f_subjectCode_hideId:{title_id},subjectCode_hideName:,keyWords:,checkcode:{yzm},grantCode:{grant_code},subGrantCode:,helpGrantCode:,year:{year},sqdm:{title_id}'.format(**locals())),
        ('checkcode', yzm),
    ]
    # 第一次post
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
    # 第二次post
    a.post("https://isisn.nsfc.gov.cn/egrantindex/funcindex/prjsearch-list?flag=grid&checkcode=", data, headers={"Referer":"https://isisn.nsfc.gov.cn/egrantindex/funcindex/prjsearch-list","Content-Type":"application/x-www-form-urlencoded","X-Requested-With":"XMLHttpRequest"})
    res = []
    for row in a.b.find_all("row"): # 每个row是一行结果
        one = [year, title_name]
        another = [i.text for i in row.find_all("cell")]
        one.extend(another)
        res.append(one) 
        # one: year title   id  title_id    name    person  university  amount  time
        # example: 2013 F020104.算法及其复杂性  61332002    F020104 分布式计算智能理论及应用    张军    华南理工大学    310 2014-01至2018-12
    return res

yzm = fuckyzm()

# 测试代码
# x=post1("F020801.计算机网络体系结构", "F020801", "2014", yzm)
# print(x)


grant_codes ={
    "220": "重点项目",
    "222": "重大项目",
    "339": "重大研究计划",
    "429": "杰青",
    "579": "联合基金",
}
        
for title in titles: # 对共70个领域进行循环
    title_id = title["id"]
    title_name = title["name"]
    for grant_code in grant_codes: #重点、重大、杰青、联合5个
        for year in range(1997,2018): #年份从1997~2017
            year = str(year)
            yzm = fuckyzm()
            print(grant_codes[grant_code], title_name, year,yzm)
            x = post1(title_name,title_id,year,yzm, grant_code)
            if len(x)>0:
                print(x)
                lines = []
                for one in x:
                    line = "\t".join(one)
                    lines.append(line)
                open(grant_codes[grant_code]+"_1997-2017.txt","a").write("\n".join(lines)+"\n")
