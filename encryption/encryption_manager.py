import base64, glob, os
from .aes import *
from encryption.key_generator import generate_key, retrieve_key
import data.enums as enums
import data.data_eraser as data_eraser
from threading import Lock

Encrypted = b"enc"

critical_function_lock = Lock()

def encrypt_file(filepath, reserved):
    if critical_function_lock.locked():
        return enums.results.ALREADY_RUNNING.value
    try:
        with critical_function_lock:
            key_sig, generated_key = b"" , b""
            # Only interested if file is encrypted, method is only relavnt for decryption
            is_encrypted, encryption_method_assert = isEncrypted(filepath, None) 
            if is_encrypted:
                return enums.results.ERR_ALREADY_ENCRYPTED.value
            # Not encrypted yet, read all file
            f = open(filepath, "rb")
            bytes_arr = f.read()
            bytes_arr = base64.b64encode(bytes_arr).decode("utf-8")
            # Key setup - either generate or retieve
            s, k = retrieve_key()
            if s == None or k == None:
                key_sig, generated_key = generate_key(32)
            else:
                key_sig = s
                generated_key = k   

            encrypted = encrypt(bytes_arr, generated_key) 
            f.close()
            header = generate_header(enums.enc_algorithms.AES_256_CFB.value, key_sig)

            replace_file(filepath, encrypted, header)
            return enums.results.SUCCESS.value
    except:
        return enums.results.ERR_UNKNOWN.value


def decrypt_file(filepath, reserved):
    if critical_function_lock.locked():
        return enums.results.ALREADY_RUNNING.value
    with critical_function_lock:
        is_encrypted, encryption_method_assert = isEncrypted(filepath, enums.enc_algorithms.AES_256_CFB.value) 
        if not is_encrypted:
            return enums.results.ERR_NOT_ENCRYPTED.value
        if not encryption_method_assert:
            return enums.results.ERR_DIFFERENT_METHOD.value
        try:
            f = open(filepath, "rb")
            # First byytes are the header
            header = f.read(12)
            is_enc, enc_method, enc_id = split_header(header)
            bytes_arr = f.read()
            key_sig, key = retrieve_key()
            if base64.b64encode(key_sig).decode('utf-8') != base64.b64encode(enc_id).decode('utf-8'):
                return enums.results.ERR_INVALID_KEY.value
            decrypted = base64.b64decode(decrypt(bytes_arr, key).encode('utf-8'))
            f.close()
            replace_file(filepath, decrypted, None)
            return enums.results.SUCCESS.value
        except:
            return enums.results.ERR_UNKNOWN.value


def encrypt_folder(folder_path, reserved):
    all_res = []
    c_s, c_f = 0 , 0
    if critical_function_lock.locked():
        return enums.results.ALREADY_RUNNING.value
    try:
        for filename in glob.iglob(folder_path + "/**", recursive=True):
            if os.path.isfile(filename):
                res = encrypt_file(filename, reserved)
                all_res.append(res)
                if res != enums.results.SUCCESS.value:
                    c_f += 1
                else:
                    c_s += 1
        return op_fin("Directory dncryption", c_s, c_f, all_res)
    except:
        return enums.results.ERR_UNKNOWN.value


def decrypt_folder(folder_path, reserved):
    all_res = []
    c_s, c_f = 0 , 0
    if critical_function_lock.locked():
        return enums.results.ALREADY_RUNNING.value
    try:
        for filename in glob.iglob(folder_path + "/**", recursive=True):
            if os.path.isfile(filename):
                res = decrypt_file(filename, reserved)
                all_res.append(res)
                if res != enums.results.SUCCESS.value:
                    c_f += 1
                else:
                    c_s += 1
        return op_fin("Directory decryption", c_s, c_f, all_res)
    except:
        return enums.results.ERR_UNKNOWN.value


def op_fin(op_name, c_s, c_f, all_res):
    '''
    from datetime import datetime
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    with open("log", "a+") as log_file:
        log_file.write(dt_string)
    '''
    if c_s > 0 and c_f > 0:
        return enums.results.PARTLY_SUCCESS.value
    elif c_s == 0 and c_f > 0:
        return enums.results.MULTIPLE_ERRORS.value
    else: 
        return enums.results.SUCCESS.value


def replace_file(filepath, bytes_arr, header):
    temp_add = ".temp"
    with open(filepath + temp_add, "wb+") as new_file:
        if header != None:
            new_file.write(header)
        new_file.write(bytes_arr)
    data_eraser.erase(filepath, enums.erase_algorithms.DOD_5220_22_m.name)
    os.rename(filepath + temp_add, filepath)


def isEncrypted(filepath, enc_method):
    with open(filepath, "rb") as f:
        file_signature = f.read(3)
        # Check if enc header exists in this file
        if file_signature == Encrypted:
            # Encrypted, check enc type
            enc_method_sig = f.read(1).decode("utf-8")
            if str(enc_method) == enc_method_sig:
                # Full match to the requested encryption
                return True, True
                # Encrypted but with different algorithm
            return True, False
    # Not encrypted
    return False, False


def generate_header(method, key_sig):
    ## IsEncrypted ~~ EncyptionMethod ~~ KeyID
    ##  3bytes ~~ 1byte ~~ 8bytes
    header = bytearray()
    header += Encrypted
    header += str(method).encode("utf-8")
    header += key_sig
    return header 


def split_header(sig_bytes):
    is_enc = sig_bytes[:3]
    enc_method = sig_bytes[3]
    enc_sig = sig_bytes[4:12]
    
    return is_enc, enc_method, enc_sig