import os
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
    

def main():
    args = parse_args()
    # detect if the source is a URL or a file path
    if os.path.exists(args.source):
        mode = "file"
    else:
        mode = "url"
    print(args)

    # Load all keys
    # if url: get data and key_id
    # parse cur
    # check if retcode and if baixiao, save baixiao if true
    # save the rest
    # print if print is true
    match mode:
        case "url":
            parse_url(args.source)
            parsed_cur = parse_cur(args.source, url_data(args.source))
            # print_json(data=data)

            pass
        case "file":
            pass
        case _:
            print(f"[bold red]Uh oh... this shouldn't have happened![/]\n [grey] mode: {mode}[/]")

    pass

if __name__ == "__main__":
    main()
