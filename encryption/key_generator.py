import os, hashlib

key_filename = "master.key"
key_sig_length = 8

def generate_key(key_length):
    user_key = os.urandom(key_length)
    key_sig = os.urandom(key_sig_length)
    with open(key_filename, "wb+") as key_file:
        key_file.write(key_sig), key_file.write(user_key)
    return key_sig, user_key


def retrieve_key():
    if os.path.isfile(key_filename):
        # Key exists
        with open(key_filename, "rb") as key_file:
            return key_file.read(key_sig_length), key_file.read()
    return None, None


def sha256sum(filename):
    if os.path.isdir(filename):
        return;
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        while n := f.readinto(mv):
            h.update(mv[:n])
    return h.hexdigest()