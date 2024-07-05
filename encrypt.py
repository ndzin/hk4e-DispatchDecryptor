from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

import os
from rich import print

class HoyoEncrypt:
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
    
    def encryptKey(self, data: bytes, key_id) -> bytes:
        print()
        enc = self.pkcs.new(self.keys[int(key_id)])
        
        out = b''
        for i in range(0, len(data), 214):  # RSA encryption with PKCS1_v1_5 padding allows up to 214 bytes per chunk
            chunk = data[i:i + 214]
            out += enc.encrypt(chunk)
        return out

    def encryptSign(self, data: bytes, key_id) -> bytes:
        enc = self.pkcs.new(self.keys[key_id])

        return enc.encrypt(data)
    
    def doSign(message, key):
        signer = pkcs1_15.new(key)
        digest = SHA256.new(message)
        return signer.sign(digest)

    def doSignature(data: bytes, key_id):
        key = "SigningKey"
        enc = PKCS1_v1_5.new(key)
        chunk_size = 256 - 11
        out = b''
        if len(data) > chunk_size:
            for i in range(0, len(data), chunk_size):
                chunk = data[i:i + chunk_size]
                out += enc.encrypt(chunk)
        else:
            out = enc.encrypt(data)
            signature = HoyoEncrypt.doSign(data, key)
        return out, signature

if __name__ == "__main__":
    crypto = HoyoEncrypt()
    crypto.load_keys()
    with open("output/CNCBWin4.7.54.json", "r") as f:
        data = f.read().encode("utf-8")

    
    with open("src/keys/SigningKey.pem", "r") as f:    
        key = RSA.import_key(f.read())  
    out = HoyoEncrypt.doSignature(data, key)
    for i in range(2, 5):
        out = "{"+f"""
    \"content\": \"{crypto.encryptKey(data, i).hex() }\",
    \"sign\": \"{out}\"
    """+"}"
        with open(f"output/encrypted_data_{i}.json", "w") as f:
            f.write(out)
     #   with open(f"output/encrypted_sign_{i}.json", "wb") as f:
         #   f.write(out["sign"].encode("utf-8"))

