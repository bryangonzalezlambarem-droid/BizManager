# B. G. L. 04/09/2025 Implementar cifrado y descifrado AES
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode

def encrypt_data(plain_text: str) -> str:
    aes_key = os.getenv("AES_KEY").encode()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(plain_text.encode()) + encryptor.finalize()
    return b64encode(iv + encrypted).decode()

def decrypt_data(cipher_text: str) -> str:
    aes_key = os.getenv("AES_KEY").encode()
    raw = b64decode(cipher_text)
    iv = raw[:16]
    encrypted = raw[16:]
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(encrypted) + decryptor.finalize()
    return decrypted.decode()
