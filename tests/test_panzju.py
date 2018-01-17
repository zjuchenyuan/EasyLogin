# coding=utf-8
from __future__ import with_statement
import unittest
import os
import sys
import requests
import threading
from EasyLogin import EasyLogin
oldcwd = os.getcwd()
os.chdir("examples/panzju")
sys.path.append(".")

from panzju import login, islogin, upload, share, download, logined_download
username, password = os.environ["panzju_username"], os.environ["panzju_password"]

a = EasyLogin()
s = threading.local()

import time
myprint = lambda s: print("[{showtime}] {s}".format(showtime=time.strftime("%Y-%m-%d %H:%M:%S"), s=s))

def gettime():
    return time.strftime("%Y%m%d%H%M%S")

from .panzju_fencrypt import fencrypt, ENCRYPTION_PASSWORD, ENCRYPTION_METHOD, cryptor

def fdecrypt_data(ciphertext):
    c = cryptor.Cryptor(ENCRYPTION_PASSWORD, ENCRYPTION_METHOD)
    return c.decrypt(ciphertext)

os.chdir(oldcwd)

class TestPanzju(unittest.TestCase):
    """testing using https://github.com/"""
    def test_a_login(self):
        self.assertTrue(login(username, password, a))
    
    def test_b_islogin(self):
        s.token = islogin(a)
    
    def test_c_upload(self):
        print(s.token)
        with open("green.jpg", "rb") as fp:
            s.picdata = fp.read()
        s.fileid = upload(s.token, gettime(), s.picdata, filesize=len(s.picdata), _a=a)
    
    def test_d_share(self):
        s.sharelink = share(s.token, s.fileid)
        self.assertIsInstance(s.sharelink, str)
    
    def test_e_download(self):
        url = download(s.sharelink)
        x = requests.get(url)
        self.assertEqual(s.picdata, x.content)
    
    def test_f_encryptupload(self):
        s.fileid_enc = upload(s.token, gettime()+"_encrypt", s.picdata, filesize=len(s.picdata), _a=a, fencrypt=fencrypt)
        s.sharelink_enc = share(s.token, s.fileid_enc)
    
    def test_g_decryptdownload(self):
        url = logined_download(s.sharelink_enc, a)
        x = requests.get(url)
        plaintext = fdecrypt_data(x.content)
        self.assertEqual(s.picdata, plaintext)