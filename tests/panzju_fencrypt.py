import base64
import mycryptor.cryptor as cryptor
ENCRYPTION_PASSWORD = "encryption_test"
ENCRYPTION_METHOD = "aes-256-cfb" 
ENCRYPTION_IVLEN = 16 

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