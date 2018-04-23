"""CSI2108 Semester 1 2018: Assessable Workshop - Symmetric Encryption."""


# Import libraries
import os
import hashlib
from base64 import b64encode
from base64 import b64decode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def _createKey():
    pwd = input("Please enter passphrase: ")
    if len(pwd) == 0:
        pwd = "CSI2108"
        print("No passphrase detected, defaulting to: " + pwd)
    sha = hashlib.sha256(pwd.encode()).digest()
    return sha


def _readMsgFile():
    fnm = input("Please enter a file to read: ")
    if len(fnm) == 0:
        fnm = "input.txt"
        print("No filename detected, defaulting to: " + fnm)
    fil = open(fnm, mode='r')
    txt = fil.read()
    txt = txt.encode()
    return txt


def _writeCrypto(msg: bytes, vec: bytes):
    fnm = input("Please enter a filename for the encryption output: ")
    if len(fnm) == 0:
        fnm = "enciphered.txt"
        print("No filename detected, defaulting to: " + fnm)
    fil = open(fnm, mode='w')
    msg = b64encode(msg).decode()
    vec = b64encode(vec).decode()
    fil.write("-----BEGIN AES256-CBC MESSAGE-----\n\n")
    fil.write(msg)
    fil.write("\n\n-----END AES256-CBC MESSAGE-----\n\n")
    fil.write("-----BEGIN AES256-CBC INITIALISATION VECTOR-----\n\n")
    fil.write(vec)
    fil.write("\n\n-----END AES256-CBC INITIALISATION VECTOR-----\n\n")


def _readCrypto():
    pass


def _encrypt(message):
    padder = padding.PKCS7(128).padder()
    padded = padder.update(message)
    padded += padder.finalize()
    backend = default_backend()
    settings = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = settings.encryptor()
    encrypted = encryptor.update(padded) + encryptor.finalize()
    return encrypted


def _decrypt(ciphertext):
    backend = default_backend()
    settings = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = settings.decryptor()
    decrypted = decryptor.update(ciphertext) + decryptor.finalize()
    # Unpad the decrypted message
    unpadder = padding.PKCS7(128).unpadder()
    unpadded = unpadder.update(decrypted)
    unpadded += unpadder.finalize()
    plaintext = unpadded.decode()
    return plaintext


# Preamble
print("CSI2108 Symmetric Encryption Tool\n")
# Input passphrase
key = _createKey()
# Input filename
message = _readMsgFile()
# Generate Initialisation Vector (IV)
iv = os.urandom(16)
# print("The Initialisation Vector (IV) is:  " + b64encode(iv).decode())
secret_message = _encrypt(message)
_writeCrypto(secret_message, iv)
deciphered = _decrypt(secret_message)
