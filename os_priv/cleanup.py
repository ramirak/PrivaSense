import json, os

from data.data_eraser import erase_folder
from os_priv.os_utils import is_admin, run_as_admin
import data.enums as enums


def init_cleanup_routine(paths):
    if not is_admin():
        run_as_admin()
    try:
        for p in paths:
            
            path_split = p.split("%")
            p = os.environ[path_split[0]] + path_split[1] 
            print(p)
            if os.path.isdir(p):
                erase_folder(p, enums.erase_algorithms.DOD_5220_22_m.name)
        return enums.results.SUCCESS.value
    except Exception as e:
        print(e)
        return enums.results.ERR_UNKNOWN.value

