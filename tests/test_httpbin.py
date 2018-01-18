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
    
    def test_d(self):
        """d"""
        a.get("https://httpbin.org", cache=True)
        a.d("h2", {"id": "ENDPOINTS"})
        self.assertIsNone(a.b.find("h2", {"id": "ENDPOINTS"}))
    
    def test_post_dict_cache(self):
        """post_dict: cache=True"""
        try:
            os.unlink("__pycache__/c346ef69fd49bbf773becfca0b3306a5")
        except:
            pass
        oldcount = len(os.listdir("__pycache__"))
        x = a.post_dict("https://httpbin.org/post", {"postdata_dict": "666666"}, cache=True)
        self.assertEqual("666666", x.json()["form"]["postdata_dict"])
        newcount = len(os.listdir("__pycache__"))
        self.assertEqual(1, newcount-oldcount)
        self.assertTrue(os.path.exists("__pycache__/c346ef69fd49bbf773becfca0b3306a5"))
        x2 = a.post_dict("https://httpbin.org/post", {"postdata_dict": "666666"}, cache=True)
        self.assertEqual("666666", x2.json()["form"]["postdata_dict"])
    
    def test_find(self):
        """find: text=True"""
        a.get("https://httpbin.org", cache=True)
        self.assertEqual("ENDPOINTS", a.find("h2",'id="ENDPOINTS"', text=True)[0])
    
    def test_text(self):
        """text"""
        a.get("https://httpbin.org/forms/post")
        texts = a.text()
        self.assertIn("Small",texts)
        self.assertIn("Medium",texts)
        self.assertIn("Large",texts)
    
    def test_save_load_showcookie(self):
        """save"""
        a.get("https://httpbin.org/cookies/set?cookie5=value5")
        a.save()
        newa = EasyLogin._import()
        cookiestring = newa.showcookie()
        self.assertIn("cookie5=value5",cookiestring)