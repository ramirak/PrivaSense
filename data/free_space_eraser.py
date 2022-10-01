import os

garbage_file = "garbage"

def erase_free_space():
    try:
        with open(garbage_file, 'wb+') as f:
            while True:
               f.write(os.urandom(1))
    except Exception as e:
        os.remove(garbage_file)

