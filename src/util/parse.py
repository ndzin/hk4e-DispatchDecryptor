from src.util.proto import QueryCurrRegionHttpRsp
from src.util.crypto import decrypt
from urllib import parse
import base64

def curParse(url, data, key, bai=False):
    decrypted = decrypt(base64.b64decode(data['content']), key)
    cur = QueryCurrRegionHttpRsp().parse(decrypted)
    cur.region_custom_config_encrypted = b''
    cur.client_secret_key = b''
    cur.region_info.res_version_config.md5 = ""
    cur.region_info.secret_key = b''
    cur.region_info.next_res_version_config.md5 = ""
    
    version = parse.parse_qs(parse.urlparse(url).query).get('version', [''])[0]

    game_version = f"{version}.json"

    if cur.retcode == 20 or cur.retcode == 1:
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
        if (bai):
            version_res = f"{version}-baixiao.json"
            baixiao = {
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
            return(formatted_cur, game_version, baixiao, version_res)
        
    return(formatted_cur, game_version, None, None)