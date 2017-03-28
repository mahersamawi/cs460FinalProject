import getpass
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import subprocess
import os
import shutil

USER = getpass.getuser()
HOME_PATH = '/home/' + USER

def encrypt_home(password):
    # public_key, private_key = gen_key_rsa(password)
    # with open(PUBLIC_KEY_PATH, 'w') as f:
    #     f.write(public_key)
    # with open(PRIVATE_KEY_PATH, 'w') as f:
    #     f.write(private_key)
    subprocess.check_output('zip -r {0}.zip {0}'.format(HOME_PATH), shell=True)
    with open(HOME_PATH + '.zip', 'r') as f:
        zip_data = f.read()
    iv = Random.new().read(AES.block_size)
    key = gen_key_aes(password)
    encrypted_data = iv + encrypt_aes(zip_data, key, iv)
    # encrypted_key = encrypt_rsa(key, public_key)[0]
    with open(HOME_PATH + '.locked', 'w') as f:
        f.write(encrypted_data)
    # with open(ENCRYPTED_KEY_PATH, 'w') as f:
    #     f.write(encrypted_key)
    os.remove(HOME_PATH + '.zip')
    shutil.rmtree(HOME_PATH)

def decrypt_home(password):
    if not os.path.isfile(HOME_PATH + '.locked'):
        print 'Home is already decrypted.'
        return
    # with open(ENCRYPTED_KEY_PATH, 'r') as f:
    #     encrypted_key = f.read()
    # with open(PRIVATE_KEY_PATH, 'r') as f:
    #     private_key = f.read()
    # with open(HOME_PATH + '.locked', 'r') as f:
    #     iv = f.read(AES.block_size)
    #     encrypted_data = f.read()
    # try:
    #     key = decrypt_rsa(encrypted_key, private_key, SHA256.new(password).hexdigest())
    # except ValueError:
    #     print 'Incorrect password.'
    key = gen_key_aes(password)
    zip_data = decrypt_aes(encrypted_data, key, iv)
    with open(HOME_PATH + '.zip', 'w') as f:
        f.write(zip_data)
    subprocess.check_output('unzip ' + HOME_PATH + '.zip -d /', shell=True)
    os.remove(HOME_PATH + '.locked')
    os.remove(HOME_PATH + '.zip')


# def encrypt_rsa(data, key):
#     return RSA.importKey(key).encrypt(data, 0)

# def decrypt_rsa(data, key, password_hash):
#     return RSA.importKey(key, password_hash).decrypt(data)

def encrypt_aes(data, key, iv):
    data = data.rstrip('\n')
    if len(data) % 16:
        aligned_data = data + ('\n' * (16 - (len(data) % 16)))
    else:
        aligned_data = data
    return AES.new(key, AES.MODE_CBC, iv).encrypt(aligned_data)

def decrypt_aes(data, key, iv):
    return AES.new(key, AES.MODE_CBC, iv).decrypt(data).rstrip('\n')

# def gen_key_rsa(password):
#     private_key = RSA.generate(2048)
#     public_key = private_key.publickey()
#     return public_key.exportKey(), private_key.exportKey(passphrase=SHA256.new(password).hexdigest())

def gen_key_aes(password=None):
    if password is None:
        ret = ""
        for i in range(32):
            ret += chr(Random.random.randint(0, 255))
        return ret
    else:
        return SHA256.new(password).digest()
