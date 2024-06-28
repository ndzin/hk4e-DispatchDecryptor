import base64

from .crypto import HoyoCrypt
from .proto import QueryCurrRegionHttpRsp

def parse_cur(url_info):
    # Parse cur logic
    crypt = HoyoCrypt()
    decrypted = crypt.decrypt(base64.b64decode(url_info['data']['content']), url_info['key_id'])

    cur = QueryCurrRegionHttpRsp().parse(decrypted)
    cur.region_custom_config_encrypted = b''
    cur.client_secret_key = b''
    cur.region_info.res_version_config.md5 = ""
    cur.region_info.secret_key = b''
    cur.region_info.next_res_version_config.md5 = ""

    if cur.retcode == 20 or cur.retcode == 1:
        return {
            "retcode": cur.retcode,
            "msg": cur.msg,
            "regionInfo": {
                "resVersionConfig": {},
                "nextResVersionConfig": {}
            },
            "forceUpdate": {}
        }
    else:
        return {
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


def parse_baixiao(parsed_cur):
    return {
                    f"{parsed_cur['regionInfo']['resVersionConfig']['branch']}": {
                        "full": {},
                        "hdiff": {},
                        "resource_info": [
                            {
                                "res": {
                                    "version": parsed_cur['regionInfo']['resVersionConfig']['version'],
                                    "suffix": parsed_cur['regionInfo']['resVersionConfig']['versionSuffix']
                                },
                                "client": {
                                    "version": parsed_cur['regionInfo']['clientDataVersion'],
                                    "suffix": parsed_cur['regionInfo']['clientVersionSuffix'],
                                },
                                "silence": {
                                    "version": parsed_cur['regionInfo']['clientSilenceDataVersion'],
                                    "suffix": parsed_cur['regionInfo']['clientSilenceVersionSuffix']
                                }
                            }
                        ]
                    }
                }
    

def parse_url(url):
    url = url.split("?")
    base_url = url[0]
    url_args = url[1].split("&")
    
    for i, arg in enumerate(url_args):
        if "lang=" in arg:
            if arg.split("=")[1] != "1":
                url_args[i] = "lang=1"

        if "key_id=" in arg:
            key_id = arg.split("=")[1]

        if "version=" in arg:
            version = arg.split("=")[1]

    reconstructed_url = base_url + "?" + "&".join(url_args)
    return {
        "fixed": reconstructed_url,
        "key_id": key_id,
        "version": version
    }