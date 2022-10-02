import json, os

from data.data_eraser import DOD_5220_22_m, erase_folder
from os_priv.os_utils import is_admin, run_as_admin


def init_cleanup_routine():
    if not is_admin():
        run_as_admin()
    try:
        with open("./privasense.conf") as conf:
            data = json.load(conf)
            for p in data["paths"]:
                path_split = p.split("%")
                p = os.environ[path_split[0]] + path_split[1] 
                if os.path.isdir(p):
                    erase_folder(p, DOD_5220_22_m)
        return 1
    except:
        return 0

