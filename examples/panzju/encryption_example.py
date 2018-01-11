"""
这是一个加密方法的示例
文件名不做加密，仅仅用base64编码
加密密码、加密方式、IV长度来自config.py
回调函数仅是print出来
"""

import base64
import mycryptor.cryptor as cryptor
from config import ENCRYPTION_PASSWORD, ENCRYPTION_METHOD, ENCRYPTION_IVLEN

def fencrypt_filename(filename):
    return base64.b64encode(filename.encode("utf-8")).decode().replace("+","~").replace("/","@")

def fencrypt_data(data_generator):
    c = cryptor.Cryptor(ENCRYPTION_PASSWORD, ENCRYPTION_METHOD)
    for data in data_generator:
        yield c.encrypt(data)

def fencrypt_callback(filename_plaintext, filename_ciphertext, folder_id, fileid):
    print(filename_plaintext, filename_ciphertext, folder_id, fileid)

fencrypt = {
    "fencrypt_filename": fencrypt_filename,
    "fencrypt_data": fencrypt_data,
    "fencrypt_addlen": ENCRYPTION_IVLEN,
    "fencrypt_callback":fencrypt_callback,
}