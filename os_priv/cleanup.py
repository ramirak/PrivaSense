import json, os

def init_cleanup_routine():
    with open("./privasense.conf") as conf:
        data = json.load(conf)
        for p in data["paths"]:
            path_split = p.split("%")
            p = os.environ[path_split[0]] + path_split[1] 
            if os.path.isdir(p):
                print(p)

