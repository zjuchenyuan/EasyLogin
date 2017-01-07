#!C:/BioWeb/python.exe
#coding:utf-8
import cgi
from EasyLogin import EasyLogin
from urllib.parse import quote

print("Content-type:text/html;charset=utf-8\r\n\r\n")#这一步必须写好，请一定保留这一行

defaultRNA=quote(""">NR_000005.1 Homo sapiens small nucleolar RNA, C/D box 15A (SNORD15A), small nucleolar RNA
CTTCGATGAAGAGATGATGACGAGTCTGACTTGGGGATGTTCTCTTTGCCCAGGTGGCCTACTCTGTGCT
GCGTTCTGTGGCACAGTTTAAAGAGCCCTGGTTGAAGTAATTTCCTAAAGATGACTTAGAGGCATTTGTC
TGAGAAGG
""")

#获得用户的输入
RNA = cgi.FieldStorage().getvalue('rna',defaultRNA)


a=EasyLogin()

a.post("http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi","target=sno&query_data={}&option=-e+0.01&mode=blast".format(RNA))
print(a.b.find("body",attrs={"alink":"#660099"}))
