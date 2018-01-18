# coding=utf-8
import unittest
import os
from EasyLogin import EasyLogin, EasyLogin_ValidateFail

if os.environ.get("GFW"):
    a = EasyLogin(proxy="socks5://127.0.0.1:10800", cachedir="__pycache__")
else:
    a = EasyLogin(cachedir="__pycache__")

class TestHttpbin(unittest.TestCase):
    """testing using https://httpbin.org/"""

    def test_homepage(self):
        """https://httpbin.org/"""
        html =a.get("https://httpbin.org/")
        self.assertIn('httpbin', html)

    def test_headers(self):
        """https://httpbin.org/headers"""
        x = a.get("https://httpbin.org/headers",
            headers={
                "accept_encoding": "gzip, deflate, sdch, br",
                "Hello-World": "test header",
            },
            o = True
        ) # type: Response

        self.assertEqual("application/json", x.headers["Content-Type"])
        returnjson = x.json()
        self.assertEqual("test header", returnjson["headers"]["Hello-World"])

    def test_post(self):
        """POST https://httpbin.org/post"""
        x = a.post("https://httpbin.org/post", "postdata=123456")
        self.assertEqual("application/json", x.headers["Content-Type"])
        returnjson = x.json()
        self.assertEqual("123456", returnjson["form"]["postdata"])

    def test_cookie(self):
        """https://httpbin.org/cookies/set?name=value"""
        x = a.get("https://httpbin.org/cookies/set?cookie1=value", o=True)
        self.assertEqual(302, x.status_code)
        x = a.get("https://httpbin.org/cookies", o=True, result=False)
        self.assertEqual("application/json", x.headers["Content-Type"])
        returnjson = x.json()
        self.assertEqual("value", returnjson["cookies"]["cookie1"])

    def test_cache(self):
        """get: cache"""
        a.get("https://httpbin.org/cookies", cache=True, o=True) # store cache
        a.get("https://httpbin.org/cookies/set?cookie2=value2") # change cookie
        x = a.get("https://httpbin.org/cookies", cache=True, o=True) # readcache
        self.assertNotIn("cookie2", x.json()["cookies"]) # should not appear because cache
        x = a.get("https://httpbin.org/cookies", o=True) # not using cache
        self.assertEqual("value2", x.json()["cookies"]["cookie2"])
    
    def test_setcookie(self):
        """setcookie"""
        a.setcookie("cookie3=value3; cookie4=value4;")
        html = a.get("https://httpbin.org/cookies")
        self.assertIn("value3", html)
        self.assertIn("value4", html)
    
    def test_failstring(self):
        """get: failstring"""
        with self.assertRaises(EasyLogin_ValidateFail) as cm:
            html = a.get("https://httpbin.org/get?errorrrr=1", failstring="errorrrr")
        x = cm.exception.args[0]
        self.assertEqual(200, x.status_code)