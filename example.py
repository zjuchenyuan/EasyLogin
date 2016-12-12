from EasyLogin import EasyLogin
a = EasyLogin()
a.get("http://ip.cn")
IP,location = a.f("code",attrs={})
print(IP)
print(location)
