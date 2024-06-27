from src.util.crypto import keyLoad
from src.util.data import dataURL, saveData
from src.util.parse import curParse
import argparse

def main():
        parser = argparse.ArgumentParser(prog="hk4e-dispatch", description="A Dispatch Response Decryptor for a certain Anime Game.")
        parser.add_argument("--url", help="QueryCurRegion URL", type=str, required=True)
        parser.add_argument("--res", help="Parse version res", type=bool, required=False, choices=[True, False])
        parser.add_argument("--out", help="Path to save the JSON File", type=str, required=False)
        args = parser.parse_args()

        i = 2
        while i < 6:    
            keyLoad(i)
            i += 1
        keyLoad("SigningKey")

        data, key_id = dataURL(args.url)
        
        curParse(args.url, data, int(key_id))
        formatted_cur, game_version, baixiao, version_res = curParse(args.url, data, key_id, args.res)

        if args.out:
            saveData(formatted_cur, game_version, args.out)
            if not "retcode" in formatted_cur and args.res == True:
                saveData(baixiao, version_res, args.out)
        else:
             saveData(formatted_cur, game_version, "out/")
             if not "retcode" in formatted_cur and args.res == True:
                saveData(baixiao, version_res, "out/")

        print(f"Done!")

if __name__ == "__main__":
    main()
