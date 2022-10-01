import os, glob, random

DOD_5220_22_m, NCSC_TG_025, HMG_IS5, ISM_6_2_92, RCMP_TSSIT_OPS_II, *_ = range(10) 

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

    if mode == DOD_5220_22_m:
        overwrite(file_path, length, zeros)
        overwrite(file_path, length, ones)
        overwrite(file_path, length, None)
    elif mode == NCSC_TG_025:
        n_overwrites = assert_choice(input("How many overwrites?"))
        if n_overwrites == -1:
            print("Invalid input")
            return -1
        for i in range(n_overwrites):
            overwrite(file_path, length, zeros)
            overwrite(file_path, length, ones)
            overwrite(file_path, length, None)
    elif mode == RCMP_TSSIT_OPS_II:
        for i in range(3):
            overwrite(file_path, length, zeros)
            overwrite(file_path, length, ones)
        overwrite(file_path, length, None)
    elif mode == HMG_IS5:
        overwrite(file_path, length, zeros)
        overwrite(file_path, length, None)
    elif mode == ISM_6_2_92:
        overwrite(file_path, length, None)

    remove(file_path)
    return


def overwrite(file_path, bytes_len, value):
    with open(file_path, 'wb') as f:
        if value != None:
            for b in range(bytes_len):
                f.write(value)
        else:
            f.write(os.urandom(bytes_len))


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