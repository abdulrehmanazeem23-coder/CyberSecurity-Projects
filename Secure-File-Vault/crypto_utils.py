from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
from config import KEY_FILE

def generate_key():
    if not os.path.exists(KEY_FILE):
        key = os.urandom(32)
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        print("Encryption key generated.")

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as f:
        return f.read()

def encrypt_file(input_file, output_file):
    key = load_key()
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    with open(input_file, "rb") as f:
        data = f.read()

    encrypted = encryptor.update(data) + encryptor.finalize()

    with open(output_file, "wb") as f:
        f.write(iv + encrypted)

def decrypt_file(input_file, output_file):
    key = load_key()

    with open(input_file, "rb") as f:
        iv = f.read(16)
        encrypted = f.read()

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted = decryptor.update(encrypted) + decryptor.finalize()

    with open(output_file, "wb") as f:
        f.write(decrypted)
