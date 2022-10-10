import os
from threading import Lock
import data.enums as enums

garbage_file = "garbage"

critical_function_lock = Lock()

def erase_free_space():
    if critical_function_lock.locked():
        return enums.results.ALREADY_RUNNING.value
    try:
        with critical_function_lock:
            with open(garbage_file, 'wb+') as f:
                while True:
                    f.write(os.urandom(1))
    except:
        os.remove(garbage_file)

