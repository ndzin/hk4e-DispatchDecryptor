from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import os

from rich import print

class HoyoCrypt:
    def __init__(self) -> None:
        self.keys = {}
        self.keyspath = os.path.join(os.path.abspath(os.curdir), "src", "keys")
        self.load_keys()
        self.pkcs = PKCS1_v1_5
        

    def load_keys(self):
        for key in range(2, 6):
            with open(os.path.join(self.keyspath, f"{key}.pem"), "r") as f:
                self.keys[key] = RSA.import_key(f.read())
        with open(os.path.join(self.keyspath, "SigningKey.pem"), "r") as f:
            self.keys["SigningKey"] = RSA.import_key(f.read())
    

    def decrypt(self, data: bytes, key_id) -> bytes:
        print()
        dec = self.pkcs.new(self.keys[int(key_id)])
        
        out = b''
        for i in range(0, len(data), 256):
            chunk = data[i:i + 256]
            out += dec.decrypt(chunk, None)
        return out



if __name__ == "__main__":
    crypto = HoyoCrypt()
    crypto.load_keys()