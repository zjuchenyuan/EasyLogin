from EasyLogin import EasyLogin
from pprint import pprint, pformat
import json
import codecs

__all__ = ["ZJUAUTHME"]

def rsa_encrypt(password_str, e_str, M_str):
    password_int = int(codecs.encode(password_str.encode("ascii"), 'hex'), 16)
    e_int = int(e_str, 16) # equal to 0x10001
    M_int = int(M_str, 16) # Modulus number
    result_int = pow(password_int, e_int, M_int) # pow is a built-in function in python
    return hex(result_int)[2:].rjust(128, '0') # int->hex str, thanks to @96486d9b

class ZJUAUTHME():
    AUTHME_DOMAIN = "https://zjuam.zju.edu.cn"
    def __init__(self, xh, password):
        self.xh = xh
        self.password = password
        self.status = "Not Login"
        self.a = EasyLogin()

    def _getPubKey(self):
        data = self.a.get(self.AUTHME_DOMAIN+"/cas/v2/getPubKey", o=True).json()
        return data["exponent"], data["modulus"]

    def login(self):
        global jscontext
        self.a.get(self.AUTHME_DOMAIN+"/cas/login")
        execution = self.a.b.find("input",{"name":"execution"})["value"]
        encryptedPwd = rsa_encrypt(self.password, *self._getPubKey())
        x=self.a.post_dict(self.AUTHME_DOMAIN+"/cas/login",{"username":self.xh, "password":encryptedPwd, "authcode":"", "execution":execution, "_eventId":"submit" })
        if "iPlanetDirectoryPro" in x.headers.get("set-cookie",""):
            self.status = "Login OK"
            return True
        else:
            self.status = "Login Failed"
            return False
        
    

