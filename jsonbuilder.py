import json
import urllib

def build_json_object():
    results = json.load(urllib.urlopen("https://www.kimonolabs.com/api/6vk1k5hu?apikey=f2jrKtObW1sW7y1aJxhCHwTqiTCMzSYR"))
    import pprint; pprint.pprint(results)


build_json_object()
