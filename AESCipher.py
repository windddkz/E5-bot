import json
import base64
import hashlib

from Crypto import Random
from Crypto.Cipher import AES

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-s[-1]]


class AESCipher:
    def __init__(self, key):
        self.key = hashlib.sha256(key.encode('utf-8')).digest()

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:]))


if __name__ == "__main__":
    cipher = AESCipher('secretkey')
    encrypted = cipher.encrypt('Secret Message A')
    decrypted = cipher.decrypt(encrypted)
    print(encrypted)
    print(decrypted)

    encrypt_file = open("./o365_token_encrypt.txt", "wb")
    with open("./o365_token.txt", "r") as f:
        token_json = f.read()
        token_raw = json.loads(token_json)
        encrypt_file.write(cipher.encrypt(token_json))
    encrypt_file.close()

    with open("./o365_token_encrypt.txt", "rb") as f:
        decrypted_json = cipher.decrypt(f.read())
        token_new = json.loads(decrypted_json.decode("utf-8"))

    print(token_raw == token_new)
    print(json.dumps(token_new, indent=4))
