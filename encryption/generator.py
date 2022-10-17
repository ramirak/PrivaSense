import os, hashlib, random
from Cryptodome.Random import get_random_bytes
from Cryptodome.PublicKey import RSA
import secrets, string
from data.id import *
import data.enums as enums

key_filename = "master.key"
key_sig_length = 8


def generate_key(key_length):
    user_key = get_random_bytes(key_length)
    key_sig = get_random_bytes(key_sig_length)
    with open(key_filename, "wb+") as key_file:
        key_file.write(key_sig), key_file.write(user_key)
    return key_sig, user_key


def retrieve_key():
    if os.path.isfile(key_filename):
        # Key exists
        with open(key_filename, "rb") as key_file:
            return key_file.read(key_sig_length), key_file.read()
    return None, None


def generate_rsa():
    key = RSA.generate(2048, os.urandom)
    priv = key.exportKey('PEM')
    pub = key.exportKey('OpenSSH')
    return priv, pub


def generate_password(length=16):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password


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


def generate_form():
    form = ("First name: " + get_name() + "\n" 
    + "Last name: " + get_name() + "\n" 
    + "Age: " + str(random.randint(18,80)) + "\n"
    + "City: " + get_city() + "\n" 
    + "Street: " + get_street() + " " + str(random.randrange(999)) + "\n" 
    + "Zip code: " + str(random.randrange(9999)) + "\n" 
    + "Phone number: " + str(random.randrange(99)) + str(random.randint(123456789,999999999)))
    return form


def generator_manager(gen_mode):
    if gen_mode == enums.generators.FAKE_FORM.name:
        return generate_form()
    elif gen_mode == enums.generators.SSH_KEY.name:
        return generate_rsa()
    elif enums.generators.SECURE_PASSWORD.name:
        return generate_password()