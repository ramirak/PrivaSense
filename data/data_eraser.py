import os, glob, random
import data.enums as enums


def erase_folder(folder_path, mode):
    try:
        for filename in glob.iglob(folder_path + "/**", recursive=True):
            if os.path.isfile(filename):
                erase(filename, mode)
    except:
        return

def erase(file_path, mode):
    length = 0
    ones = b'\xFF'
    zeros = b'\x00'
    ## Get the positin of the last byte in the file 
    with open(file_path, 'ab') as f:
        length = f.tell()
    if mode == enums.erase_algorithms.DOD_5220_22_m.name:
        overwrite(file_path, length, zeros)
        overwrite(file_path, length, ones)
        overwrite(file_path, length, None)
    elif mode == enums.erase_algorithms.RCMP_TSSIT_OPS_II.name:
        for i in range(3):
            overwrite(file_path, length, zeros)
            overwrite(file_path, length, ones)
        overwrite(file_path, length, None)
    elif mode == enums.erase_algorithms.HMG_IS5.name:
        overwrite(file_path, length, zeros)
        overwrite(file_path, length, None)
    elif mode == enums.erase_algorithms.ISM_6_2_92.name:
        overwrite(file_path, length, None)
    else:
        return enums.results.ERR_UNKNOWN.value
    remove(file_path)
    return enums.results.SUCCESS.value


def overwrite(file_path, bytes_len, value):
    try:
        with open(file_path, 'wb') as f:
            if value != None:
                for b in range(bytes_len):
                    f.write(value)
            else:
                f.write(os.urandom(bytes_len))
    except:
        return 

def remove(file_path):
    ## Generate a new random name before removing
    new_file_name = str(random.getrandbits(32))
    os.rename(file_path, new_file_name)
    os.remove(new_file_name)


def assert_choice(choice):
    try:
        choice = int(choice)
    except:
        return -1;
    return choice