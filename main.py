from src.util.crypto import keyLoad
from src.util.data import dataURL, saveData
from src.util.parse import curParse
import argparse

def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("--url", help="URL argument", type=str, required=True)
        parser.add_argument("--baixiao", help="Parse version-res for Baixiao", required=False)
        args = parser.parse_args()

        i = 2
        while i < 6:    
            keyLoad(i)
            i += 1
        keyLoad("SigningKey")

        data, key_id = dataURL(args.url)
        
        curParse(args.url, data, int(key_id))
        formatted_cur, game_version, baixiao, version_res = curParse(args.url, data, key_id, args.baixiao)

        if not "retcode" in formatted_cur and args.baixiao == "True":
            saveData(baixiao, version_res)
        saveData(formatted_cur, game_version)

        print(f"Done!")

if __name__ == "__main__":
    main()
