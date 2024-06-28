import os
import json
import argparse
import requests

from rich import print, print_json

from .utils.parser import parse_url, parse_cur

def url_data(url):
    return requests.get(url).json()

def parse_args()    :
    parser = argparse.ArgumentParser(prog="Dispatch Decryptor", description="🌐 HK4E dispatch response decryptor")
    
    parser.add_argument("source", type=str, help="Source of the dispatch response (URL/Path)")
    parser.add_argument("-o", "--output", type=str, help="Output path for the decrypted response", default=os.path.join(os.path.abspath(os.curdir), "output"))
    parser.add_argument("-p", "--print", action="store_true", help="Print the decrypted response to the console")
    parser.add_argument("--baixiao", action="store_true", help="Parse version-res for Baixiao")
    
    return parser.parse_args()


def save_data(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def main():
    root = os.path.abspath(os.path.curdir)
    output = os.path.join(root, "output")

    if not os.path.exists(output):
        os.makedirs(output, exist_ok=True)

    args = parse_args()
    # detect if the source is a URL or a file path
    if os.path.exists(args.source):
        mode = "file"
    else:
        mode = "url"

    match mode:
        case "url":
            url_info = parse_url(args.source)
            url_info["data"] = url_data(url_info['fixed'])
            
            parsed_cur = parse_cur(args.source, url_info)

            if args.print:
                print("Cur:")
                print_json(data=parsed_cur)
            
            if args.baixiao:
                baixiao_cur = {
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
                save_data(baixiao_cur, os.path.join(output, f"{url_info['version']}-baixiao.json"))
            
            save_data(parsed_cur, os.path.join(output, f"{url_info['version']}.json"))
            # print_json(data=url_info)
            # print_json(data=data)
            pass
        case "file":
            with open(args.source, "r") as file:
                data = json.loads(file.read())
            
            parsed_cur = parse_cur("file", data)
            pass
        case _:
            print(f"[bold red]Uh oh... this shouldn't have happened![/]\n [grey] mode: {mode}[/]")

    pass

if __name__ == "__main__":
    main()
