def parse_cur(url, data):
    game_version = parse_url(url)['version']
    
    # Parse cur logic
    
    pass

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
        "url": reconstructed_url,
        "key_id": key_id,
        "version": version
    }