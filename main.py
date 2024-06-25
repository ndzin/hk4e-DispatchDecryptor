from Crypto.PublicKey import RSA
import os
import base64
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from proto import QueryCurrRegionHttpRsp
from urllib.request import urlopen
from urllib import parse
keys = {}
path = "keys"

def load_key(key_id):
    with open(os.path.join(path, f"{key_id}.pem"), 'r') as f:
        keys[key_id] = RSA.import_key(f.read())

def do_sign(message, key):
    signer = pkcs1_15.new(key)
    digest = SHA256.new(message)
    return signer.sign(digest)

def encrypt_and_sign(data: bytes, key_id):
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
    signature = do_sign(data, sign_key)
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

def get_data_from_url():
    url = input("Enter URL: ")
    lang = int(parse.parse_qs(parse.urlparse(url).query)['lang'][0])
    if lang != 1:
        url = url.replace(f'lang={lang}', 'lang=1')
    body = urlopen(url).read()
    data = json.loads(body)
    key_id = int(parse.parse_qs(parse.urlparse(url).query)['key_id'][0])

    return data, key_id, url

def get_data_from_key():
    key_id = int(input("Enter key: "))
    data = json.loads(input("Enter data: "))
    return data, key_id

def save_data_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    i = 2
    while i < 6:    
        load_key(i)
        i += 1
    load_key("SigningKey")

    data, key, url = get_data_from_url()
    version = parse.parse_qs(parse.urlparse(url).query).get('version', [''])[0]

    decrypted = decrypt(base64.b64decode(data['content']), key)
    cur = QueryCurrRegionHttpRsp().parse(decrypted)
    cur.region_custom_config_encrypted = b''
    cur.client_secret_key = b''
    cur.region_info.res_version_config.md5 = ""
    cur.region_info.secret_key = b''
    cur.region_info.next_res_version_config.md5 = ""

    filename = f"{version}.json"

    if cur.retcode == 20:
        formatted_cur = {
            "retcode": cur.retcode,
            "msg": cur.msg,
            "regionInfo": {
                "resVersionConfig": {},
                "nextResVersionConfig": {}
            },
            "forceUdpate": {}
        }
    else:
        formatted_cur = {
            "regionInfo": {
                "gateserverIp": cur.region_info.gateserver_ip,
                "gateserverPort": cur.region_info.gateserver_port,
                "areaType": cur.region_info.area_type,
                "resourceUrl": cur.region_info.resource_url,
                "dataUrl": cur.region_info.data_url,
                "feedbackUrl": cur.region_info.feedback_url,
                "resourceUrlBak": cur.region_info.resource_url_bak,
                "clientDataVersion": cur.region_info.client_data_version,
                "handbookUrl": cur.region_info.handbook_url,
                "clientSilenceDataVersion": cur.region_info.client_silence_data_version,
                "clientDataMd5": cur.region_info.client_data_md5,
                "clientSilenceDataMd5": cur.region_info.client_silence_data_md5,
                "resVersionConfig": {
                    "version": cur.region_info.res_version_config.version,
                    "releaseTotalSize": cur.region_info.res_version_config.release_total_size,
                    "versionSuffix": cur.region_info.res_version_config.version_suffix,
                    "branch": cur.region_info.res_version_config.branch
                },
                "officialCommunityUrl": cur.region_info.official_community_url,
                "clientVersionSuffix": cur.region_info.client_version_suffix,
                "clientSilenceVersionSuffix": cur.region_info.client_silence_version_suffix,
                "accountBindUrl": cur.region_info.account_bind_url,
                "cdkeyUrl": cur.region_info.cdkey_url,
                "privacyPolicyUrl": cur.region_info.privacy_policy_url,
                "nextResVersionConfig": {}
            }
        }
        version_res = f"{version}-res.json"
        # for baixiao
        content = {
            f"{cur.region_info.res_version_config.branch}": {
                "full": {},
                "hdiff": {},
                "resource_info": [
                    {
                        "res": {
                            "version": cur.region_info.res_version_config.version,
                            "suffix": cur.region_info.res_version_config.version_suffix
                        },
                        "client": {
                            "version": cur.region_info.client_data_version,
                            "suffix": cur.region_info.client_version_suffix
                        },
                        "silence": {
                            "version": cur.region_info.client_silence_data_version,
                            "suffix": cur.region_info.client_silence_version_suffix
                        }
                    }
                ]
            }
        }
        save_data_to_file(content, version_res)

    save_data_to_file(formatted_cur, filename)
    print(f"Done!")


if __name__ == "__main__":
    main()
