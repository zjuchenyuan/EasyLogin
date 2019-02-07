import requests
from urllib.parse import quote
from base64 import b64encode
s = requests.session()

def ocr(img_bytes):
    # 返回 ["success", 识别结果, confidence int]
    global s
    x=s.post("https://api.py3.io/ocr", "img="+quote(b64encode(img_bytes).decode()), headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
    text, confidence = x.json()
    text = text.replace(" ","")
    if len(text)==4 and text.isdigit() and len(confidence) and confidence[0]>40:
        return ["success", text, confidence[0]]
    else:
        return ["fail", text, confidence]