from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import os

keys = {}
path = "keys"

def keyLoad(key_id):
    with open(os.path.join(path, f"{key_id}.pem"), 'r') as f:
        keys[key_id] = RSA.import_key(f.read())

def doSign(message, key):
    signer = pkcs1_15.new(key)
    digest = SHA256.new(message)
    return signer.sign(digest)

def doSignature(data: bytes, key_id):
    sign_key = keys["SigningKey"]
    key = keys[key_id]
    enc = PKCS1_v1_5.new(key)
    chunk_size = 256 - 11
    out = b''
    if len(data) > chunk_size:
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i + chunk_size]
            out += enc.encrypt(chunk)
    else:
        out = enc.encrypt(data)
    signature = doSign(data, sign_key)
    return out, signature

def decrypt(data: bytes, key_id) -> bytes:
    key = keys[key_id]
    dec = PKCS1_v1_5.new(key)
    chunk_size = 256
    out = b''
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        out += dec.decrypt(chunk, None)
    return out