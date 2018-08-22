import base64
import hashlib
import json

from Crypto import Random
from Crypto.Cipher import AES


class EncryptionService:

    BS = 16
    SECRET_KEY = "secret"

    def __init__(self, file_service):
        secret_path = file_service.get_secret_path()
        secret_file = open(secret_path, "r")
        secret_dict = json.loads(secret_file.read())
        secret_file.close()
        secret = secret_dict[self.SECRET_KEY]
        self.key = hashlib.sha256(secret.encode()).digest()

    def encrypt(self, raw):
        raw = self.__pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def encrypt_to_string(self, raw):
        return self.encrypt(raw).decode()

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self.__unpad(cipher.decrypt(enc[16:]))

    def decrypt_to_string(self, enc):
        return self.decrypt(enc).decode()

    def __pad(self, s):
        return s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)

    def __unpad(self, s):
        return s[0:-s[-1]]
